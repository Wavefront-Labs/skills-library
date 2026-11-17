---
id: computing-software.cloud-infrastructure-engineering.kubernetes.autoscaler-observability-and-failure-modes
name: autoscaler-observability-and-failure-modes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, hpa, vpa, cluster-autoscaler, karpenter, keda, observability, prometheus, alerting, failedgetresourcemetric, unschedulable, silent-failure, metrics-server]
level: advanced
status: docs-checked
description: "The specific signals and alerts that catch each autoscaler (HPA/VPA/CA/Karpenter/KEDA) silently failing instead of just scaling wrong."
sources: ["https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#algorithm-details", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/proposals/metrics.md", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/reference/metrics.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/nodeclaims.md", "https://github.com/kedacore/keda-docs/blob/main/content/docs/2.22/integrations/prometheus.md", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/horizontalpodautoscaler-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoscaler observability and failure modes

**Goal:** catch "autoscaling stopped working" before an incident does — every autoscaler in the
stack has a specific way of failing *silently* (holding last-known-good state, not erroring
loudly), and each needs its own signal.

## 1. HPA: watch conditions, not just replica count
`kubectl describe hpa` shows `Conditions` — `AbleToScale`, `ScalingActive`, `ScalingLimited`. A
failure to watch for is `ScalingActive: False` with a `FailedGet...Metric` reason
(`FailedGetResourceMetric`, `FailedGetPodsMetric`, `FailedGetObjectMetric`,
`FailedGetExternalMetric`): the HPA cannot compute a desired count from that metric. Per the HPA
docs, when a metric cannot be fetched and the other metrics suggest a scale down, scaling is
skipped (scale-up can still happen). Nothing crashes or restarts, so it is easy to miss.
- Alert on: `kube_horizontalpodautoscaler_status_condition{condition="ScalingActive",status="false"}`
  (kube-state-metrics) sustained for more than one or two metrics-polling intervals.
- Also alert on `kube_horizontalpodautoscaler_status_current_replicas == kube_horizontalpodautoscaler_spec_max_replicas`
  sustained for a long window — pegged at max is not necessarily wrong, but worth a second look combined with
  latency/error-rate metrics to rule out being capacity-starved by `maxReplicas` itself.

## 2. VPA: recommender silence looks identical to "nothing to recommend"
A VPA object has `status.conditions` and `status.recommendation`, but nothing tells you the
recommendation is stale. The practical signal is whether `status.recommendation` keeps changing
for workloads whose load changes; if the recommender pod is down, the VPA object simply stops
updating.
- Alert on the VPA admission-controller/recommender/updater pods' own health (standard
  pod-restart/crashloop alerting is enough; they're ordinary Deployments).
- Cross-check periodically: `kubectl get vpa -A -o yaml` recommendation values actually changing
  over time for workloads with changing load; a recommendation that never moves despite load
  changes is a reason to check the recommender.

## 3. Cluster Autoscaler: logs and events, no rich metrics API by default
CA exposes Prometheus metrics (`cluster_autoscaler_*`) on port 8085 at `/metrics` by default
(`--address`). Useful ones: `cluster_autoscaler_unschedulable_pods_count`,
`cluster_autoscaler_nodes_count` (label `state`), `cluster_autoscaler_failed_scale_ups_total`
(label `reason`) and `cluster_autoscaler_errors_total`.
- `cluster_autoscaler_failed_scale_ups_total` incrementing with no corresponding node count
  change means scale-up operations are failing; use the `reason` label and the CA logs for the
  specific cause (quota, instance availability, permissions).
- A sustained high `cluster_autoscaler_unschedulable_pods_count` with flat node count means CA
  concluded `NotTriggerScaleUp` for all of them — check node group template limits before assuming
  CA itself is broken.
- CA logging the same decision loop repeatedly without a node count change for many minutes is the
  practical "it's stuck" signal when metrics aren't wired up — don't rely on logs alone long-term,
  wire the metrics endpoint.

## 4. Karpenter: richer metrics, watch NodeClaim/NodePool conditions too
Karpenter exposes `karpenter_nodeclaims_*`, `karpenter_nodepools_*` and
`karpenter_pods_startup_duration_seconds` metrics; its metrics reference lists each metric with a
stability level, so check the reference for your installed version before building dashboards.
Beyond metrics, `kubectl get nodeclaims` and `kubectl get nodepools` show live state, and a
NodeClaim has status conditions `Launched`, `Registered` and `Initialized` (and `Drifted` when it
has drifted from its NodePool); `kubectl describe nodeclaim` shows where a NodeClaim is stuck.
- Compare `karpenter_nodepools_usage` with `karpenter_nodepools_limit` (labels `nodepool`,
  `resource_type`): NodePool `spec.limits` stop Karpenter from creating new instances once the
  limit is exceeded, so pending pods with no scale-up can mean a NodePool is at its limit.

## 5. KEDA: metric path and HPA path can fail independently
Because KEDA's ScaledObject creates and feeds a real HPA (see the KEDA architecture skill), you
need **both** layers of observability: the HPA conditions above (fed by KEDA's external metric),
*and* KEDA's own scaler health. `keda_scaler_detail_errors_total` (per scaler),
`keda_scaled_object_errors_total` and `keda_scaled_job_errors_total` catch the case where the external system (queue API,
Prometheus) is failing to answer KEDA's polls — this fails distinctly from an HPA metrics-API
problem and needs its own alert, because `FailedGetExternalMetric` on the HPA side only tells you
*something* is wrong, not whether it's KEDA's poll or the underlying broker.

## Gotchas
- These failures are quiet: a failing metric source shows up as HPA conditions and events, CA
  and Karpenter failures as events, counters and logs, rather than as a crashed pod, so you must
  build the alerting.
- Dashboards built once and never revisited drift out of sync with metric name changes across
  autoscaler version upgrades — re-validate dashboard queries against the `/metrics` endpoint
  and the project's metrics reference after every autoscaler upgrade.
- A healthy-looking autoscaler controller pod (no restarts, no crash) tells you nothing about
  whether it's *successfully acting* — pod health and functional health are different signals;
  alert on both.

## Verify
- [ ] An alert fires within one polling interval of HPA entering `ScalingActive: False` for any
      reason, tested by deliberately breaking a metrics source in a non-prod cluster.
- [ ] VPA recommendation freshness is checked on a schedule, not assumed, for at least the
      highest-traffic workloads using it.
- [ ] CA/Karpenter failed-scale-up counters and NodeClaim/node-group limit events route to the
      same alerting pipeline as application-level capacity alerts, not a separate ignored channel.
- [ ] KEDA scaler error metrics are alerted on independently of the HPA conditions they feed.

## Checked

Checked 2026-10-24 against Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24), the kube-state-metrics HPA metrics doc, the Cluster Autoscaler metrics proposal and FAQ, the Karpenter v1.15 docs source and the KEDA 2.22 Prometheus integration doc.
- kube-state-metrics names: `kube_horizontalpodautoscaler_status_condition`, `..._status_current_replicas`, `..._spec_max_replicas`.
- Cluster Autoscaler: metrics served on `:8085` `/metrics` by default via `--address` (there is no `--metrics-port`); metric names and labels `nodes_count{state}`, `unschedulable_pods_count`, `failed_scale_ups_total{reason}`, `errors_total`.
NodeClaim conditions `Launched`, `Registered`, `Initialized`, `Drifted`; NodePool `spec.limits` behaviour.
- KEDA: `keda_scaler_detail_errors_total`, `keda_scaled_object_errors_total`, `keda_scaled_job_errors_total`.
- HPA behaviour with unfetchable metrics: HPA page. VPA `status.conditions` exists in the VPA API reference.

Method: documentation only; no commands were run.
