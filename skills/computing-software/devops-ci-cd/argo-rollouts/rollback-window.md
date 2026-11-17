---
id: computing-software.devops-ci-cd.argo-rollouts.rollback-window
name: rollback-window
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [rollbackwindow, rollback, fast-track, revisionhistorylimit, analysis, steps, argo-rollouts]
level: advanced
status: docs-checked
description: "Fast-track rollbacks to recent revisions by skipping steps and analysis with rollbackWindow."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/rollback/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available for blue-green and canary since v1.4. By default, re-applying an older Rollout manifest is treated like any spec change: the full list of steps runs, with analysis. There are two exceptions: the controller detects it is moving back to a blue-green ReplicaSet that still exists and is scaled up (within its `scaleDownDelay`), and it detects a return to the canary stable ReplicaSet before the upgrade completed.

When you want to roll back as fast as possible, a rollback window marks how many recent revisions can be reached without re-running steps and analysis:

```yaml
spec:
  rollbackWindow:
    revisions: 3
  revisionHistoryLimit: 5
```

With a linear history 1, 2, 3, 4, 5 (current), a rollback from 5 to 4 or 3 falls inside the window with `revisions: 3` and is fast tracked, skipping all steps.

The related `kubectl argo rollouts undo NAME --to-revision=N` rolls back to a given revision (default: the last one).

Consider the trade-off: skipping analysis on rollback is usually right because you are returning to a known-good version, but only if that version is still compatible with current data and dependencies.

Verify by rolling back within the window and observing no pause or analysis in `kubectl argo rollouts get rollout NAME -w`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/rollback/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_undo/.

Removed or corrected: the claim that rolling back to revisions 2 or 1 runs normal steps and the revisionHistoryLimit advice.

Method: documentation only; no commands were run.
