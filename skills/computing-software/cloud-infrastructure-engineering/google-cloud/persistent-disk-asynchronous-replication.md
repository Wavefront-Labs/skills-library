---
id: computing-software.cloud-infrastructure-engineering.google-cloud.persistent-disk-asynchronous-replication
name: persistent-disk-asynchronous-replication
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, persistent-disk, async-replication, persistent-disk-asynchronous-replication, cross-region-dr, consistency-groups, hyperdisk]
level: practitioner
status: docs-checked
description: "Replicate Persistent Disk or Hyperdisk across regions with Asynchronous Replication: create secondary disks, consistency groups, failover and failback for DR."
sources: ["https://cloud.google.com/compute/docs/disks/async-pd/about", "https://cloud.google.com/compute/docs/disks/async-pd/configure", "https://cloud.google.com/sdk/gcloud/reference/compute/disks/stop-async-replication"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persistent Disk Asynchronous Replication

Async replication copies a disk to a secondary region (a region pair). Typical target RPO is one minute for up to
12.5 GB of compressed changed blocks per minute; higher change rates push RPO above that. Used for
cross-region DR of VMs where application-level replication is not available. The documented disk types include
Balanced Persistent Disk, SSD Persistent Disk, Hyperdisk Balanced, Hyperdisk Balanced High Availability and
Hyperdisk Extreme (check the docs for current types and region pairs). A project can have at most 1000 disk pairs.

## Set up
```bash
# primary exists: data-1 in europe-west2-a
gcloud compute disks create data-1-dr --zone=europe-west1-b --size=500 --type=pd-balanced \
  --primary-disk=data-1 --primary-disk-zone=europe-west2-a
gcloud compute disks start-async-replication data-1 --zone=europe-west2-a \
  --secondary-disk=data-1-dr --secondary-disk-zone=europe-west1-b
```
Multi-disk apps: create a **consistency group** (resource policy) so all disks replicate to the same point:
```bash
gcloud compute resource-policies create disk-consistency-group app-cg --region=europe-west2
gcloud compute disks add-resource-policies data-1 --zone=europe-west2-a --resource-policies=app-cg
# also add secondaries to a CG in the secondary region before starting replication
```

## Failover
```bash
gcloud compute disks stop-async-replication data-1-dr --zone=europe-west1-b      # works on primary or secondary; stop-group-async-replication for a CG
gcloud compute instances create app-dr --zone=europe-west1-b --disk=name=data-1-dr,boot=no ...
```
After the primary region recovers, failback = create a new secondary in the original region from the
current disk and replicate back, then repeat failover in a maintenance window.

## Monitoring
Metric `compute.googleapis.com/disk/async_replication/time_since_last_replication` (RPO) and
`async_replication_state`; pick an alert threshold above your RPO target (for example 120 s).

## Gotchas
- If the primary is a non-boot disk with auto-delete, you cannot delete the VM or disk until replication is stopped or the disk is detached.
- Add primary disks to a consistency group before starting replication.
- Replication and the secondary disk are billed; see the Compute Engine pricing page.
- Boot disks are better rebuilt from images + config management than replicated.

## Verify
- [ ] RPO metric stays under target; a DR drill boots the app from secondaries.

## Checked

Checked 2026-10-27 against About Asynchronous Replication, Configure Asynchronous Replication, the gcloud reference for disks create, start-async-replication, stop-async-replication and stop-group-async-replication, and the Cloud Monitoring metrics list. Fixed the RPO statement (target one minute for up to 12.5 GB of changed blocks per minute) and the metric name (async_replication_state). Confirmed 1000 disk pairs per project, the deletion restriction with auto-delete, that stop works on primary or secondary, and the supported disk type list. Removed unconfirmed attach, crash-consistency and egress statements.

Method: documentation only; no commands were run.
