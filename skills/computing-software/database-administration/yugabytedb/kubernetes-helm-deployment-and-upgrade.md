---
id: computing-software.database-administration.yugabytedb.kubernetes-helm-deployment-and-upgrade
name: kubernetes-helm-deployment-and-upgrade
category: computing-software
field: database-administration
product: yugabytedb
tags: [kubernetes, helm, statefulset, liveness-probe, readiness-probe, partition-tserver, storage-class, pod-resources]
level: practitioner
status: docs-checked
description: "Deploy YugabyteDB on Kubernetes with the Helm chart, size pods, set probes, scale tservers and run a rolling upgrade with the partition setting."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/kubernetes/single-zone/oss/helm-chart.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/kubernetes/best-practices.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/upgrade-deployment-kubernetes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kubernetes Helm deployment and upgrade

Install:
```
helm repo add yugabytedb https://charts.yugabyte.com
helm install yb-demo yugabytedb/yugabyte --version <version> --namespace yb-demo --wait
```
Defaults in the chart's values.yaml are 3 masters and 3 tservers; master pods get 2 CPU and 2Gi, tserver pods 2 CPU and 4Gi, each with 10Gi storage. The chart is tested with Kubernetes 1.20 or later and Helm 3.4 or later. On Minikube override the resource requests (for example `resource.master.requests.cpu=0.5` and `resource.master.requests.memory=0.5Gi`, and the same for tserver) and consider `enableLoadBalancer=False`. Scale tservers with `helm upgrade --set replicas.tserver=5 yb-demo yugabytedb/yugabyte` (only tservers need scaling in an RF 3 cluster; masters stay at 3).

The pod memory limit becomes the tserver `--memory_limit_hard_bytes`.

Probes: readiness probes are disabled by default (enable with `master.readinessProbe.enabled` and `tserver.readinessProbe.enabled`). `livenessProbe.enabled` defaults to true; with persistent storage the default probe writes a `disk.check` timestamp under each data directory and runs sync, and it is omitted when `storage.ephemeral` is true.

Storage tradeoff: local SSD has higher throughput and lower latency but a pod that moves loses its local copy and needs a full remote bootstrap of its tablets; remote SSD survives pod movement. The best-practices page does not recommend local storage for most production use.

Rolling upgrade: set `partition.tserver` to the number of tservers in the zone so the tserver StatefulSet holds back while masters upgrade, then run the upgrade again without it to roll tservers. Finalizing differs between the two official pages: the Helm chart page runs `yb-admin finalize_upgrade`, while the Kubernetes upgrade page runs `promote_auto_flags` and then `upgrade_ysql`; follow the page that matches your release. From v2026.1.0.0, when cert-manager manages certificates, `rootCA.cert` takes precedence over cert-manager's `ca.crt`; set it to an empty string to keep the old behaviour. From v2026.1.2 images run as non-root by default.

## Checked

2026-11-04. Confirmed against the Helm chart page (repo add, install command, values.yaml defaults, scaling with replicas.tserver, memory limit converted to `--memory_limit_hard_bytes`, readiness probes off by default, liveness defaults, Minikube overrides, non-root from v2026.1.2), Kubernetes best practices (local vs remote SSD) and the Kubernetes upgrade page (partition.tserver, rootCA.cert precedence from v2026.1.0.0). Conflict recorded in the skill: the Helm chart page finalizes with `finalize_upgrade`, the upgrade page with `promote_auto_flags` plus `upgrade_ysql`. Corrected the cert-manager wording; the skill had said 'other certificate sources'.

Method: documentation only; no commands were run.
