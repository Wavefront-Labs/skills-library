---
id: computing-software.ai-ml-engineering.kserve.kserve-keda-autoscaling
name: kserve-keda-autoscaling
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [keda, scaledobject, triggerauthentication, external-metrics, prometheus, opentelemetry, podmetric, otel-add-on, vllmnum-requests-running, enable-prometheus-scraping]
level: advanced
status: docs-checked
description: "Autoscale an InferenceService with KEDA in Standard mode: autoscalerClass keda, ScaledObject, autoScaling.metrics of type Resource, External (Prometheus) and PodMetric."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/autoscaling/keda-autoscaler.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KEDA autoscaling

Standard (raw) mode only. Install KEDA, then annotate: `serving.kserve.io/autoscalerClass: "keda"`. KServe creates a `ScaledObject` named like `NAME-predictor` (`kubectl get scaledobjects`).

## Metric types under `autoScaling.metrics`
- `Resource`: `resource.name` cpu or memory; `target.type` `Utilization` (`averageUtilization`) or `AverageValue` (`averageValue`).
- `External`: `external.metric.backend` (`prometheus`, `graphite`), `serverAddress`, `query`, optional `authModes: bearer`, `authenticationRef.name`; `target.type: Value`, `value`.
- `PodMetric` (OpenTelemetry): `podmetric.metric.backend: opentelemetry`, `metricNames`, `query`, `target.value`.

```yaml
metadata:
  annotations:
    serving.kserve.io/deploymentMode: "Standard"
    serving.kserve.io/autoscalerClass: "keda"
    serving.kserve.io/enable-prometheus-scraping: "true"
    prometheus.io/scrape: "true"
    prometheus.io/path: "/metrics"
    prometheus.io/port: "8080"
spec:
  predictor:
    minReplicas: 1
    maxReplicas: 5
    autoScaling:
      metrics:
        - type: External
          external:
            metric:
              backend: "prometheus"
              serverAddress: "http://prometheus.istio-system.svc.cluster.local:9090"
              query: vllm:num_requests_running
            authenticationRef: {name: keda-prom-creds}   # TriggerAuthentication with bearerToken and ca
            target: {type: Value, value: "2"}
```

## OpenTelemetry
Install the OpenTelemetry Operator and `kedify otel-add-on` (Helm `--set validatingAdmissionPolicy.enabled=false`, needed for vLLM-style metric names). Add annotation `sidecar.opentelemetry.io/inject: "NAME-predictor"` so a collector sidecar exports pod metrics; check `kubectl get opentelemetrycollector`.

## Per component
Unlike HPA, KEDA creates a ScaledObject only for components that declare `autoScaling`; others stay at fixed `minReplicas` (default 1). KServe rejects, at admission, an InferenceService with `autoscalerClass: keda` where no component declares `autoScaling`.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the KServe website KEDA autoscaler page: Raw-mode-only note, annotation, ScaledObject check, resource and external metric options (`prometheus`, `graphite`), optional `authModes` and `authenticationRef`, the kedify otel-add-on webhook-disable flag and its reason, the sidecar inject annotation pattern `<inferenceservice-name>-predictor`, and the per-component ScaledObject and admission rejection behaviour. The page names the install chart `oci://ghcr.io/kedify/charts/otel-add-on`; pin the chart version from the page when you install.
