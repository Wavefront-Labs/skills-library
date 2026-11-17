---
id: computing-software.devops-ci-cd.argo-cd.rollouts-with-hpa-and-controller-metrics
name: rollouts-with-hpa-and-controller-metrics
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, rollouts-hpa, rollouts-metrics, rollout-scale-subresource, rollouts-prometheus]
level: advanced
status: docs-checked
description: "Autoscale Argo Rollouts with an HPA targeting the Rollout scale subresource, avoid replica drift in GitOps, and monitor rollouts via the controller's Prometheus metrics."
sources: ["https://argo-rollouts.readthedocs.io/en/stable/features/hpa-support/", "https://argo-rollouts.readthedocs.io/en/stable/features/controller-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rollouts with HPA and controller metrics

## 1. HPA on a Rollout
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: api }
spec:
  scaleTargetRef:
    apiVersion: argoproj.io/v1alpha1
    kind: Rollout
    name: api
  minReplicas: 4
  maxReplicas: 40
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 65 } }
```
Rollouts expose the `/scale` subresource (since v0.3.0), and HPA works through the autoscaling/v2 API (Kubernetes 1.23+). The HPA sets the **total** replica count; during a
canary the controller allocates pods according to the configured strategy; the HPA decides the total, Argo Rollouts does the deployment changes.

## 2. GitOps replica drift
Omit `spec.replicas` from the Rollout in Git, or ignore it:
```yaml
ignoreDifferences:
  - { group: argoproj.io, kind: Rollout, jsonPointers: [/spec/replicas] }
```
plus `RespectIgnoreDifferences=true`, otherwise every sync resets replicas and the HPA fights Argo CD.

## 3. Controller metrics
The controller serves Prometheus metrics on port **8090** `/metrics`.
Useful series:
- `rollout_info` — information about the rollout (`rollout_phase` is deprecated in favour of it)
- `rollout_info_replicas_available`, `rollout_info_replicas_unavailable`, `rollout_info_replicas_desired`, `rollout_info_replicas_updated`
- `analysis_run_info`, `analysis_run_phase`, `analysis_run_metric_phase` — state of analysis runs
- `experiment_info`, `controller_clientset_k8s_request_total`
Alert on rollouts stuck unhealthy and on failing analysis runs; thresholds are yours to choose.

## Gotchas
- HPA scaling during a canary changes canary pod count — analysis based on absolute request counts gets noisy; use rates/ratios.

## Verify
- [ ] Load test scales the Rollout via HPA mid-canary; weights stay proportional; no Argo CD OutOfSync on replicas.

## Checked

2026-11-02. Confirmed against the Argo Rollouts HPA support and controller metrics pages: /scale subresource, autoscaling/v2, HPA sets total replicas, metrics on port 8090 /metrics, rollout_info and replica series, analysis_run_* series, experiment_info, controller_clientset_k8s_request_total; and the Argo CD sync options page: RespectIgnoreDifferences=true. Removed (not stated in the docs): the Helm ServiceMonitor value, rollout_info label set, the 5 minute alert, Error vs Failed guidance, workloadRef advice, weight-split statement and the scaleDownDelay capacity claim.

Method: documentation only; no commands were run.
