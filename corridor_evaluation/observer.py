"""Append-only, observer-only capture of the native training-loop boundary.

This module deliberately does not assign Corridor classifications.  In particular,
Gymnasium actions are recorded as environment dispatches, not renamed tool calls.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

import numpy as np


def _plain(value: Any) -> Any:
    """Convert genuine values to JSON values; never manufacture absent values."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if hasattr(value, "detach"):
        return value.detach().cpu().numpy().tolist()
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return repr(value)


def digest(value: Any) -> dict[str, Any]:
    """Lossless shape/type provenance plus a digest, avoiding huge image records."""
    array = np.asarray(value)
    contiguous = np.ascontiguousarray(array)
    return {
        "sha256": hashlib.sha256(contiguous.tobytes()).hexdigest(),
        "dtype": str(array.dtype),
        "shape": list(array.shape),
    }


class CorridorObserver:
    """Writes one causally complete record per real ``env.step`` call."""

    schema = "consciousness-ai.native-boundary.v1"

    def __init__(self, path: str | os.PathLike[str], *, run_id: str, seed: int | None,
                 environment: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id
        self.seed = seed
        self.environment = environment
        self._handle = self.path.open("x", encoding="utf-8")
        self._sequence = 0

    def record(self, *, episode: int, step: int, observation: Any,
               observation_info: dict[str, Any] | None, proposed_action: Any,
               dispatched_action: Any, action_source: str, result_observation: Any,
               reward: float, terminated: bool, truncated: bool,
               result_info: dict[str, Any] | None, candidates: dict[str, float],
               winner: str | None, cognitive: dict[str, Any]) -> None:
        event_id = f"{self.run_id}:e{episode}:s{step}"
        record = {
            "schema": self.schema,
            "run_id": self.run_id,
            "event_id": event_id,
            "sequence": self._sequence,
            "environment": self.environment,
            "seed": self.seed,
            "episode": episode,
            "cognitive_tick": step,
            "observation": digest(observation),
            "observation_info": _plain(observation_info or {}),
            "proposed_action": _plain(proposed_action),
            "action_selection": {
                "source": action_source,
                "dispatched_action": _plain(dispatched_action),
                # Argmax is the documented native discrete-action projection, not
                # a divergence.  Only an explicit downstream override is one.
                "diverged_from_policy": action_source.endswith("_override"),
            },
            "dispatch": {"boundary": "gymnasium.env.step", "call_count": 1},
            "result": {
                "observation": digest(result_observation),
                "reward": float(reward),
                "terminated": bool(terminated),
                "truncated": bool(truncated),
                "info": _plain(result_info or {}),
            },
            "completion": bool(terminated or truncated),
            "workspace_competition": {
                "candidates": {str(k): float(v) for k, v in candidates.items()},
                "winner": winner,
            },
            "cognitive": _plain(cognitive),
            # The native loop dispatches exactly once and has no retry construct.
            "retry": {"available": False, "reason": "no native retry path"},
        }
        self._handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        self._handle.flush()
        os.fsync(self._handle.fileno())
        self._sequence += 1

    def close(self) -> None:
        if not self._handle.closed:
            self._handle.close()

    def __enter__(self) -> "CorridorObserver":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
