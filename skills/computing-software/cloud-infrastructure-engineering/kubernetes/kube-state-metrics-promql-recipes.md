---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-state-metrics-promql-recipes
name: kube-state-metrics-promql-recipes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-state-metrics, ksm-promql, promql, alerting, prometheus]
level: practitioner
status: docs-checked
description: "Write PromQL over kube-state-metrics for crash loops, unavailable replicas, failed jobs, pending PVCs, OOM kills and joins with pod labels and owners."
sources: ["https://github.com/kubernetes/kube-state-metrics/tree/main/docs/metrics", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/developer/cli-arguments.md", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common PromQL over kube-state-metrics

## Workloads
```promql
# containers crash-looping
kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff"} == 1
# restarts in the last hour
increase(kube_pod_container_status_restarts_total[1h]) > 3
# deployments missing replicas for 15m (use in an alert with for: 15m)
kube_deployment_spec_replicas != kube_deployment_status_replicas_available
# rollout stuck: generation not observed
kube_deployment_status_observed_generation != kube_deployment_metadata_generation
# last termination was OOMKilled
kube_pod_container_status_last_terminated_reason{reason="OOMKilled"} == 1
# pods not ready (exclude completed)
sum by (namespace, pod) (kube_pod_status_ready{condition="false"}) * on (namespace, pod) group_left() (kube_pod_status_phase{phase="Running"} == 1)
```

## Jobs and storage
```promql
kube_job_status_failed > 0                        # failed pod count; kube_job_status_failure_reason gives the reason
time() - kube_cronjob_status_last_successful_time > 2 * 3600
kube_persistentvolumeclaim_status_phase{phase="Pending"} == 1
```

## Nodes
```promql
kube_node_status_condition{condition="Ready",status="true"} == 0
kube_node_spec_unschedulable == 1
```

## Joining labels and owners
`kube_pod_labels` carries only labels allowed with `--metric-labels-allowlist` (by default no label values are exposed); they appear as `label_<name>`.
```promql
# restarts by team label
sum by (label_team) (
  increase(kube_pod_container_status_restarts_total[1h])
  * on (namespace, pod) group_left(label_team) kube_pod_labels)
# requests by owning workload (kube-scheduler's kube_pod_resource_request is the more precise source)
sum by (namespace, owner_name) (
  kube_pod_container_resource_requests{resource="cpu"}
  * on (namespace, pod) group_left(owner_name) kube_pod_owner{owner_kind="ReplicaSet"})
```

## Gotchas
- Two KSM instances scraped by one Prometheus double counts; dedupe with `max by`.
- Use `honorLabels: true` or conflicting labels such as `namespace` become `exported_namespace`.

## Verify
Each expression returns sensible series in the Prometheus UI before it goes into an alert.

## Checked

2026-10-26: kube-state-metrics metric docs for pod, deployment, node, job, cronjob and PVC (kubernetes/kube-state-metrics main, latest release v2.20.0), the CLI arguments page and the Prometheus configuration reference. Confirmed every metric name and label used (kube_pod_container_status_waiting_reason, kube_deployment_* names, kube_job_status_failed, kube_cronjob_status_last_successful_time, kube_persistentvolumeclaim_status_phase, kube_node_status_condition, kube_node_spec_unschedulable, kube_pod_owner owner_kind/owner_name, kube_pod_labels label_ prefix), the label allowlist behaviour and exported_ renaming. Added the note that the docs recommend kube-scheduler's pod resource metrics over the container-level request metric. The PromQL expressions themselves were not executed.

Method: documentation only; no commands were run.
