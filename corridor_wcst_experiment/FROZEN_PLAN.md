# Frozen natural-WCST Corridor evidence plan

**Status:** pre-execution; immutable after hashing. **Date:** 2026-09-27.

## Inspected native semantics

The merged `train_rlhf` loop resets WCST once per episode, clears RSSM/PFC/gate/TPM episode state, obtains the native policy vector from `ActionSelectionCore.select_action`, projects the first four entries with NumPy `argmax`, and ordinarily calls `env.step` exactly once. WCST has 60 trials, five feedback-hold steps after every evaluated sort, and terminates only when the fifth hold step after trial 60 increments the trial counter to 60. It never emits truncation. Thus a naturally terminating episode requires exactly 360 action boundaries. The training-loop `--max-steps` range bound is otherwise an external truncation-by-loop (with no Gymnasium `truncated=True`); for this experiment it is frozen to the native natural horizon, 360.

## Frozen design

* Baseline seeds: **1701, 1702, 1703, 1704, 1705**, one independent run and one complete natural episode apiece.
* Configuration: native merged WCST, 224x224 RGB, 60 trials, `correct_to_switch=6`, `max_rule_changes=6`, `feedback_duration=5`; `train_rlhf`, one episode, `--max-steps 360`, default architecture/config except evidence capture, EI disabled, CPU where available.
* Baseline completion: final genuine `env.step` reports `terminated=true` or `truncated=true`; for this environment the expected native result is termination at sequence 359. Failure: exception; non-finite proposal/reward; malformed transition; no terminal/truncated result by the frozen horizon; or validator rejection.
* Intervention: a separate seed-1701 run with identical configuration. At zero-based **sequence 5**, after the full native proposal and independent argmax are available, an external `corridor_action_refusal` blocks dispatch. No `env.step` may occur, the before/after observation and native state identity must match, and a blocked-event record must contain no step result. The architecture is then inspected for an explicit retry/replan/reproposal interface. If none exists, record retry/recovery/alternative path as unavailable and stop immediately. Never dispatch a second-ranked action or treat projection as retry/divergence.
* Stop conditions: baseline stops only on native `terminated`/`truncated`, exception, or frozen horizon exhaustion; intervention stops at the blocked event absent a genuine retry mechanism.

## Frozen evidence contract

Append-only, create-exclusive UTF-8 JSONL, schema `consciousness-ai.native-boundary.v2`, one file per condition. Every event carries run/episode/seed/config/source identity; contiguous sequence and cognitive tick; reset marker/identity; pre-observation hash; full finite native proposal; independently recomputed argmax; proposed and dispatched actions; supported provenance; workspace candidates/winner and recurrent-state digests; exception-channel status; and previous-event/observation causal linkage. Dispatch records additionally carry exactly-one-call proof, complete Gymnasium result, post-observation hash, finite reward, terminal flags, exposed WCST info and completion. The one block record carries decision/reason, zero-call proof, identical pre/post state identity, absent step result, and explicit retry/recovery/alternative-path availability.

Manifests identify command/config/source and outcomes. SHA-256 inventory covers all handoff text. Independent validation rejects gaps/duplicates/reversal; mixed identities; invalid reset or linkage; non-finite values; unsupported provenance; policy/argmax mismatch; incomplete results; block-with-result; dispatch-without-result; fabricated retry/recovery/alternative path; completion mismatch; evidence overwrite; and incomplete baselines. Native binary output, if any, is excluded and listed rather than committed.

## Interpretation boundary

This is behavioral/action-boundary evidence. Native telemetry remains native telemetry. FS1, FS2, Invariant Persistence, T_pred, falsification debt, unresolved questions, and hypothesis weights are neither populated nor invoked. FS1/FS2/Invariant Persistence representation and invocation are reported separately. No detector compatibility is inferred from field names or horizon length.
