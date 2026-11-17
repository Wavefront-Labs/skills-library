---
id: computing-software.cloud-infrastructure-engineering.calico.monitoring-felix-metric-families
name: monitoring-felix-metric-families
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [prometheus, metrics, felix, calculation-graph, cluster-metrics, policies, endpoints, dataplane]
level: practitioner
status: docs-checked
description: "Find the right Felix metric: cluster-wide counts of hosts, policies, tiers and endpoints, per-host active policies and selectors, and calculation-graph timing."
sources:
  - https://docs.tigera.io/calico/latest/reference/felix/prometheus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable Felix metrics through its configuration (see the component metrics skill). The page states that some metrics are tied to Felix implementation choices, so there is no hard guarantee they persist across releases.

**Cluster-wide** (same on every node):
- `felix_cluster_num_hosts`, `felix_cluster_num_workload_endpoints`, `felix_cluster_num_host_endpoints`
- `felix_cluster_num_policies`, `felix_cluster_num_profiles`, `felix_cluster_num_tiers`

**General, per host:**
- `felix_active_local_endpoints`: active workload plus host endpoints on this host.
- `felix_active_local_policies`: only active policies, those matching a local endpoint, carry significant cost.
- `felix_active_local_selectors`: only active rule source or destination selectors have significant cost.
- `felix_exec_time_micros`: time to fork and exec child processes.
- `felix_log_errors` and `felix_logs_dropped`: logging failures, including logs dropped because the output stream was blocked.

**Calculation graph** (works out active endpoints and policy from datastore updates):
- `felix_calc_graph_output_events`
- `felix_calc_graph_update_time_seconds`
- `felix_calc_graph_updates_processed`

**Common data plane:** `felix_resyncs_started` (not meaningful in a Typha deployment), `felix_resync_state` (1 waiting for datastore, 2 resync in progress, 3 in sync), `felix_int_dataplane_apply_time_seconds` and `felix_int_dataplane_failures`. The page also lists iptables (`felix_iptables_*`) and BPF (`felix_bpf_*`) data plane metrics.

**Label index** (selector cost): `felix_label_index_num_active_selectors{optimized="true|false"}`. A few unoptimized selectors are fine; many are costly at scale. If `felix_label_index_selector_evals{result="false"}` is many times `result="true"`, some selectors are probably not optimized.

Use the `active_local_*` pair when judging per-node policy cost, and the calc-graph timing when datastore churn is suspected.

## Checked

2026-11-08. The Monitoring Felix with Prometheus page was read in full. Metric names and descriptions in the cluster-wide, general, calculation graph, data plane and label index entries were confirmed.

Method: documentation only; no commands were run.
