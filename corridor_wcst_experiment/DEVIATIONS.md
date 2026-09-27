# Execution deviations

The frozen scientific design was not revised. Two operational events occurred:

1. The first launch omitted the ethics framework's mandatory `--existence-drive` declaration and stopped before observer creation or any environment action. All executed conditions used `--existence-drive on`; manifests record the exact commands.
2. Seeds 1702–1705 were initially launched concurrently. CPU oversubscription made progress impractical, so those processes were stopped while their files were incomplete, the incomplete non-handoff files were removed, and each seed was restarted from its declared initial seed/config. The committed create-exclusive evidence files are the restarted complete runs. `OMP_NUM_THREADS=1` and `MKL_NUM_THREADS=1` were operational scheduling controls and did not change the frozen model/environment configuration.

A fetch of `origin/main` was attempted before branching but the environment's HTTPS CONNECT proxy returned 403. The clean checked-out HEAD was the repository's existing merged main commit `64a78cb985eceabc78918ca1a81cb9a5ce03dd18`; execution source identity in every event records that commit. No claim is made that the remote was independently refreshed.
