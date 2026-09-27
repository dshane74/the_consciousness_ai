# Natural WCST behavioral experiment — Corridor text handoff

## Executive result

Five independent, seeded baseline episodes reached **genuine native termination** after exactly 360 genuine `env.step` calls each. No run truncated, raised an observed transition exception, changed rule, completed a category, or showed proposed-versus-dispatched divergence. Trial accuracy ranged from 18.33% to 21.67%. In the separate seed-1701 intervention, the native proposal at zero-based sequence 5 was refused before dispatch: call count was zero, no result exists, and the pre/post state digest is identical. The native architecture exposes no retry/replan/reproposal interface, so the condition stopped and retry, recovery, and alternative-path behavior are unavailable.

This is an ordinary behavioral/action-boundary result. It is not a Corridor deep-detector result.

## Protocol and native endpoint

The pre-execution plan was frozen and SHA-256 hashed as `c1e923d9665372e2015136d257c43288d9304bcd43e12c6df5d7d5acae0b9c94` before execution. WCST evaluates one sort, then accepts five feedback-hold calls; the fifth increments the trial. Therefore 60 trials naturally terminate on transition 360 (sequence 359). Gymnasium `truncated` is always false in this environment. The loop bound was set to 360 so it did not pre-empt the native terminal transition.

## 1. Natural baseline outcomes by seed

| Seed | Steps | Correct / 60 | Accuracy | Reward | Rule changes | Categories | Perseverative errors | End |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1701 | 360 | 11 | 18.33% | -3.7 | 0 | 0 | 0 | terminated |
| 1702 | 360 | 11 | 18.33% | -3.7 | 0 | 0 | 0 | terminated |
| 1703 | 360 | 11 | 18.33% | -3.7 | 0 | 0 | 0 | terminated |
| 1704 | 360 | 12 | 20.00% | -2.4 | 0 | 0 | 0 | terminated |
| 1705 | 360 | 13 | 21.67% | -1.1 | 0 | 0 | 0 | terminated |

**Evidence status:** completion, rewards, correctness, and rule metrics are **supported by raw evidence**. Behavioral success at acquiring/switching a WCST rule is **contradicted** by zero category completions and zero rule changes. A broader learning-capability claim is **unsupported** by one episode per seed.

The 300 zero-reward transitions per run are the native five-frame feedback holds following each of 60 evaluated sorts; they are genuine calls, not duplicated or synthesized records.

## 2. Action-boundary intervention

The paired seed-1701 intervention matches the baseline design through sequence 4. At sequence 5 it captures the full native policy proposal and independently recomputed argmax, then records `corridor_action_refusal`, `call_count: 0`, no dispatched action, and `result: null`. The observation digest on both sides of the boundary decision is identical. The run stops at six records as preregistered.

**Evidence status:** refusal and absence of an environment transition are **supported by raw evidence**. A native retry mechanism is **not represented** in the action architecture; consequently retry, recovery, and alternative-path outcomes are **unavailable**, not failures and not fabricated negative behavior.

## 3. Proposed-versus-dispatched divergence

All 1,800 baseline transitions dispatched the independently recomputed argmax of the first four native policy-vector entries. Divergence count is zero for every baseline. The intervention's refusal is an explicit external boundary divergence, not a policy alternative and not a second-best action. Policy-vector projection is never labeled retry or alternative-path behavior.

## 4. Completion, failure, exceptions, retry, recovery, alternative paths

* **Completion:** supported for all baselines by `terminated=true` on sequence 359; intervention intentionally incomplete by task semantics.
* **Failure:** baseline behavioral rule acquisition is contradicted; execution/validation failure is contradicted by complete valid files.
* **Exceptions:** no per-transition native exception channel exists, explicitly recorded on each event; observed exceptions are unavailable rather than silently asserted false.
* **Retry / recovery / alternative path:** unavailable after refusal because there is no genuine native interface. No automatic fallback was dispatched.

## 5. Cross-seed consistency

All seeds agree on natural horizon, termination rather than truncation, no rule change/category completion/perseverative error, vision as the dominant workspace winner on nearly every step, and zero baseline action divergence. Correct trials vary only from 11 to 13. Initial rules genuinely differ: seed 1701 exposes color while 1702–1705 expose shape. Action distributions differ across seeds, so the files are not duplicated trajectories. These five episodes support consistency only for this default randomly initialized one-episode regime.

## 6. Native cognitive telemetry observations

The handoff preserves the already available workspace candidate bids/winner, conscious flag, ignition salience, reentrant-cycle value, RSSM `h`/`z` state digests, visual prediction-error proxy, critic value, and action-selection RPE input. Vision won 360/360, 354/360, 357/360, 359/360, and 350/360 steps for seeds 1701–1705 respectively; conscious flags have the same counts. Mean ignition salience was approximately 0.01233, 0.00384, 0.00218, 0.01144, and 0.01272.

These are descriptions of native cognitive telemetry only. They do not establish Corridor semantics, consciousness, causal recovery, or deep-detector findings.

## 7. Deep-detector representation status

| Construct | Represented in evidence? | Invoked? | Status |
|---|---|---|---|
| FS1 | No | No | **not represented** |
| FS2 | No | No | **not represented** |
| Invariant Persistence | No | No | **not represented** |
| T_pred | No | No | **not represented** |
| Falsification debt | No | No | **not represented** |
| Unresolved questions | No | No | **not represented** |
| Hypothesis weights | No | No | **not represented** |

No placeholder fields were created, no longer horizon was requested for these constructs, and no apparent compatibility was accepted.

## 8. Validation and integrity

The independent validator recomputes argmax, enforces finite values and identity/sequence/reset/observation chains, validates dispatch provenance and complete Gym results, distinguishes zero-call blocks, rejects fabricated recovery claims, and requires terminal completion for baselines. All six evidence files pass. Per-file validation JSON and run manifests accompany the evidence. `SHA256SUMS` inventories every committed handoff file except itself.

## 9. Limitations and unsupported conclusions

* The environment exposes its hidden active rule in `info`; this is recorded as native provenance but is not directly passed as a privileged policy input by the observed loop.
* One episode per seed tests untrained/default within-episode behavior, not long-run training or checkpoint performance.
* No category was completed, so rule-switch adaptation and perseverative-error recovery have **insufficient evidence** rather than demonstrated absence as an architectural capacity.
* The observer proves the intervention branch made zero `env.step` calls by control flow plus zero-call/no-result/state-identity evidence; it does not monkey-patch an independent call counter inside Gymnasium.
* The proposal is preserved losslessly as JSON numeric values, while large recurrent tensors are represented by shape/type/SHA-256 digests to keep the handoff text-only.
* Native execution produced model/session binary artifacts in `/tmp`; they are not committed and are itemized with sizes/hashes in `EXCLUDED_BINARY_ARTIFACTS.tsv`.
* Remote refresh was blocked by the environment's HTTPS proxy. The clean local merged HEAD was used; see `DEVIATIONS.md`.
* No conclusion about Corridor FS1, FS2, Invariant Persistence, consciousness, hypothesis adjudication, or alternate-path competence is supported.
