---
id: computing-software.cloud-infrastructure-engineering.kubernetes.off-hours-scale-down-non-production
name: off-hours-scale-down-non-production
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cost-optimisation, off-hours-scaling, kube-downscaler, keda-cron, cluster-autoscaler]
level: practitioner
status: docs-checked
description: "Scale non-production workloads down outside working hours with kube-downscaler annotations, KEDA cron triggers or CronJobs, and let the autoscaler remove idle nodes."
sources: ["https://github.com/caas-team/py-kube-downscaler", "https://github.com/caas-team/GoKubeDownscaler", "https://keda.sh/docs/latest/scalers/cron/", "https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Off-hours scaling for non-production

Dev and staging often run 24x7 for about 50 working hours a week. Scaling them down nights and
weekends cuts their compute bill, once the autoscaler removes the empty nodes.

## kube-downscaler
The maintained Python implementation, py-kube-downscaler (caas-team), is in maintenance-only mode;
its README points to the Go rewrite, GoKubeDownscaler, as the successor with feature updates, so
check the successor's documentation for new installs. The annotations below are from the
py-kube-downscaler README. Install it (one Deployment), then annotate namespaces or workloads:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  annotations:
    downscaler/uptime: "Mon-Fri 07:00-20:00 Europe/London"
```
```yaml
metadata:
  annotations:
    downscaler/exclude: "true"          # keep this workload running
```
Cluster-wide default: `--default-uptime="Mon-Fri 07:00-20:00 Europe/London"` with
`--exclude-namespaces=kube-system,monitoring`. It scales Deployments, StatefulSets, HPAs (via
`downscaler/downtime-replicas`, which must be at least 1 for an HPA), and others, sets CronJobs to
`suspend: true`, and restores the original replica count afterwards.

## KEDA cron scaler
```yaml
triggers:
- type: cron
  metadata: {timezone: Europe/London, start: "0 7 * * 1-5", end: "0 20 * * 1-5", desiredReplicas: "2"}
```
With `minReplicaCount: 0`, the workload scales to zero outside the window. `start` and `end` must
differ, and scale-down happens after the cooldown period (5 minutes by default) following `end`.

## Plain CronJob
A CronJob running `kubectl scale deploy --all --replicas=0 -n staging` at night and a second one
restoring counts (store them in an annotation first). Needs a ServiceAccount with scale rights.

## Make the savings real
- Cluster autoscaler or Karpenter must be able to remove nodes: no PDBs blocking and no local
  storage pinning. For consolidation a node counts as empty if only DaemonSet and static pods run
  on it.
- Databases on PVCs: scaling a StatefulSet to zero keeps its PVCs under the default
  `persistentVolumeClaimRetentionPolicy` (`Retain`); managed databases need their own stop
  schedule.

## Verify
At night, `kubectl get deploy -n staging` shows 0 replicas and node count in the non-prod pool
drops; in the morning everything returns to its previous replica counts.

## Checked

Checked 2026-10-27. Documentation checked: py-kube-downscaler README (caas-team, main), KEDA cron scaler docs (content/docs/2.22 on the keda-docs main branch; latest KEDA release v2.21.0), Kubernetes website main tree (v1.38 dev; v1.37 latest release) node autoscaling and StatefulSet pages. Confirmed: `downscaler/uptime` format and `downscaler/exclude`, `--default-uptime`, `--exclude-namespaces`, HPA downtime replicas minimum of 1, CronJob suspension; KEDA cron fields `timezone`, `start`, `end`, `desiredReplicas`, `minReplicaCount: 0` and 5 minute scale-down after `end`; empty-node definition; default PVC retention. Fixed: the original hjacobs/kube-downscaler Codeberg source (replaced by the fork whose README was read, now maintenance-only) and the missing note about the successor. Removed as unconfirmed: the "more than half" savings figure.

Method: documentation only; no commands were run.
