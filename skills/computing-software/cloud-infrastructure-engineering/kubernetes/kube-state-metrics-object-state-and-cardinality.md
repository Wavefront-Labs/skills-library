---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-state-metrics-object-state-and-cardinality
name: kube-state-metrics-object-state-and-cardinality
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-state-metrics, ksm, prometheus, cardinality, label-cardinality, object-state, kube-pod-status-phase, kube-deployment-status, sharding, metric-allowlist, annotations-labels-metric, metric-labels-allowlist]
level: advanced
status: docs-checked
description: "What kube-state-metrics exposes (object state, not resource usage), how it differs from cAdvisor/metrics-server, and how to control label cardinality."
sources: ["https://github.com/kubernetes/kube-state-metrics/blob/main/README.md", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/developer/cli-arguments.md", "https://github.com/kubernetes/kube-state-metrics/tree/main/docs/metrics"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# kube-state-metrics: object state, not resource usage

**Goal:** know what kube-state-metrics (KSM) is for — turning the Kubernetes API's object
state into Prometheus metrics — and avoid the two classic mistakes: expecting it to report
CPU/memory (it doesn't), and allowlisting too many labels or annotations into the
label metrics (`kube_pod_labels`, `kube_pod_annotations`).

## 1. What it is
KSM watches the apiserver (list-watch, like a controller) and converts object **status
fields** into gauges — it never touches a kubelet or cgroup. Core examples:
- `kube_pod_status_phase{phase="Running|Pending|Failed|..."}` — a gauge of 0/1 per phase, so
  `sum(kube_pod_status_phase{phase="Pending"})` counts stuck pods.
- `kube_deployment_status_replicas_available` vs `kube_deployment_spec_replicas` — the
  canonical "is this rollout actually at desired state" check.
- `kube_pod_container_status_restarts_total`, `kube_pod_container_status_waiting_reason` —
  the alertable surface for CrashLoopBackOff (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.troubleshooting-crashloops-and-oom`).
- `kube_node_status_condition{condition="Ready|MemoryPressure|DiskPressure|...", status="true|false|unknown"}`
  — the Prometheus-side view of node conditions (compare to
  `computing-software.cloud-infrastructure-engineering.kubernetes.node-problem-detector-and-node-conditions`,
  which is what *writes* custom conditions NPD detects).
- `kube_job_status_failed`, `kube_cronjob_next_schedule_time`, `kube_horizontalpodautoscaler_status_current_replicas`,
  `kube_persistentvolumeclaim_status_phase` — every controller-managed object gets a status
  surface this way.

This is complementary to, not overlapping with, metrics-server/cAdvisor
(`computing-software.cloud-infrastructure-engineering.kubernetes.cadvisor-and-cgroup-container-metrics`):
KSM answers "what does the control plane think the state is," cAdvisor/metrics-server answer
"how much CPU/memory is actually being consumed." A pod can be `Running` per KSM while
starved of CPU per cAdvisor — you need both to diagnose "why is this slow."

## 2. The cardinality trap
`kube_pod_labels`, `kube_pod_annotations` and `kube_node_labels` turn Kubernetes labels and annotations into
Prometheus labels (`label_<name>`). By default the labels and annotations metrics are **not exposed**; you opt in with
an allowlist. The CLI help warns that a single `*` per resource (for example `pods=[*]`) allows any label and has
severe performance implications. Every distinct combination of allowed label values is a separate series, so values
that change per pod (a git SHA, a timestamp) multiply cardinality.

Controls KSM supports:
- `--metric-labels-allowlist=pods=[app,team,env]` (resource-scoped, plural resource names) to expose only named labels;
  `--metric-annotations-allowlist` works the same way for annotations.
- `--metric-allowlist` / `--metric-denylist` (exact names or regexes) to drop whole metrics, and `--metric-opt-in-list`
  for metrics that are off by default.
- `--resources` to disable object types you do not query (fewer watches, fewer series); the exposition endpoint also
  accepts `?resources=` and `?exclude_resources=` query parameters.
- Prometheus-side `metric_relabel_configs` with `labeldrop` also work.

## 3. Scaling KSM itself
- KSM can be sharded with `--shard` (zero indexed) and `--total-shards`, or with automated sharding when run as a
  StatefulSet with `--pod` and `--pod-namespace`. Objects are assigned by an md5 sum of the UID modulo the shard count;
  every instance still unmarshals all objects. The README says to monitor that every shard is up: after any sharding
  change `count(kube_pod_info)` should equal `kubectl get pods -A` (minus the header).
- KSM's own metrics are on `--telemetry-port` (default 8081) and include `kube_state_metrics_list_total` and
  `kube_state_metrics_watch_total` (labels `resource`, `result`) so you can compute list and watch error rates. Alert on
  `up{job="kube-state-metrics"}` so a dead instance does not just leave dashboards stale.

## Gotchas
- KSM metrics are **gauges representing a point-in-time list**, not counters of events — a
  `kube_pod_status_phase` flip from Running to Failed and back within one scrape interval is
  invisible; use Kubernetes Events (`computing-software.cloud-infrastructure-engineering.kubernetes.kubernetes-event-based-debugging`)
  for sub-interval transitions.
- `kube_job_status_failed` is a failed-pod count; use `kube_job_status_failure_reason` for a breakdown by reason and
  `kube_pod_container_status_last_terminated_reason` on the job's pods for container detail.
- Metric stability labels differ (the docs mark many STABLE and some, such as the last-terminated metrics, EXPERIMENTAL);
  read the release notes before upgrading KSM.

## Verify
- [ ] `count(kube_pod_info)` matches the pod count from `kubectl get pods -A --no-headers` (sharding and scrape are healthy).
- [ ] `up{job="kube-state-metrics"}` is alerted on, not just assumed.
- [ ] `count by (label_app) (kube_pod_labels)` cardinality is bounded and reviewed after any new label convention ships.
- [ ] Dashboards combine a KSM status metric with the matching cAdvisor/metrics-server usage metric, not one alone.

## Checked

2026-10-26: kube-state-metrics README, cli-arguments and metric docs (kubernetes/kube-state-metrics main, latest release v2.20.0, repo updated 2026-10-19). Confirmed: labels and annotations metrics are off by default and controlled by allowlists (with the severe-performance warning for the wildcard), the other filter flags and the resources query parameters, sharding algorithm and flags, telemetry port and list/watch metrics, metric names and the STABLE/EXPERIMENTAL labels. Corrected: the old text said these metrics re-emit every label by default and named kube_hpa_status_current_replicas, whose real name is kube_horizontalpodautoscaler_status_current_replicas. Removed unconfirmed sizing thresholds and the v1-to-v2 rename claim.

Method: documentation only; no commands were run.
