---
id: computing-software.devops-ci-cd.argo-rollouts.rollout-timing-and-history-fields
name: rollout-timing-and-history-fields
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [minreadyseconds, revisionhistorylimit, progressdeadlineseconds, paused, restartat, rollout-spec, argo-rollouts]
level: practitioner
status: docs-checked
description: "Set the Rollout spec fields that control readiness, history, progress deadline, manual pause and restart."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Several top-level `Rollout` fields behave like their Deployment counterparts, with a few extras.

- `replicas`: desired pods, default 1.
- `minReadySeconds`: seconds a new pod must be ready with no crashing container to count as available; default 0.
- `revisionHistoryLimit`: old ReplicaSets retained; default 10.
- `progressDeadlineSeconds`: maximum time a rollout must make progress before it is considered failed; default 600. The controller keeps processing failed rollouts and surfaces a `ProgressDeadlineExceeded` condition. Progress is not estimated while paused.
- `progressDeadlineAbort`: set true to abort the update when the deadline is exceeded; default false.
- `paused`: manual pause. The rollout will not advance through steps while paused, but HPA scaling still occurs. Normally controlled by `kubectl argo rollouts pause`, not set in the manifest. If true at creation, replicas are not scaled up from zero until manually promoted.
- `restartAt`: UTC timestamp for sequentially restarting all pods; written by `kubectl argo rollouts restart`.
- `rollbackWindow.revisions`: see the rollback-window skill.
- `analysis.successfulRunHistoryLimit` and `unsuccessfulRunHistoryLimit`: AnalysisRun/Experiment history; both default 5, and unsuccessful covers Error, Failed and Inconclusive.

```yaml
spec:
  minReadySeconds: 30
  progressDeadlineSeconds: 600
  progressDeadlineAbort: true
  analysis:
    unsuccessfulRunHistoryLimit: 10
```

Verify with `kubectl describe rollout NAME` conditions.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: nothing; every field and default matched the specification page.

Method: documentation only; no commands were run.
