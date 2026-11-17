---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spot-vms-in-migs-with-on-demand-fallback
name: spot-vms-in-migs-with-on-demand-fallback
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spot-vms, spot-mig, mixed-spot-on-demand, managed-instance-groups, autoscaler, cost-optimisation]
level: advanced
status: docs-checked
description: "Serve traffic or run batch on Spot MIGs with an on-demand baseline: two MIGs behind one backend service, autoscaler settings, instance flexibility and preemption-aware draining."
sources: ["https://cloud.google.com/compute/docs/instance-groups/create-mig-with-spot-vms", "https://cloud.google.com/compute/docs/instance-groups/about-instance-flexibility", "https://cloud.google.com/load-balancing/docs/backend-service"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spot VMs in MIGs with on-demand fallback

## 1. Pattern: baseline + Spot burst
| MIG | Template | Autoscaler |
|---|---|---|
| `web-od` | standard provisioning | min = load needed if all Spot vanished (e.g. 4), max small |
| `web-spot` | `--provisioning-model=SPOT --instance-termination-action=DELETE` | min 0, max large, same signal |
Both are backends of one backend service; the LB spreads load, Spot carries the bulk.
```bash
gcloud compute instance-templates create web-spot-v7 --machine-type=n2-standard-4 \
  --provisioning-model=SPOT --instance-termination-action=DELETE \
  --image-family=web --image-project=<P> --no-address --service-account=<SA> --scopes=cloud-platform
gcloud compute instance-groups managed create web-spot --region=<R> --template=web-spot-v7 --size=0 \
  --target-distribution-shape=balanced \
  --instance-selection-machine-types=n2-standard-4,n2d-standard-4,c3-standard-4
gcloud compute instance-groups managed set-autoscaling web-spot --region=<R> \
  --min-num-replicas=0 --max-num-replicas=60 --target-cpu-utilization=0.6
gcloud compute backend-services add-backend web-bes --global --instance-group=web-spot --instance-group-region=<R> \
  --balancing-mode=UTILIZATION --max-utilization=0.7
```
Instance flexibility (several equivalent shapes) and `balanced`/`any` distribution raise the
chance of getting Spot capacity.

## 2. Preemption behaviour
- MIG autohealing/recreation replaces preempted VMs when capacity returns.
- Mass preemption in one zone moves load to on-demand + other zones; size the on-demand baseline for that.
- Connection draining on the backend service plus a shutdown script that fails health checks immediately shortens user impact.

## 3. Batch variant
For queue workers, scale both MIGs on Pub/Sub backlog (`--update-stackdriver-metric=pubsub.googleapis.com/subscription/num_undelivered_messages`)
with on-demand max kept low so the backlog is mostly drained by Spot.

## Gotchas
- The autoscaler on each MIG sees only its own VMs; two MIGs on CPU can oscillate — give the on-demand MIG a higher target so Spot scales first.
- A Spot template defaults to STOP on preemption; `DELETE` is set explicitly here so the MIG recreates instead of leaving stopped VMs.
- Stateful workloads (DB, caches with warm state) don't belong on Spot.

## Verify
- [ ] Under steady load, ≥ 70% of serving VMs are Spot (`list-instances` per MIG).
- [ ] Deleting all Spot VMs in a test keeps error rate within SLO while the baseline scales.

## Checked

Checked 2026-10-27 against the gcloud reference for instance-groups managed create, set-autoscaling and backend-services add-backend, the Create a MIG with Spot VMs page (STOP is the default preemption action, DELETE is optional) and the MIG instance flexibility page. Confirmed the flags in the example (--target-distribution-shape, --instance-selection-machine-types, --min-num-replicas, --max-num-replicas, --target-cpu-utilization, --update-stackdriver-metric, --instance-group-region, --balancing-mode, --max-utilization). Removed the unconfirmed claim that Spot VMs cannot use reservations or CUDs.

Method: documentation only; no commands were run.
