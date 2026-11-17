---
id: computing-software.cloud-infrastructure-engineering.keda.query-keda-external-metrics-with-kubectl
name: query-keda-external-metrics-with-kubectl
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [external-metrics, kubectl-get-raw, externalmetricnames, metrics-server, external-metrics-k8s-io, debugging]
level: practitioner
status: docs-checked
description: "Query the values KEDA feeds the HPA with kubectl get --raw on external.metrics.k8s.io and find metric names from the ScaledObject status."
sources:
  - https://keda.sh/docs/2.17/operate/metrics-server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Metric names look like `s1-rabbitmq-queueName2`, so read them from the status rather than guessing.
KEDA's metrics server implements the Kubernetes external metrics API, so you can ask it directly what the HPA sees.

List what is exposed:
```bash
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1"
```
The reply is an `APIResourceList` with the `externalmetrics` resource (external metrics only).

Read one value:
```bash
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1/namespaces/YOUR_NAMESPACE/YOUR_METRIC_NAME?labelSelector=scaledobject.keda.sh%2Fname%3D{SCALED_OBJECT_NAME}"
```
KEDA metrics are namespaced, so you must give the namespace of the ScaledObject. Example: metric `s1-rabbitmq-queueName2` of ScaledObject `my-scaled-object` in namespace `sample-ns` is queried through `.../namespaces/sample-ns/s1-rabbitmq-queueName2?labelSelector=scaledobject.keda.sh%2Fname%3Dmy-scaled-object`, returning an `ExternalMetricValueList` whose items contain `metricName`, `timestamp` and `value`.

Find the metric name: KEDA records the names generated from your triggers on the ScaledObject:
```bash
kubectl get scaledobject SCALEDOBJECT_NAME -n NAMESPACE -o jsonpath={.status.externalMetricNames}
```

Exception: the `cpu` and `memory` scalers do not use this API. The HPA uses the standard metrics from the Kubernetes Metrics Server, so query those at `/apis/metrics.k8s.io/v1beta1` instead of `/apis/external.metrics.k8s.io/v1beta1`.

## Checked

2026-11-03. Confirmed on the 2.17 KEDA Metrics Server page: the kubectl get --raw queries, response kinds, status.externalMetricNames jsonpath, cpu and memory exception.

Method: documentation only; no commands were run.
