"""Independent fail-closed validator for native Corridor handoff evidence."""
from __future__ import annotations

import argparse, hashlib, json, math
from pathlib import Path
from typing import Any

SCHEMA = "consciousness-ai.native-boundary.v2"
SOURCES = {"policy_argmax", "policy_continuous", "dmts_match_head_override"}
REQUIRED = {"schema", "run_id", "event_id", "sequence", "environment", "seed",
            "episode", "cognitive_tick", "reset", "identity", "causal", "observation",
            "proposed_action", "independent_argmax", "action_selection", "event_type",
            "dispatch", "result", "completion", "workspace_competition", "cognitive",
            "retry", "recovery", "alternative_path", "exception_channel"}


class EvidenceError(ValueError): pass


def _finite(value: Any) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, str): return True
    if isinstance(value, (int, float)): return math.isfinite(value)
    if isinstance(value, list): return all(_finite(v) for v in value)
    if isinstance(value, dict): return all(_finite(v) for v in value.values())
    return False


def validate(path: str | Path, *, require_complete: bool = True,
             expected_seed: int | None = None) -> dict[str, Any]:
    source, records, seen = Path(path), [], set()
    raw = source.read_bytes()
    for line_no, line in enumerate(raw.splitlines(), 1):
        try: row = json.loads(line)
        except json.JSONDecodeError as exc: raise EvidenceError(f"line {line_no}: malformed JSON") from exc
        missing = REQUIRED - row.keys()
        if missing: raise EvidenceError(f"line {line_no}: missing {sorted(missing)}")
        if row["schema"] != SCHEMA: raise EvidenceError(f"line {line_no}: semantic schema mismatch")
        if row["event_id"] in seen: raise EvidenceError(f"line {line_no}: duplicate event_id")
        seen.add(row["event_id"])
        if row["sequence"] != len(records): raise EvidenceError(f"line {line_no}: sequence gap")
        if row["cognitive_tick"] != row["sequence"]: raise EvidenceError(f"line {line_no}: cognitive tick gap")
        if expected_seed is not None and row["seed"] != expected_seed: raise EvidenceError("unexpected seed")
        proposal = row["proposed_action"]
        if not isinstance(proposal, list) or len(proposal) < 4 or not _finite(proposal):
            raise EvidenceError(f"line {line_no}: non-finite or incomplete proposal")
        argmax = max(range(4), key=lambda i: proposal[i])
        if row["independent_argmax"] != argmax: raise EvidenceError(f"line {line_no}: argmax mismatch")
        event_type, dispatch = row["event_type"], row["dispatch"]
        if dispatch.get("boundary") != "gymnasium.env.step": raise EvidenceError("unsupported boundary")
        if event_type == "dispatch":
            if dispatch.get("call_count") != 1 or dispatch.get("provenance") not in SOURCES:
                raise EvidenceError(f"line {line_no}: malformed or unsupported dispatch provenance")
            result = row["result"]
            if not isinstance(result, dict) or not {"terminated", "truncated", "observation", "reward", "info"} <= result.keys():
                raise EvidenceError(f"line {line_no}: dispatch without complete env.step result")
            if not _finite(result["reward"]): raise EvidenceError(f"line {line_no}: non-finite reward")
            if row["action_selection"]["dispatched_action"] != argmax and dispatch["provenance"] == "policy_argmax":
                raise EvidenceError(f"line {line_no}: dispatched argmax mismatch")
            if row["completion"] != bool(result["terminated"] or result["truncated"]):
                raise EvidenceError(f"line {line_no}: completion mismatch")
        elif event_type == "blocked_action":
            if dispatch != {"boundary": "gymnasium.env.step", "provenance": "corridor_action_refusal", "call_count": 0}:
                raise EvidenceError(f"line {line_no}: false block claim")
            if row["result"] is not None or row["action_selection"]["dispatched_action"] is not None:
                raise EvidenceError(f"line {line_no}: claimed block accompanied by dispatch/result")
            decision = row.get("boundary_decision", {})
            if decision.get("decision") != "refuse" or decision.get("state_before") != decision.get("state_after"):
                raise EvidenceError(f"line {line_no}: block lacks no-transition proof")
            if row["retry"].get("attempted") or row["recovery"].get("claimed") or row["alternative_path"].get("claimed"):
                raise EvidenceError(f"line {line_no}: fabricated retry/recovery/alternative path")
            if not row.get("condition_stop", {}).get("stopped"):
                raise EvidenceError(f"line {line_no}: blocked condition did not stop")
        else: raise EvidenceError(f"line {line_no}: unsupported event type")
        if records:
            prev = records[-1]
            keys = ("run_id", "environment", "seed", "episode", "identity")
            if any(row[k] != prev[k] for k in keys): raise EvidenceError(f"line {line_no}: mixed run, seed, episode, or identity")
            if prev["completion"]: raise EvidenceError(f"line {line_no}: record after completion")
            if row["causal"]["previous_event_id"] != prev["event_id"]:
                raise EvidenceError(f"line {line_no}: broken event linkage")
            expected = prev["result"]["observation"] if prev["result"] else None
            if row["causal"]["expected_observation"] != expected or row["observation"] != expected:
                raise EvidenceError(f"line {line_no}: observation/result linkage mismatch")
            if row["reset"]["episode_start"]: raise EvidenceError(f"line {line_no}: invalid reset continuity")
        else:
            if row["sequence"] != 0 or not row["reset"]["episode_start"] or row["causal"]["previous_event_id"] is not None:
                raise EvidenceError("invalid first reset")
        records.append(row)
    if not records: raise EvidenceError("empty evidence is not evaluable")
    blocked = records[-1]["event_type"] == "blocked_action"
    if blocked and require_complete: raise EvidenceError("baseline ended with blocked action")
    if not blocked and require_complete and not records[-1]["completion"]:
        raise EvidenceError("incomplete baseline: no termination/truncation")
    return {"valid": True, "records": len(records), "run_id": records[0]["run_id"],
            "seed": records[0]["seed"], "condition": "intervention" if blocked else "baseline",
            "complete": records[-1]["completion"], "sha256": hashlib.sha256(raw).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("evidence")
    parser.add_argument("--allow-blocked", action="store_true")
    args = parser.parse_args()
    try: print(json.dumps(validate(args.evidence, require_complete=not args.allow_blocked), sort_keys=True))
    except EvidenceError as exc: raise SystemExit(f"INVALID: {exc}")


if __name__ == "__main__": main()
