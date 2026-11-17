---
id: computing-software.ai-ml-engineering.seldon-core-2.autoscaling-models-inference-lag
name: autoscaling-models-inference-lag
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, autoscaling, model-autoscaling, inference-lag, seldon-model-inference-lag-threshold, seldon-model-inactive-seconds-threshold, seldon-scaling-stats-period-seconds]
level: advanced
status: docs-checked
description: "Native Seldon Core 2 model autoscaling on inference lag: enable autoscalingModelEnabled, set minReplicas or maxReplicas, tune lag, inactivity and stats-period variables."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/scaling/core-autoscaling-models.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Native model autoscaling on inference lag

Enabled when Core 2 is installed with helm value `autoscaling.autoscalingModelEnabled` set to true (default false) and at least `minReplicas` or `maxReplicas` is set on the Model. The system then scales `replicas` within that range according to lag.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: tfsimple
spec:
  storageUri: "gs://seldon-models/triton/simple"
  requirements:
  - tensorflow
  memory: 100Ki
  minReplicas: 1
  replicas: 1
```

If only `replicas` is set, model autoscaling is disabled. Autoscaling never edits the original spec, so you cannot reset replicas to the initial number without first changing it to a different value.

## Logic
- Scale up: inference lag (incoming minus outgoing requests in a period) over the threshold `SELDON_MODEL_INFERENCE_LAG_THRESHOLD`, an inference server environment variable that applies to all models on that Server.
- Scale down: a model unused for `SELDON_MODEL_INACTIVE_SECONDS_THRESHOLD` seconds.
- Check frequency: agents compute stats every `SELDON_SCALING_STATS_PERIOD_SECONDS` and send scale requests to the scheduler.

The scheduler acts only if the model is stable (no state change in the last 5 minutes) and available, the desired count is in range (always at least 1 replica; overcommit reduces resources further), and for scale up without server autoscaling there are enough server replicas.

Pair this with native Server autoscaling; otherwise the needed servers may not start.

## Checked

2026-11-04. Confirmed against scaling/core-autoscaling-models.md (Seldon Core 2 docs, v2 branch): helm value and default, minReplicas/maxReplicas, three env vars, 5-minute stability rule. Removed or corrected: nothing.

Method: documentation only; no commands were run.
