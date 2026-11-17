---
id: computing-software.ai-ml-engineering.kserve.kserve-kpa-autoscaling
name: kserve-kpa-autoscaling
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [kpa, knative-pod-autoscaler, scale-to-zero, minreplicas, containerconcurrency, concurrency, qps, rps, panic-mode, autoscalingknativedevtarget, scale-from-zero]
level: practitioner
status: docs-checked
description: "Knative Pod Autoscaler: scaleMetric concurrency/rps/cpu/memory, scaleTarget soft limit, containerConcurrency hard limit, minReplicas 0 scale to zero, panic windows."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/autoscaling/kpa-autoscaler.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Knative Pod Autoscaler (KPA)

Knative deployment mode only. Default metric is `concurrency` (average in-flight requests per pod); valid `scaleMetric` values are `concurrency`, `rps`, `cpu`, `memory`. The old annotation `autoscaling.knative.dev/target` equals `scaleTarget` and is a SOFT limit: bursts can exceed it.

```yaml
spec:
  predictor:
    scaleTarget: 1
    scaleMetric: concurrency      # the page's other example uses qps; its transformer example uses rps
    model:
      modelFormat: {name: tensorflow}
      storageUri: "gs://kfserving-examples/models/tensorflow/flowers"
```

Load test: `hey -z 30s -c 5 -m POST -host ${SERVICE_HOSTNAME} -D input.json http://${INGRESS_HOST}:${INGRESS_PORT}/v1/models/$MODEL_NAME:predict`; with target 1 and 5 concurrent requests about 5 pods start.

Timing: concurrency is averaged over a 60 s window; a 6 s panic window enters panic mode if it reaches 2x the target concurrency, using a shorter and more sensitive window; the autoscaler returns to the 60 s window once panic conditions have not been met for 60 s.

## Hard limit
`containerConcurrency: 10` on the predictor is a HARD cap per replica; extra requests are buffered until capacity frees up.

## Scale to zero
`minReplicas` defaults to 1. Set `minReplicas: 0` for pods to scale down when idle (useful for GPUs).

## GPU
GPU utilization fluctuates, so scale GPU services on `scaleMetric: concurrency` with `scaleTarget: 1` instead.

## Per component
```yaml
  predictor:   {scaleTarget: 2, scaleMetric: concurrency}
  transformer: {scaleTarget: 8, scaleMetric: rps}
```

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website kpa-autoscaler.md page: Knative-mode-only note, default and listed `scaleMetric` values, soft-limit wording, 60 s and 6 s windows with the 2x panic rule, `containerConcurrency` hard limit, `minReplicas` default of 1, and the GPU guidance. Replaced the vague panic wording. The page lists `qps` in an example but not in its list of possible values, so prefer `rps`.
