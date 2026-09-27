# Source and configuration identity

* Executed source commit: `64a78cb985eceabc78918ca1a81cb9a5ce03dd18` (the clean merged fork HEAD available locally before changes).
* Experiment branch: `codex/natural-wcst-corridor-experiment`.
* Entry point: `python -m scripts.training.train_rlhf`.
* Native environment: `WCSTEnv`, 224x224, 60 trials, six correct sorts to switch, at most six rule changes, five feedback frames.
* Architecture configuration: merged defaults, action dimension 4, existence drive on, EI periodic calculation disabled, one episode, maximum loop bound 360.
* Seed/config identity: each event contains the seed, source commit and SHA-256 of parsed CLI arguments. Exact commands appear in per-run manifests.
* Evidence instrumentation was added after the execution-source commit and is part of this experiment commit; it observes native proposals and transitions and adds only the predeclared external refusal path.
