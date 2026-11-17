---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-monitoring-and-logging-components-selection
name: gke-monitoring-and-logging-components-selection
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-monitoring-components, gke-logging-components, logging-variant, managed-prometheus, observability-config]
level: practitioner
status: docs-checked
description: "Choose which GKE logging and monitoring components to collect (system, workloads, control plane, kube-state, cAdvisor, DCGM) and the max-throughput logging variant."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/concepts/about-logs", "https://docs.cloud.google.com/sdk/gcloud/reference/container/clusters/update", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/configure-metrics", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/adjust-log-throughput"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE monitoring and logging components selection

## Logging
```bash
gcloud container clusters update prod --location=<R> \
  --logging=SYSTEM,WORKLOAD,API_SERVER,SCHEDULER,CONTROLLER_MANAGER
gcloud container clusters describe prod --location=<R> --format="value(loggingConfig.componentConfig.enableComponents)"
```
Valid `--logging` values: `SYSTEM`, `WORKLOAD`, `API_SERVER`, `CONTROLLER_MANAGER`, `SCHEDULER`, `KCP_HPA`, `KCP_VPA` and `NONE`. `SYSTEM` must be enabled to collect any logs, and `WORKLOAD` cannot be collected on its own; workload logging is on by default but optional. On Autopilot you cannot disable the Cloud Logging and Cloud Monitoring integration.

High-volume nodes: `--logging-variant=MAX_THROUGHPUT` (up to 10 MiB/s per node, needs control plane 1.23.13-gke.1000 or later, uses more CPU and memory) versus `DEFAULT` (at least 100 KiB/s per node). Changing the variant on an existing node pool recreates its nodes.

## Monitoring
```bash
gcloud container clusters update prod --location=<R> \
  --monitoring=SYSTEM,API_SERVER,SCHEDULER,CONTROLLER_MANAGER,STORAGE,POD,DEPLOYMENT,STATEFULSET,DAEMONSET,HPA,CADVISOR,KUBELET,DCGM \
  --enable-managed-prometheus
```
- Valid `--monitoring` values on the metrics page: `SYSTEM`, `API_SERVER`, `SCHEDULER`, `CONTROLLER_MANAGER`, `STORAGE`, `POD`, `DEPLOYMENT`, `STATEFULSET`, `DAEMONSET`, `HPA`, `JOBSET`, `CADVISOR`, `KUBELET`, `DCGM` and `NONE`. Include `JOBSET` if you use it.
- GKE system metrics are not charged for ingestion; the observability packages (control plane, kube state, and so on) are charged by samples ingested.
- Autopilot clusters cannot turn off system metric collection.

## Cost lens
Logging, Monitoring and Managed Service for Prometheus charges follow the volume of logs and metrics collected. Enable the extra observability packages where you use them, and leave them off elsewhere.

## Gotchas
- Autopilot clusters cannot disable the Cloud Logging and Cloud Monitoring integration.
- For an existing cluster, changing the logging agent variant does not affect existing node pools; it applies to node pools added later (changing it on a node pool recreates the nodes).

## Verify
- [ ] `describe` shows the intended components, and the matching logs and metrics appear in Cloud Logging and Metrics Explorer.

## Checked

2026-10-24, GKE about-logs, gcloud clusters update reference, configure-metrics and adjust-log-throughput pages on docs.cloud.google.com. Confirmed: `--logging` and `--monitoring` value lists, SYSTEM dependency rule, `--logging-variant` values and throughput figures, Autopilot restrictions, billing statements for system metrics and observability packages. Corrected: `JOBSET` and `KCP_HPA`/`KCP_VPA` values were missing, the variant change recreates nodes rather than restarting the agent. Removed unconfirmed claims about the Terraform blocks, kube state metric name and per-component content table.

Method: documentation only; no commands were run.
