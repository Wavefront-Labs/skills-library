---
id: computing-software.cloud-infrastructure-engineering.google-cloud.mig-instance-flexibility-mixed-machine-types
name: mig-instance-flexibility-mixed-machine-types
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, managed-instance-groups, instance-flexibility, mixed-machine-types, capacity, spot-vms, obtainability]
level: advanced
status: docs-checked
description: "Make MIGs obtain capacity reliably by letting them choose from several machine types with ranked instance selections, distribution shapes and Spot, and size the autoscaler for it."
sources: ["https://cloud.google.com/compute/docs/instance-groups/about-instance-flexibility", "https://cloud.google.com/sdk/gcloud/reference/compute/instance-groups/managed/create", "https://cloud.google.com/compute/docs/instance-groups/regional-mig-distribution-shape"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MIG instance flexibility (mixed machine types)

When one machine type is short in a zone (GPUs, Spot, new families), a MIG with a single type
keeps retrying. An **instance flexibility policy** lets it pick from a list.

## 1. Create with ranked selections
```bash
gcloud compute instance-groups managed create render-mig --region=us-central1 \
  --template=render-tmpl --size=40 \
  --target-distribution-shape=any \
  --instance-selection=name=preferred,machine-type=c3-standard-22,rank=1 \
  --instance-selection=name=fallback,machine-type=n2-standard-24,machine-type=n2d-standard-24,rank=2
# simple unranked form
#   --instance-selection-machine-types=n2-standard-16,n2d-standard-16,c3-standard-22
```
`--instance-selection-machine-types` is a single unranked selection; if no selection is given, the template's machine type is used. Everything else (image, disks, SA) comes from the template.
Lower `rank` = higher preference; the MIG checks availability of all configured machine types and ranks together and provisions from the most preferred rank that has capacity.

## 2. Distribution shape matters
| Shape | Behaviour |
|---|---|
| `even` (default) | VM counts across zones differ by at most 1 — least flexible |
| `balanced` | prioritises creating VMs; similar to even when resources are available, can skew under constraints |
| `any` | picks zones where capacity is available — recommended for batch workloads |
| `any-single-zone` | all VMs in one zone (avoids cross-zone traffic) |

## 3. Workload and autoscaler fit
- Keep alternatives near the same vCPU/memory, or have the app adapt its worker count from `nproc`.
- Images and disks must work on every machine type listed (x86 vs Arm, gVNIC, disk types each family supports).
- Combine with Spot in the template for cheap batch; on-demand fallback lives in a second MIG (see Spot-in-MIGs).

## Gotchas
- Mixing families with different disk support (for example Persistent Disk-only and Hyperdisk-only families) can fail for the incompatible ones; group compatible families.
- Load balancers see heterogeneous backends — prefer utilization-based balancing.

## Verify
- [ ] `gcloud compute instances list --filter="name~render-mig" --format="table(name,machineType.basename(),zone.basename())"` shows the mix.
- [ ] MIG `status.isStable` becomes true at target size during a capacity shortage test (e.g. ask for more than one family offers).

## Checked

Checked 2026-10-27 against About instance flexibility, the regional MIG distribution shape page and the gcloud reference for instance-groups managed create. Confirmed --instance-selection (repeatable, name, machine-type, rank) and --instance-selection-machine-types, lower rank means higher preference, the four distribution shapes and their descriptions, the default even shape, and status.isStable. Fixed the verification command (list-instances has no machine type column). Removed unconfirmed CUD, autoscaler and load balancing claims.

Method: documentation only; no commands were run.
