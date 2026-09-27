# Corridor evaluation and fail-closed handoff

## 1. Repository and run identity

The frozen starting point was branch `work`, commit `4fedd5ee293d4eff49831a05dffef1811299c823`, with a clean initial status. This checkout has no configured Git remote; the project advertises `https://github.com/tlcdv/the_consciousness_ai.git`, so that URL is recorded as advertised rather than verified checkout provenance. The license is the repository's non-commercial, attribution-required license. Dependencies are declared in `requirements.txt`; the executed host used Python 3.12.13, Torch 2.14.0+cu130, three logical CPUs, and no CUDA. No checkpoint files were present. The exact command, configuration, seed, hardware, and start commit are in `corridor_run/run_manifest.json`.

Available runnable environments are Dark Room, Navigation, DMTS, and WCST. Existing reproducible artifacts were the three CSV DQN baselines in `runs_baseline/` (Dark Room 1,000 episodes; DMTS and WCST 500 each). Repository size was 26 MiB before the new evidence package. The bounded run took 12.346 seconds and its package is about 34 KiB; a 200-step CPU run is consequently expected to take roughly 3–5 minutes and tens to hundreds of KiB for these evidence surfaces (an estimate, not a benchmark). Full training depends on episode count and optional models and can require the documented GPU/weight storage.

## 2. Selected baseline

Exactly one initial baseline was selected: **WCST, seed 1701, one bounded episode of 10 genuine steps**. WCST exposes stable trials, hidden rule changes, discrete native action identifiers, error monitoring, and inhibition-relevant policy machinery. That gives a better joint opportunity for ordinary action-boundary analysis and legitimate hypothesis/falsification admission analysis than Dark Room's continuous movement or DMTS's primarily perceptual working-memory cycle. It was not selected by metric volume. DMTS, Dark Room, and their existing CSV runs were inventoried but not executed, avoiding repeated short traces masquerading as a detector horizon.

## 3. External action/runtime evidence inventory

The observer records the observation digest and pre-step info, raw continuous policy proposal, native discrete projection, explicit downstream override source when present, the single `gymnasium.env.step` dispatch, returned observation digest/reward/termination/truncation/info, completion, workspace bids/winner, cognitive tick, episode, run/event/sequence identifiers, and provenance. Raw arrays used as actions are preserved; large image and recurrent tensors are represented by dtype, shape, and SHA-256 rather than invented scalar summaries. Missing constructs are omitted or explicitly marked unavailable; they are never zero-filled.

The code trace is: environment reset → observation processing → specialist bid construction → recurrent workspace settling → policy proposal → discrete argmax (and, only in configured DMTS choice mode, match-head override) → exactly one `env.step` → result and learning. The executed WCST trace contains 10 linked records, no override divergence, no termination/truncation within the bound, no retry path, and no alternative action after dispatch. Argmax is a native representation conversion, not a divergence.

A Gymnasium dispatch is demonstrably the genuine causal external-effect boundary for this architecture: it consumes the selected native action and synchronously yields the result used by learning. **It is not thereby proven equivalent to a Corridor tool call.** Tool-call equivalence depends on Corridor's canonical action-boundary admission semantics. Without those definitions, the handoff preserves `gymnasium.env.step` as itself and does not rename it.

## 4. Ordinary Corridor evaluation results

**Result: NOT RUN / UNAVAILABLE, fail-closed.** No authoritative Corridor checkout, runner, adapter, classifier, report generator, prior-agent protocol, or tests were found under `/workspace`, `/root`, or `/opt`. Recreating its evidence classes, divergence meanings, non-evaluation format, or thresholds would violate the requirement. The native observer and validated immutable package were completed for handoff. This non-evaluation is independent of detector availability and is not an ordinary-evaluation failure verdict.

## 5. Divergence findings

Native mapping distinguishes proposal, representation projection, optional policy override, and dispatch. All 10 WCST steps used `policy_argmax`; therefore native override divergence was **0/10**. The raw vector necessarily differs in representation from the integer, but that is not classified as behavioral divergence. No Corridor divergence classification is asserted.

## 6. Task completion and retry findings

The bounded run returned total reward `-0.5771501002899342`, zero correct trials, zero rule changes, and zero consecutive correct responses. It reached the configured 10-step bound without native `terminated` or `truncated`; it therefore supplies no task-completion claim. The loop has no retry-after-result construct and dispatched once per tick. A later episode step is not a retry. No alternative-path behavior occurred. The ethics precondition was independently observed to fail closed when `--existence-drive` was omitted; the recorded run explicitly selected `on`.

## 7. Evidence availability and limitations

Available evidence establishes causal/temporal linkage, episode/tick ordering, native action IDs, policy-to-dispatch mapping, returned effects, bids/winner, and recurrent state continuity hashes. It does not expose a pre-dispatch ethical gate in this executed training path, per-path Go/No-Go/STN tensors, retry intent, a natural-language task instruction, or a success predicate beyond environment fields. The observer is isolated and has no control-flow or tensor mutation. The independent validator rejects empty, malformed, missing-field, duplicated, sequence-gapped, tick-gapped, backward/reset-crossing, dispatch-mismatched, and completion-mismatched records.

## 8. Deep cognitive telemetry inventory

Genuine telemetry includes stable specialist identities (`vision`, `audio`, `memory`, `body`, `semantic`), raw per-tick bids, actual workspace winner, consciousness/ignition values, recurrent RSSM `h_state`/`z_state` identity hashes and shapes, the native vision surprise bid, critic value, policy-selection RPE input, cognitive tick, episode reset, returned reward, and run provenance. The architecture also applies learning after results, but this observer does not yet capture parameter-delta hashes or optimizer-step identities.

