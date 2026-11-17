---
id: computing-software.cloud-infrastructure-engineering.knative.progress-deadline
name: progress-deadline
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [progress-deadline, deployment-failed, slow-image-pull, revision-timeout]
level: practitioner
status: docs-checked
description: "Raise the deployment progress deadline for slow image pulls or cluster autoscaling."
sources:
  - https://knative.dev/docs/serving/configuration/deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop Revisions being marked failed while they are still starting.

The progress deadline is the maximum time you wait for the Deployment behind a Revision to progress before the system reports it failed. Default 600 seconds, expressed as a Go `time.Duration` string rounded to a second.

If the initial scale cannot be reached within the limit, the Knative Autoscaler scales the Revision to 0 and the Knative Service enters a terminal `Failed` state.

Raise it if:
- pulling the Service image is slow because the image is large;
- the Service takes a long time to become `READY`, for example from priming an initial cache;
- the cluster relies on cluster autoscaling to allocate resources for new pods.

Setting:
- Global key: `progress-deadline`, in `config-deployment` in `knative-serving`.
- Per-revision annotation: `serving.knative.dev/progress-deadline`.
- Value: a `time.Duration`.
- Default: `"600s"`.

```yaml
spec:
  template:
    metadata:
      annotations:
        serving.knative.dev/progress-deadline: "1200s"
```

Global form:

```yaml
data:
  progress-deadline: "1200s"
```

The page also shows an Operator form of the same global setting.

## Checked

2026-11-03. Confirmed on the Knative Serving configuration/deployment page: the progress-deadline key, annotation, 600s default, terminal Failed state and the three reasons to raise it. Removed: the progressDeadlineSeconds mapping sentence (not on the page).
Method: documentation only; no commands were run.
