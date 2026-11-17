---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-node-pools-and-upgrades
name: gke-node-pools-and-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, node-pools, node-auto-provisioning, nap, gke-upgrades, release-channels, maintenance-windows, maintenance-exclusions, surge-upgrade, blue-green-upgrade, node-auto-upgrade, node-auto-repair, cluster-autoscaler, gke-version-skew, rollout-sequencing, pdb]
level: practitioner
status: docs-checked
description: "Operate GKE node pools and upgrades: pool layout with taints, surge vs blue-green upgrades, maintenance windows and exclusions, release channels, NAP limits, and rollout sequencing across clusters."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/concepts/node-pool-upgrade-strategies", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/node-pool-upgrade-strategies", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/maintenance-windows-and-exclusions", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/maintenance-windows-and-exclusions", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/release-channels", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/cluster-upgrades", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/node-auto-provisioning", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/node-pools"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE node pools and upgrades

**Goal:** node pools shaped by workload class, upgrades that happen in your window with
no customer-visible disruption, and a way to pause them when the business says no.

## 1. Pool layout
```bash
gcloud container node-pools create apps --cluster=prod --region=europe-west1 \
  --machine-type=n2-standard-8 --num-nodes=1 \
  --node-labels=pool=apps --node-taints=workload=apps:NoSchedule \
  --max-surge-upgrade=1 --max-unavailable-upgrade=0 \
  --service-account=gke-nodes@<PROJECT_ID>.iam.gserviceaccount.com
```
- Use a **dedicated, minimally privileged node service account** instead of the Compute Engine default (the node pools page recommends this). Grant only what nodes need, such as logging, monitoring and Artifact Registry read roles.
- Separate pools by purpose: a `system` pool without taints, `apps`, a Spot pool (`--spot`, see `gke-spot-pods-and-spot-node-pools`), and a GPU pool (see `gke-gpu-node-pools-and-drivers`).
- Machine attributes of an existing pool (`--machine-type`, `--disk-type`, `--disk-size`) can be changed with `gcloud container node-pools update`, but the change recreates the nodes and can disrupt running workloads. Plan it like an upgrade, or create a new pool and migrate.

## 2. Node auto-provisioning (NAP)
`gcloud container clusters update prod --enable-autoprovisioning --min-cpu=0 --max-cpu=500 --min-memory=0 --max-memory=2000 --autoprovisioning-config-file=nap.yaml`. `--min-cpu/--max-cpu` and `--min-memory/--max-memory` (GiB) are cluster-wide limits, including manually created pools. The YAML file can hold `resourceLimits`, `management` (`autoRepair`, `autoUpgrade`), `shieldedInstanceConfig`, `imageType`, `serviceAccount`, `scopes`, `autoprovisioningLocations`, `bootDiskKmsKey` and `upgradeSettings`. Set resource limits so a bad request does not create a large fleet.

## 3. Upgrade strategy per pool
| Strategy | How | Use |
|---|---|---|
| **Surge** (default) | `--max-surge-upgrade=1 --max-unavailable-upgrade=0` (defaults: `maxSurge` 1, `maxUnavailable` 0, counted per zone) | most pools; raise surge for speed |
| **Blue-green** | `--enable-blue-green-upgrade --standard-rollout-policy=batch-node-count=2,batch-soak-duration=10s --node-pool-soak-duration=600s` (or `batch-percent=0.25`) | pools where you want a soak period and a way back; `--enable-surge-upgrade` switches back to surge |
Surge drain respects **PodDisruptionBudgets** and `terminationGracePeriodSeconds` for up to one hour; after that remaining Pods are forcefully evicted. Node pools cannot be rolled back after a successful surge upgrade. For blue-green, the blue pool is un-cordoned when you roll back; the default pool soak is one hour (3600 s) and the default batch soak is zero seconds. Blue-green deletion does not respect PDBs.

## 4. Channels, windows, exclusions
- **Release channels:** Rapid, Regular (default), Stable and Extended (long-term support; extra charges apply once a minor version enters extended support). Clusters enrolled in a channel get node auto-upgrades by default; you can block them with maintenance exclusions.
- **Maintenance window:** `gcloud container clusters update prod --maintenance-window-start=<RFC3339_TIME> --maintenance-window-duration=<DURATION> --maintenance-window-recurrence=<RRULE>`; a recurring window must be at least 4 hours (`4H`), and the RRULE is always in UTC.
- **Exclusions** pause upgrades: `--add-maintenance-exclusion-name=peak --add-maintenance-exclusion-start=... --add-maintenance-exclusion-end=... --add-maintenance-exclusion-scope=no_upgrades|no_minor_upgrades|no_minor_or_node_upgrades` (or `--add-maintenance-exclusion-until-end-of-support`). The "no upgrades" scope cannot exceed 90 days and Google recommends under 30 days, since longer risks missing critical patches; for minor-upgrade exclusions Google recommends under six months. Exclusions that block all upgrades need at least 48 hours of maintenance availability in a 92-day rolling window.
- Maintenance windows and exclusions can delay security patches, and GKE reserves the right to override maintenance policies for critical security vulnerabilities.

## 5. Sequencing and version skew
- Node pools can be no more than **two minor versions** behind the control plane; GKE upgrades nodes to align with the control plane.
- GKE may delay automatic upgrades when a new version impacts a group of clusters.
- Manual: `gcloud container clusters upgrade prod --master --cluster-version=<VERSION>` then `--node-pool=apps`.
- GKE publishes upgrade and security bulletin notifications to Pub/Sub when cluster notifications are enabled.

## Gotchas
- Surge upgrades need quota headroom for the extra nodes (CPUs, IPs) in the region.
- Check deprecation insights and recommendations before a minor upgrade.
- A taint without matching tolerations leaves a pool looking "broken"; Spot pools need a toleration for the Spot taint you add.

## Verify
- [ ] `node-pools describe` shows the upgrade settings you designed and a non-default service account.
- [ ] The maintenance policy and exclusions appear in `clusters describe`.
- [ ] Node pool versions are within two minors of the control plane (`kubectl get nodes` against the cluster's control plane version).

## Checked

2026-10-24, GKE node-pool upgrade strategy (concept and how-to), maintenance windows and exclusions (concept and how-to), release channels, cluster upgrades, node auto-provisioning and node pools pages on docs.cloud.google.com. Confirmed: surge and blue-green flags and defaults, one-hour PDB limit, rollback behaviour, window minimum of 4 hours and flags, exclusion flags and scope values, 90-day and recommended limits, channel list and default, two-minor version skew, NAP flags and config-file keys, machine attributes changeable with recreation. Corrected: machine type, disk type and size are not immutable (update recreates nodes); the window flag is `--maintenance-window-duration` (not an end time); the `no_upgrades` limit is 90 days (30 days is a recommendation); node auto-upgrade is not mandatory on channels. Removed unconfirmed claims: autorepair NotReady duration, extended-channel pricing figures, `fleet clusterupgrade`, notification event type names, per-flag autoscaling and shielded flags in the example.

Method: documentation only; no commands were run.
