---
id: computing-software.ai-ml-engineering.kserve.kserve-prometheus-metrics
name: kserve-prometheus-metrics
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [prometheus, metrics, prometheuskserveioport, prometheuskserveiopath, servingkserveioenable-prometheus-scraping, request-predict-seconds, queue-proxy, qpext, observability]
level: practitioner
status: docs-checked
description: "Expose model server metrics: enable-prometheus-scraping annotation, prometheus.kserve.io/port and path, latency histograms (request_predict_seconds), queue-proxy ports."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/observability/prometheus-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus metrics

All supported runtimes can export Prometheus metrics on a port defined in the `kserve/config/runtimes` YAML files, for example TorchServe:

```yaml
spec:
  annotations:
    prometheus.kserve.io/port: '8082'
    prometheus.kserve.io/path: "/metrics"
```

Override on the InferenceService and turn on with:

```yaml
metadata:
  annotations:
    serving.kserve.io/enable-prometheus-scraping: "true"
```

Default for the annotation can be set in `inferenceservice-config`. The annotations only declare port and path; you must still configure Prometheus to scrape the pod. There is no unified metric set across model servers.

## Python servers
lgbserver, paddleserver, pmmlserver, sklearnserver, xgbserver and custom predictors/transformers emit latency histograms:

| Metric | Meaning |
|---|---|
| `request_preprocess_seconds` | pre-processing latency |
| `request_explain_seconds` | explain latency |
| `request_predict_seconds` | prediction latency |
| `request_postprocess_seconds` | post-processing latency |

Per-step latencies are also logged per request.

## Knative / queue-proxy
Exporting metrics in serverless mode needs the queue-proxy extension (qpext) image. The queue proxy emits metrics on port 9091 by default; with qpext aggregation the aggregated port is 9088.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited Prometheus metrics page in full. Corrected where the runtime port is defined (kserve/config/runtimes YAML files) and dropped the qpext README pointer, which the page does not make for the configmap default.
