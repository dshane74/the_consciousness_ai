"""Independent fail-closed validator for native Corridor handoff evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = "consciousness-ai.native-boundary.v1"
REQUIRED = {"schema", "run_id", "event_id", "sequence", "environment", "episode",
            "cognitive_tick", "observation", "proposed_action", "action_selection",
            "dispatch", "result", "completion", "workspace_competition", "cognitive"}


class EvidenceError(ValueError):
    pass


def validate(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    raw = source.read_bytes()
    records = []
    seen = set()
    for line_no, line in enumerate(raw.splitlines(), 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EvidenceError(f"line {line_no}: malformed JSON: {exc}") from exc
        missing = REQUIRED - row.keys()
        if missing:
            raise EvidenceError(f"line {line_no}: missing {sorted(missing)}")
        if row["schema"] != SCHEMA:
            raise EvidenceError(f"line {line_no}: semantic schema mismatch")
        if row["event_id"] in seen:
            raise EvidenceError(f"line {line_no}: duplicate event_id")
        seen.add(row["event_id"])
        if row["sequence"] != len(records):
            raise EvidenceError(f"line {line_no}: sequence gap")
        if row["dispatch"] != {"boundary": "gymnasium.env.step", "call_count": 1}:
            raise EvidenceError(f"line {line_no}: unverifiable dispatch")
        if not {"terminated", "truncated", "observation", "reward"} <= row["result"].keys():
            raise EvidenceError(f"line {line_no}: incomplete result")
        if row["completion"] != bool(row["result"]["terminated"] or row["result"]["truncated"]):
            raise EvidenceError(f"line {line_no}: completion mismatch")
        if records:
            previous = records[-1]
            if (row["run_id"], row["environment"], row.get("seed")) != (
                    previous["run_id"], previous["environment"], previous.get("seed")):
                raise EvidenceError(f"line {line_no}: run semantic mismatch")
            if row["episode"] < previous["episode"]:
                raise EvidenceError(f"line {line_no}: episode went backwards")
            if row["episode"] == previous["episode"]:
                if previous["completion"]:
                    raise EvidenceError(f"line {line_no}: record crosses completed episode")
                if row["cognitive_tick"] != previous["cognitive_tick"] + 1:
                    raise EvidenceError(f"line {line_no}: cognitive tick gap")
                if row["observation"] != previous["result"]["observation"]:
                    raise EvidenceError(f"line {line_no}: observation/result linkage mismatch")
            elif row["episode"] != previous["episode"] + 1 or row["cognitive_tick"] != 0:
                raise EvidenceError(f"line {line_no}: reset/episode gap")
        elif row["cognitive_tick"] != 0:
            raise EvidenceError("first record is not tick zero")
        records.append(row)
    if not records:
        raise EvidenceError("empty evidence is not evaluable")
    return {"valid": True, "records": len(records), "runs": sorted({r["run_id"] for r in records}),
            "sha256": hashlib.sha256(raw).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.evidence), sort_keys=True))
    except EvidenceError as exc:
        raise SystemExit(f"INVALID: {exc}")


if __name__ == "__main__":
    main()
