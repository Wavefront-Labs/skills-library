---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spreading-spot-capacity-across-zones-and-machine-types
name: spreading-spot-capacity-across-zones-and-machine-types
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spot-vms, spot-zone-flexibility, spot-obtainability, regional-mig, instance-flexibility, any-single-zone]
level: practitioner
status: docs-checked
description: "Improve Spot VM obtainability: regional MIGs with flexible distribution, instance flexibility across machine types, bulk API with zone choice, and handling stockout errors."
sources: ["https://cloud.google.com/compute/docs/instance-groups/regional-mig-distribution-shape", "https://cloud.google.com/compute/docs/instance-groups/about-instance-flexibility", "https://cloud.google.com/compute/docs/instances/multiple/about-bulk-creation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spreading Spot capacity across zones and machine types

Spot capacity varies by zone and machine type and changes over time. Locking a fleet to one zone and
one type maximises preemptions and stockouts.

## Regional MIG with flexible shape and instance flexibility
```bash
gcloud compute instance-groups managed create spot-workers --region=us-central1 \
  --template=spot-tmpl --size=50 \
  --target-distribution-shape=any --instance-redistribution-type=none \
  --instance-selection="name=pref1,machine-type=n2-standard-8,machine-type=n2d-standard-8,rank=1" \
  --instance-selection="name=pref2,machine-type=c3-standard-8,machine-type=e2-standard-8,rank=2"
```
- `any`: the group picks zones that can supply the requested VMs (recommended for batch workloads that do not need high availability).
- `any-single-zone`: all VMs in one zone (avoids cross-zone egress and latency).
- `balanced`: prioritises creating VMs but tolerates imbalance when capacity is short.
- `even` is the default shape.
- Repeat `--instance-selection` per selection; a lower `rank` means higher preference. A redistribution type can only be set on a non-autoscaled regional MIG.

## Bulk instance API
```bash
gcloud compute instances bulk create --name-pattern="job-####" --count=100 --min-count=60 \
  --region=us-central1 --provisioning-model=SPOT --machine-type=n2-standard-8 \
  --location-policy=us-central1-a=allow,us-central1-b=allow,us-central1-c=allow,us-central1-f=allow \
  --target-distribution-shape=ANY
```
`--min-count` = succeed if at least that many obtained. `--target-distribution-shape` defaults to `ANY_SINGLE_ZONE` here, so set `ANY` to let VMs span zones.

## Batch / GKE
- Batch: `allocationPolicy.location.allowedLocations: ["regions/us-central1"]` and multiple `instances[]` policies.
- GKE: Spot node pools in a regional cluster with several machine types, or a GKE custom ComputeClass that lists machine and Spot options in priority order.

## Errors
`ZONE_RESOURCE_POOL_EXHAUSTED` = no capacity in that zone, retry in another zone or machine type.
A quota error on the `PREEMPTIBLE_CPUS` metric means dedicated preemptible quota is exhausted;
without it Spot VMs count against the regular CPUs quota.

## Verify
- [ ] Fleet reaches target size during a peak window; `list-instances` shows multiple zones/types.

## Checked

Checked 2026-10-27 against the gcloud reference for instance-groups managed create and instances bulk create, the regional MIG distribution shape page, the instance flexibility page, the Compute Engine resource usage page (PREEMPTIBLE_CPUS) and the VM creation troubleshooting page (ZONE_RESOURCE_POOL_EXHAUSTED). Fixed: the nonexistent set-instance-selections command (use repeated --instance-selection), the nonexistent bulk create flag --target-shape (the flag is --target-distribution-shape, default ANY_SINGLE_ZONE), the shape default (even) and the lower-case shape and location-policy values. Removed the unconfirmed STOCKOUT and QUOTA_EXCEEDED codes.

Method: documentation only; no commands were run.
