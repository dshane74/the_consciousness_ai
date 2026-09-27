"""Append-only capture of genuine native environment action boundaries."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

import numpy as np


def _plain(value: Any) -> Any:
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
    array = np.asarray(value)
    contiguous = np.ascontiguousarray(array)
    return {"sha256": hashlib.sha256(contiguous.tobytes()).hexdigest(),
            "dtype": str(array.dtype), "shape": list(array.shape)}


class CorridorObserver:
    """Create-exclusive writer: one event per dispatch or explicit refusal."""

    schema = "consciousness-ai.native-boundary.v2"

    def __init__(self, path: str | os.PathLike[str], *, run_id: str, seed: int | None,
                 environment: str, config_identity: str | None = None,
                 source_identity: str | None = None) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.run_id, self.seed, self.environment = run_id, seed, environment
        self.config_identity, self.source_identity = config_identity, source_identity
        self._handle = self.path.open("x", encoding="utf-8")
        self._sequence = 0
        self._previous_event_id = None
        self._previous_post = None

    def _base(self, episode: int, step: int, observation: Any,
              observation_info: dict[str, Any] | None, proposed_action: Any,
              action_source: str) -> dict[str, Any]:
        proposal = np.asarray(proposed_action, dtype=float).reshape(-1)
        action_count = 4 if self.environment == "wcst" else len(proposal)
        argmax = int(np.argmax(proposal[:action_count]))
        event_id = f"{self.run_id}:e{episode}:s{step}"
        before = digest(observation)
        return {
            "schema": self.schema, "run_id": self.run_id, "event_id": event_id,
            "sequence": self._sequence, "environment": self.environment,
            "seed": self.seed, "episode": episode, "cognitive_tick": step,
            "reset": {"episode_start": step == 0, "reset_id": f"{self.run_id}:e{episode}"},
            "identity": {"config_sha256": self.config_identity,
                         "source_commit": self.source_identity},
            "causal": {"previous_event_id": self._previous_event_id,
                       "expected_observation": self._previous_post},
            "observation": before, "observation_info": _plain(observation_info or {}),
            "proposed_action": _plain(proposed_action),
            "independent_argmax": argmax,
            "action_selection": {"source": action_source},
            "exception_channel": {"available": False,
                                  "reason": "native loop has no per-transition exception channel"},
        }

    def _write(self, row: dict[str, Any], post: dict[str, Any] | None) -> None:
        self._handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        self._handle.flush()
        os.fsync(self._handle.fileno())
        self._sequence += 1
        self._previous_event_id = row["event_id"]
        self._previous_post = post

    def record(self, *, episode: int, step: int, observation: Any,
               observation_info: dict[str, Any] | None, proposed_action: Any,
               dispatched_action: Any, action_source: str, result_observation: Any,
               reward: float, terminated: bool, truncated: bool,
               result_info: dict[str, Any] | None, candidates: dict[str, float],
               winner: str | None, cognitive: dict[str, Any]) -> None:
        row = self._base(episode, step, observation, observation_info,
                         proposed_action, action_source)
        post = digest(result_observation)
        row.update({
            "event_type": "dispatch",
            "action_selection": {"source": action_source,
                                 "dispatched_action": _plain(dispatched_action),
                                 "diverged_from_policy": int(dispatched_action) != row["independent_argmax"]},
            "dispatch": {"boundary": "gymnasium.env.step", "provenance": action_source,
                         "call_count": 1},
            "result": {"observation": post, "reward": float(reward),
                       "terminated": bool(terminated), "truncated": bool(truncated),
                       "info": _plain(result_info or {})},
            "completion": bool(terminated or truncated),
            "workspace_competition": {"candidates": {str(k): float(v) for k, v in candidates.items()},
                                      "winner": winner},
            "cognitive": _plain(cognitive),
            "retry": {"available": False, "attempted": False,
                      "reason": "no native retry path"},
            "recovery": {"available": False, "claimed": False},
            "alternative_path": {"available": False, "claimed": False},
        })
        self._write(row, post)

    def record_block(self, *, episode: int, step: int, observation: Any,
                     observation_info: dict[str, Any] | None, proposed_action: Any,
                     action_source: str, candidates: dict[str, float], winner: str | None,
                     cognitive: dict[str, Any], reason: str) -> None:
        row = self._base(episode, step, observation, observation_info,
                         proposed_action, action_source)
        row.update({
            "event_type": "blocked_action",
            "action_selection": {"source": action_source, "dispatched_action": None,
                                 "diverged_from_policy": True},
            "boundary_decision": {"decision": "refuse", "reason": reason,
                                  "state_before": row["observation"],
                                  "state_after": row["observation"]},
            "dispatch": {"boundary": "gymnasium.env.step", "provenance": "corridor_action_refusal",
                         "call_count": 0},
            "result": None, "completion": False,
            "workspace_competition": {"candidates": {str(k): float(v) for k, v in candidates.items()},
                                      "winner": winner},
            "cognitive": _plain(cognitive),
            "retry": {"available": False, "attempted": False,
                      "reason": "native architecture exposes no retry/replan/reproposal interface"},
            "recovery": {"available": False, "claimed": False},
            "alternative_path": {"available": False, "claimed": False},
            "condition_stop": {"reason": "refusal_without_native_retry", "stopped": True},
        })
        self._write(row, None)

    def close(self) -> None:
        if not self._handle.closed:
            self._handle.close()

    def __enter__(self) -> "CorridorObserver": return self
    def __exit__(self, *_: object) -> None: self.close()
