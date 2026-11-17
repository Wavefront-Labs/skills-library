---
id: computing-software.cloud-infrastructure-engineering.keda.scaledjob-scaling-strategies
name: scaledjob-scaling-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [scalingstrategy, accurate, eager, custom, pendingpodconditions, multiplescalerscalculation]
level: advanced
status: docs-checked
description: "Pick a ScaledJob scalingStrategy (default, custom, accurate, eager) and set multipleScalersCalculation for several triggers."
sources:
  - https://keda.sh/docs/2.17/reference/scaledjob-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.scalingStrategy.strategy` selects how many Jobs to create per poll. Define `maxScale = min(maxReplicaCount, ceil(queueLength / targetAverageValue))`, with `runningJobCount` being unfinished Jobs and `pendingJobCount` those not yet running.

- `default`: create `maxScale - runningJobCount`.
- `custom`: needs `customScalingQueueLengthDeduction` and `customScalingRunningJobPercentage`; creates `min(maxScale - deduction - int(runningJobCount * percentage), maxReplicaCount)`. Without these parameters it behaves as `default`.
- `accurate`: recommended when the scaler's `queueLength` excludes locked (in-flight) messages, as Azure Storage Queue does and when your app deletes a message once consumed. It returns `maxReplicaCount - runningJobCount` if `maxScale + runningJobCount` exceeds the maximum, otherwise `maxScale - pendingJobCount`.
- `eager`: fills every free slot up to `maxReplicaCount`. With `maxReplicaCount: 10`, jobs running 3 hours and 3 messages sent twice, `default` ends with 3 running Jobs for 6 queued messages while `eager` ends with 6.

`pendingPodConditions` (for example `Ready`, `PodScheduled`) redefines a pending Job as one whose listed conditions are not all true.

`multipleScalersCalculation` (default `max`; also `min`, `avg`, `sum`) says which scaler's `queueLength` and `maxScale` to use when several triggers exist; `avg` sums the active scalers and divides by their count.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledJob specification: strategies and formulas, accurate and eager descriptions, pendingPodConditions, multipleScalersCalculation values.

Method: documentation only; no commands were run.