Specialist identity is not assumed to be hypothesis identity. Vision surprise is not assumed to be a committed prediction error. RSSM state continuity is not assumed to expose prediction commitment/resolution. A literal `rpe_used_for_selection` of 0.0 is recorded because that is the executed call argument, not as evidence of later reward qualification/application. No unresolved-question ledger, contradiction identity, failed-hypothesis record, or falsification-debt-like lifecycle was found in the executed path.

## 9. FS1 admission and result/non-invocation

- `invoked: false`
- Status: **blocked (semantically mismatched and unexposed evidence)**.
- Missing: authoritative FS1 definition/implementation plus stable native hypothesis identities with genuine lifecycle transitions, commitment timing, resolution/falsification outcomes, and verified causal linkage.
- The workspace has stable *specialist* labels and bids, but treating them as hypotheses would change meaning.
- Required: Corridor itself and either already-native hypothesis lifecycle records or an observer-only exposure of such existing objects. New architectural hypotheses must not be added for admission.

## 10. FS2 admission and result/non-invocation

- `invoked: false`
- Status: **blocked (construct absent/unexposed and canonical detector unavailable)**.
- Missing: authoritative FS2 definition/implementation, persistent unresolved/contradiction/failure identities, weight updates tied to evidence, and any canonical falsification-debt qualification semantics.
- Candidate bids are per-tick competition values, not proven belief confidence or debt.
- Required: the canonical implementation and genuine persistent native records satisfying its schema and timing; naming an existing scalar “confidence” is insufficient.

## 11. Invariant Persistence admission and result/non-invocation

- `invoked: false`
- Status: **blocked (semantically insufficient evidence and detector unavailable)**.
- Missing: authoritative implementation/threshold/horizon, identified invariant commitments, value observations over the required uninterrupted horizon, resolution events, reset rules, and parameter-update provenance.
- RSSM state hashes demonstrate recurrent continuity but not invariant content or prediction identity.
- Required: native commitment identity/content and resolution telemetry over one genuine run of the detector's required length. Short traces must not be repeated to manufacture a horizon.

## 12. Frozen findings compared with upstream diagnoses

The machine-readable freeze is `docs/corridor/frozen_findings.json`. A repository overview containing developer-written diagnoses was displayed before the freeze, so independence cannot honestly be claimed; this is recorded as a protocol limitation rather than concealed. Comparisons are therefore conservative:

- **ALREADY_KNOWN:** the overview documents an appraisal call failure; the bounded run reproduced the missing-`goal_vector` warning.
- **INDEPENDENTLY_CONFIRMED:** none claimed because the required pre-diagnosis freeze was contaminated.
- **PARTIALLY_KNOWN:** RSSM recurrence and workspace competition are implemented and observed, but neither establishes Corridor prediction/hypothesis semantics.
- **POTENTIALLY_NOVEL:** none claimed from a 10-step bounded run.
- **UNSUPPORTED:** any claim that Gym actions automatically equal tool calls; that specialist bids are hypothesis confidences; that recurrent hashes are persistent invariants; or that any deep detector passed/failed.

Alternatives, confidence, and falsification tests are preserved in the freeze file.

## 13. Evidence paths and hashes

- `corridor_run/native_evidence.jsonl`: canonical native boundary trace; SHA-256 `bd98c3c08838ae62cd72fbce2bdb155056ad00286f62b628b8f5b76c5b0abc95`.
- `corridor_run/run_manifest.json`: run/repository/platform identity.
- `corridor_run/SHA256SUMS`: hashes for every retained evidence, metrics, manifest, and report artifact.
- `corridor_run/EXCLUDED_BINARY_ARTIFACTS.tsv`: original path, byte size, and SHA-256 for generated binary telemetry intentionally excluded from Git. Its recorded hash preserves provenance without adding the binary to the PR.
- `corridor_run/metrics/`: retained native episode, environment, step, and ethics text records. The generated NumPy broadcast array is documented in the exclusion manifest.
- `docs/corridor/frozen_findings.json`: pre-comparison mapping/admission record, including the contamination limitation.

## 14. Tests and results

The observer/validator tests passed (round trip, gap rejection, overwrite refusal). Python compilation passed. The validator accepted exactly 10 records and produced the evidence hash above. The bounded WCST command completed successfully with a known appraisal warning. A deliberate first invocation without the mandatory existence-drive declaration failed closed before execution, as designed.

## 15. Exact files changed

- `scripts/training/train_rlhf.py`: optional observer wiring at the genuine selection/dispatch/result boundary.
- `corridor_evaluation/__init__.py`, `observer.py`, `validate.py`: isolated capture and independent fail-closed validation.
- `tests/test_corridor_evidence.py`: observer and negative validator tests.
- `docs/corridor/evaluation_report.md`, `docs/corridor/frozen_findings.json`: report and frozen mapping.
- `corridor_run/*`: bounded immutable text handoff evidence, manifest, hashes, native text metrics, and the binary-exclusion manifest.
- `.gitignore`: narrowly excludes reproducible `corridor_run/metrics/*.npy` telemetry.

## 16. Remaining handoff requirements

Provide the authoritative Corridor repository/commit and the exact prior external-agent experiment invocation/configuration. Run its unmodified ordinary runner/classifiers/reporting against this package only if its adapter formally admits a Gymnasium effect boundary; otherwise emit its canonical unavailable item. Then run each canonical detector's admission separately. If a detector requires currently unexposed but genuinely existing telemetry, extend only this observer and validator, rerun one natural uninterrupted horizon, hash it, and invoke the unmodified detector. Do not infer detector results from this report, modify thresholds, reinterpret bids/states, or combine ordinary and deep outcomes into one pass/fail.
