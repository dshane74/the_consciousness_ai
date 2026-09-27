import json

import numpy as np
import pytest

from corridor_evaluation.observer import CorridorObserver
from corridor_evaluation.validate import EvidenceError, validate


def _write(path, *, steps=2):
    observer = CorridorObserver(path, run_id="run", seed=7, environment="wcst")
    for step in range(steps):
        observer.record(
            episode=0, step=step, observation=np.full((2, 2, 3), step, dtype=np.uint8),
            observation_info={"rule": "shape"}, proposed_action=np.array([0.1, 0.9]),
            dispatched_action=1, action_source="policy_argmax",
            result_observation=np.full((2, 2, 3), step + 1, dtype=np.uint8), reward=1.0,
            terminated=step == steps - 1, truncated=False,
            result_info={"correct": True}, candidates={"vision": 0.8},
            winner="vision", cognitive={"prediction_error": 0.2},
        )
    observer.close()


def test_observer_and_validator_round_trip(tmp_path):
    evidence = tmp_path / "evidence.jsonl"
    _write(evidence)
    result = validate(evidence)
    assert result["valid"] is True
    assert result["records"] == 2
    first = json.loads(evidence.read_text().splitlines()[0])
    assert first["dispatch"]["boundary"] == "gymnasium.env.step"
    assert first["action_selection"]["diverged_from_policy"] is False


def test_validator_rejects_gap(tmp_path):
    evidence = tmp_path / "evidence.jsonl"
    _write(evidence)
    rows = evidence.read_text().splitlines()
    second = json.loads(rows[1])
    second["sequence"] = 4
    evidence.write_text(rows[0] + "\n" + json.dumps(second) + "\n")
    with pytest.raises(EvidenceError, match="sequence gap"):
        validate(evidence)


def test_observer_refuses_overwrite(tmp_path):
    evidence = tmp_path / "evidence.jsonl"
    evidence.write_text("preserve me")
    with pytest.raises(FileExistsError):
        CorridorObserver(evidence, run_id="run", seed=None, environment="dmts")
