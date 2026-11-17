---
id: computing-software.cloud-infrastructure-engineering.keda.scaledjob-replica-counts-and-history
name: scaledjob-replica-counts-and-history
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [maxreplicacount, minreplicacount, successfuljobshistorylimit, failedjobshistorylimit, scaledjob-limits, envsourcecontainername]
level: practitioner
status: docs-checked
description: "Size a ScaledJob: how maxReplicaCount caps jobs per polling period, how minReplicaCount keeps warm jobs, and how history limits clean up."
sources:
  - https://keda.sh/docs/2.17/reference/scaledjob-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`maxReplicaCount` (default 100) is the maximum number of Jobs created within a single polling period, with currently running Jobs deducted. The page's table: queue length 10, max 3, target average value 1, no running jobs creates 3; with one running job it creates 2; with max 100 it creates 10; queue length 4 with target 5 creates 1. "Target Average Value" is the messages one job consumes, defined on the scaler side (for example `queueLength` on the Azure Storage Queue scaler).

`minReplicaCount` (default 0) is how many Jobs are always created, which avoids bootstrapping delay. If it exceeds `maxReplicaCount` it is lowered to `maxReplicaCount`. With min 2 and a target value of 1, three new messages create three more Jobs, even though two of those messages are processed by the already running Jobs, to satisfy the minimum.

`successfulJobsHistoryLimit` and `failedJobsHistoryLimit` (both default 100) say how many finished Jobs are retained, similar to Kubernetes Jobs history limits. The count may briefly exceed the limit; cleanup runs on the same schedule as `pollingInterval`.

`envSourceContainerName` defaults to the first container in `jobTargetRef.template.spec.containers`. `pollingInterval` defaults to 30 seconds.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledJob specification: maxReplicaCount table, minReplicaCount behaviour, history limits and cleanup period. Reworded two explanations to match the page.

Method: documentation only; no commands were run.
