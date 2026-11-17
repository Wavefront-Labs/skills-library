---
id: computing-software.ai-ml-engineering.kserve.kserve-config-metrics-localmodel-multinode
name: kserve-config-metrics-localmodel-multinode
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [metricsaggregator, enablemetricaggregation, enableprometheusscraping, opentelemetrycollector, scrapeinterval, keda-otel-scaler, localmodel-config, jobnamespace, jobttlsecondsafterfinished, disablevolumemanagement, customgpuresourcetypelist, servingkserveiogpu-resource-types]
level: advanced
status: docs-checked
description: "inferenceservice-config keys for metric aggregation, Prometheus scraping, OpenTelemetry collector (KEDA), localModel cache and multiNode custom GPU resource types."
sources: ["https://github.com/kserve/website/blob/main/docs/admin-guide/configurations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# inferenceservice-config: metrics, OTel, localModel, multiNode

**metricsAggregator**
- `enableMetricAggregation` (default "false"): queue-proxy aggregation for Knative; adds annotation `serving.kserve.io/enable-metric-aggregation` on each service.
- `enablePrometheusScraping` (default "false"): adds Prometheus annotations to pods; the Prometheus port is the default 9090 when `serving.kserve.io/enable-metric-aggregation` is false, otherwise the metric aggregation port. No per-service annotation for scraping.

**opentelemetryCollector** (KEDA autoscaling in Standard mode): `scrapeInterval` "5s", `metricReceiverEndpoint` `keda-otel-scaler.keda.svc:4317`, `metricScalerEndpoint` `keda-otel-scaler.keda.svc:4318` (the endpoint KEDA's ScaledObject scrapes).

**localModel**
```json
{"enabled": false, "jobNamespace": "kserve-localmodel-jobs",
 "defaultJobImage": "kserve/storage-initializer:latest", "fsGroup": 1000,
 "jobTTLSecondsAfterFinished": 3600, "reconcilationFrequencyInSecs": 60,
 "disableVolumeManagement": false}
```
Per-service opt-out annotation: `serving.kserve.io/disable-localmodel`. `reconcilationFrequencyInSecs` (spelled that way) is how often the agent checks for missing models. `disableVolumeManagement` stops PV/PVC management in namespaces with no InferenceServices.

**multiNode**: `customGPUResourceTypeList` (default empty), for example `["custom.com/gpu"]`. It identifies GPU resource types so the multi-node pod adds GPU resources dynamically; it does not restrict usable GPUs. Per service: annotation `serving.kserve.io/gpu-resource-types`.

## Checked
Confirmed against the KServe Configurations admin guide: the metricsAggregator, opentelemetryCollector, localModel and multiNode blocks, every default, the per-service annotations, the Prometheus port rule and the customGPUResourceTypeList semantics.

Method: docs-only read of cited pages, 2026-11-08
