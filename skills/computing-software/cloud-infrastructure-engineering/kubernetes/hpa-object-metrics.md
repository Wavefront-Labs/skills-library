---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hpa-object-metrics
name: hpa-object-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, hpa, object-metric, custom-metrics, prometheus-adapter, autoscaling-v2]
level: practitioner
status: docs-checked
description: "Scale on a metric describing another object (Ingress requests per second, queue length on a Service) with HPA Object metrics and target Value vs AverageValue."
sources: ["https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#autoscaling-on-multiple-metrics-and-custom-metrics", "https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#autoscaling-on-metrics-not-related-to-kubernetes-objects", "https://github.com/kubernetes-sigs/prometheus-adapter/blob/master/docs/config.md", "https://github.com/kubernetes/design-proposals-archive/blob/main/instrumentation/custom-metrics-api.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPA Object metrics

Object metrics come from the custom metrics API (`custom.metrics.k8s.io`) and describe a single
Kubernetes object in the same namespace other than the pods being scaled, for example an Ingress.
The metric is not necessarily fetched from that object; it only describes it.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: web}
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: web}
  minReplicas: 3
  maxReplicas: 30
  metrics:
  - type: Object
    object:
      describedObject:
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        name: web
      metric:
        name: requests_per_second
      target:
        type: AverageValue        # divided by current replica count
        averageValue: "100"       # 100 rps per pod
```
- `type: Value`: compare the raw object metric to the target (scale so that metric equals target,
  using ratio to current).
- `type: AverageValue`: metric divided by replicas; usually what you want for throughput.

## Providing the metric (prometheus-adapter)
Example rule; it assumes the Prometheus series carries `namespace` and `ingress` labels.
```yaml
rules:
- seriesQuery: 'nginx_ingress_controller_requests{ingress!="",namespace!=""}'
  resources:
    overrides:
      namespace: {resource: namespace}
      ingress: {group: networking.k8s.io, resource: ingress}
  name: {matches: "^nginx_ingress_controller_requests$", as: "requests_per_second"}
  metricsQuery: 'sum(rate(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)'
```

## Verify
```bash
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta2/namespaces/default/ingresses.networking.k8s.io/web/requests_per_second"
kubectl describe hpa web
```
`FailedGetObjectMetric` means the API path or the adapter rule's resource mapping is wrong.
Prefer External metrics (KEDA or adapter) for things that are not Kubernetes objects, like SQS queues.

## Checked

Checked 2026-10-24 against Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24), the prometheus-adapter configuration doc and the custom metrics API design doc.
- Object metric source shape (`describedObject`, `metric.name`, `target`) and the `Value` vs `AverageValue` semantics: HPA walkthrough.
- API path form `/namespaces/NS/RESOURCE.GROUP/NAME/METRIC`: custom metrics API design doc; `v1beta2` is the version the HPA page links.
- prometheus-adapter rule fields (`seriesQuery`, `resources.overrides` with group and resource, `name.matches/as`, `metricsQuery` with `<<.Series>>`, `<<.LabelMatchers>>`, `<<.GroupBy>>`): prometheus-adapter config doc.
- `FailedGetObjectMetric` is an event reason in the HPA controller source (kubernetes/kubernetes pkg/controller/podautoscaler/horizontal.go).
- The ingress label names in the example rule are not documented in the ingress-nginx metrics page, so the example is labelled as an assumption.

Method: documentation only; no commands were run.
