---
id: computing-software.cloud-infrastructure-engineering.kubernetes.hpa-multiple-and-containerresource-metrics
name: hpa-multiple-and-containerresource-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, hpa, multiple-metrics, containerresource, container-resource-metric, autoscaling-v2, sidecars]
level: advanced
status: docs-checked
description: "Combine several HPA metrics (resource, pods, object, external) knowing the max-of-recommendations rule, and use ContainerResource metrics so sidecars don't distort CPU scaling."
sources: ["https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#algorithm-details", "https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#container-resource-metrics", "https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#autoscaling-on-multiple-metrics-and-custom-metrics", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPA with multiple metrics and ContainerResource metrics

## Multiple metrics: the max rule
With several entries in `spec.metrics`, the HPA computes a desired replica count for **each**
and uses the **highest**. If a metric cannot be turned into a desired replica count (for
example an error fetching it) and the metrics that can be fetched suggest a scale down, scaling
is skipped; scale-up still works when any fetchable metric asks for more replicas.
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: web}
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: web}
  minReplicas: 3
  maxReplicas: 40
  metrics:
  - type: ContainerResource
    containerResource:
      name: cpu
      container: app                      # ignore istio-proxy / log shipper
      target: {type: Utilization, averageUtilization: 65}
  - type: Pods
    pods:
      metric: {name: http_requests_per_second}
      target: {type: AverageValue, averageValue: "200"}
  - type: External
    external:
      metric: {name: sqs_messages_visible, selector: {matchLabels: {queue: orders}}}
      target: {type: AverageValue, averageValue: "30"}   # per replica
```
Design: one "work" metric (RPS, queue depth) + CPU as a safety net. Don't add metrics that
move in opposite directions — the max rule means the most aggressive one always wins.

## ContainerResource (stable since 1.30)
`Resource` utilization is computed against the requests of the containers in each pod. A
sidecar with a big request and low usage drags utilisation down (HPA under-scales); a busy
sidecar can trigger scaling the app doesn't need. `ContainerResource` tracks one named
container; pods where that container is absent are ignored. `Utilization` targets are a
percentage of that container's request, so it needs a request.

## Inspect
```bash
kubectl describe hpa web          # each metric's current/target, events "New size: N; reason: ..."
kubectl get hpa web -o jsonpath='{.status.currentMetrics}'
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta2/namespaces/shop/pods/*/http_requests_per_second"
```
Pods/Object metrics are served by the custom metrics API (`custom.metrics.k8s.io`, for example
through prometheus-adapter); External metrics are served by `external.metrics.k8s.io`, which
may be provided by the same kind of adapter. Pods metrics support only the `AverageValue` target.

## Verify
- [ ] `describe hpa` shows all metrics with values (none `<unknown>`); load test scales on the intended metric.

## Checked

Checked 2026-10-24 against Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24).
- Largest-of-desired-replicas rule and the "skip scale-down when a metric cannot be fetched" behaviour: HPA page, algorithm details.
- ContainerResource metric source shape (`containerResource.name/container/target`) and the "container absent, pod ignored" rule: HPA page; feature gate HPAContainerMetrics is stable from 1.30 (gate removed later) per the feature-gate page.
- Custom metrics API version is `v1beta2` (HPA page, API links); Pods metrics support only `AverageValue` (walkthrough).

Method: documentation only; no commands were run.
