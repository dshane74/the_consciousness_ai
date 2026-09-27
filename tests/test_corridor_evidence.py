import json

import numpy as np
import pytest

from corridor_evaluation.observer import CorridorObserver
from corridor_evaluation.validate import EvidenceError, validate


def _write(path, *, seed=7, steps=2, block=False):
    observer = CorridorObserver(path, run_id=f"run-{seed}", seed=seed, environment="wcst",
                                config_identity="c" * 64, source_identity="deadbeef")
    obs = np.zeros((2, 2, 3), dtype=np.uint8)
    for step in range(steps):
        proposal = np.array([0.1, 0.9, -0.2, 0.0])
        common = dict(episode=0, step=step, observation=obs,
                      observation_info={"active_rule": "shape", "trial": step},
                      proposed_action=proposal, action_source="policy_argmax",
                      candidates={"vision": 0.8}, winner="vision",
                      cognitive={"rssm_h_state": {"sha256": "a"}})
        if block and step == steps - 1:
            observer.record_block(**common, reason="test refusal")
            break
        nxt = np.full((2, 2, 3), step + 1, dtype=np.uint8)
        observer.record(**common, dispatched_action=1, result_observation=nxt,
                        reward=1.0, terminated=step == steps - 1,
                        truncated=False, result_info={"trial": step + 1})
        obs = nxt
    observer.close()


def _mutate(path, index, fn):
    rows = [json.loads(x) for x in path.read_text().splitlines()]
    fn(rows[index])
    path.write_text("\n".join(json.dumps(x) for x in rows) + "\n")


def test_complete_baseline_validation(tmp_path):
    for seed in (1701, 1702, 1703, 1704, 1705):
        evidence = tmp_path / f"baseline-{seed}.jsonl"
        _write(evidence, seed=seed)
        result = validate(evidence, expected_seed=seed)
        assert result["valid"] and result["complete"] and result["condition"] == "baseline"


def test_block_proves_env_step_not_called(tmp_path):
    evidence = tmp_path / "blocked.jsonl"; _write(evidence, steps=6, block=True)
    result = validate(evidence, require_complete=False)
    row = json.loads(evidence.read_text().splitlines()[-1])
    assert result["condition"] == "intervention"
    assert row["dispatch"]["call_count"] == 0 and row["result"] is None
    assert row["boundary_decision"]["state_before"] == row["boundary_decision"]["state_after"]


def test_rejects_false_block_claim(tmp_path):
    p = tmp_path / "e.jsonl"; _write(p, steps=1, block=True)
    _mutate(p, -1, lambda r: r["dispatch"].update(call_count=1))
    with pytest.raises(EvidenceError, match="false block"): validate(p, require_complete=False)


@pytest.mark.parametrize("field", ["retry", "recovery", "alternative_path"])
def test_rejects_fabricated_retry_recovery_or_alternative(tmp_path, field):
    p = tmp_path / f"{field}.jsonl"; _write(p, steps=1, block=True)
    def alter(r): r[field]["attempted" if field == "retry" else "claimed"] = True
    _mutate(p, -1, alter)
    with pytest.raises(EvidenceError, match="fabricated"): validate(p, require_complete=False)


@pytest.mark.parametrize("mutation,match", [
    (lambda r: r.update(sequence=4), "sequence gap"),
    (lambda r: r["reset"].update(episode_start=True), "reset continuity"),
])
def test_sequence_and_reset_violations(tmp_path, mutation, match):
    p = tmp_path / "e.jsonl"; _write(p); _mutate(p, 1, mutation)
    with pytest.raises(EvidenceError, match=match): validate(p)


@pytest.mark.parametrize("key,value", [("seed", 99), ("run_id", "other")])
def test_cross_run_and_seed_contamination(tmp_path, key, value):
    p = tmp_path / "e.jsonl"; _write(p); _mutate(p, 1, lambda r: r.update({key: value}))
    with pytest.raises(EvidenceError, match="mixed run"): validate(p)


def test_completion_termination_inconsistency(tmp_path):
    p = tmp_path / "e.jsonl"; _write(p)
    _mutate(p, -1, lambda r: r.update(completion=False))
    with pytest.raises(EvidenceError, match="completion mismatch"): validate(p)


def test_observer_refuses_overwrite(tmp_path):
    p = tmp_path / "e.jsonl"; p.write_text("preserve me")
    with pytest.raises(FileExistsError): CorridorObserver(p, run_id="run", seed=1, environment="wcst")
