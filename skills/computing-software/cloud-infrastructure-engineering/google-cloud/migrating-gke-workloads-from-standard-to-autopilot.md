---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migrating-gke-workloads-from-standard-to-autopilot
name: migrating-gke-workloads-from-standard-to-autopilot
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, standard-to-autopilot-migration, autopilot, workload-compatibility, compute-classes, gke-migration]
level: practitioner
status: docs-checked
description: "Move workloads from a GKE Standard cluster to Autopilot: check incompatibilities, set resource requests, replace node selectors with compute classes, and cut over traffic."
sources: ["https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-security#built-in-security", "https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-resource-requests", "https://cloud.google.com/sdk/gcloud/reference/container/clusters/check-autopilot-compatibility"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating workloads from GKE Standard to Autopilot

Clusters cannot be converted in place; you create an Autopilot cluster and move workloads (or, in
newer versions, run Autopilot compute classes inside Standard clusters as a stepping stone).

## 1. Compatibility check
```bash
gcloud container clusters check-autopilot-compatibility <STANDARD_CLUSTER> --location=<R>
```
Typical blockers:
| Standard usage | Autopilot answer |
|---|---|
| privileged containers | blocked by default; allowed only from verified partners, so redesign |
| NET_ADMIN (service meshes) | allowed with `--workload-policies=allow-net-admin` at cluster creation |
| node selectors on custom node pool labels | use an Autopilot ComputeClass (Balanced, Scale-Out, Performance, or a custom one) |
| no resource requests | Autopilot assigns defaults (general-purpose class: 0.5 vCPU, 2 GiB) and enforces per-class minimum and maximum requests: set explicit requests |
| mutating admission webhooks | GKE modifies them to exclude managed namespaces such as kube-system; some resources are rejected |
| SSH to nodes | blocked |

## 2. Prepare manifests
- Set requests to what the Pods need; Autopilot validates them against the allowed minimum and maximum for the selected compute class or hardware (such as GPUs).
- Spot Pods and GPUs use their own selectors and limits: see the Autopilot docs for the current ones.

## 3. Cut over
1. Create the Autopilot cluster in the same VPC with secondary ranges sized for its Pods.
2. Deploy with the same CI pipeline targeting both clusters; add Workload Identity bindings for the new cluster's KSAs.
3. Shift traffic: multi-cluster Gateway weights, or DNS weighted records, or LB backends.
4. Migrate stateful workloads with app-level replication or a backup/restore tool.

## Gotchas
- Pod startup can be slower when new nodes must be provisioned.

## Verify
- [ ] Compatibility check clean; load test on Autopilot meets latency SLO; Standard cluster drained.

## Checked

2026-10-27. Confirmed in the Autopilot security, Autopilot resource requests and `check-autopilot-compatibility` reference pages: privileged containers blocked except verified partners, `--workload-policies=allow-net-admin`, SSH blocked, mutating webhook handling, ComputeClass names, default requests of 0.5 vCPU and 2 GiB for the general-purpose class, per-class minimum and maximum requests. The migrate-to-autopilot page returned 404 and is no longer cited. Removed: hostPath/hostNetwork row, DaemonSet row, CPU:memory ratio, Spot and GPU selector strings, `--format` projection, per-node /24 and max-pods figures, billing and balloon-pod gotchas, Backup for GKE mention. Read end to end.

Method: documentation only; no commands were run.
