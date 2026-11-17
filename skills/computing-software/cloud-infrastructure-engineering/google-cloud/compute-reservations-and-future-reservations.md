---
id: computing-software.cloud-infrastructure-engineering.google-cloud.compute-reservations-and-future-reservations
name: compute-reservations-and-future-reservations
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, reservations, future-reservations, capacity-reservation, shared-reservations, committed-use-discounts]
level: practitioner
status: docs-checked
description: "Guarantee zonal capacity with on-demand and future reservations: create, share across projects, target specific reservations, track utilisation and auto-delete them."
sources: ["https://cloud.google.com/compute/docs/instances/reservations-overview", "https://cloud.google.com/compute/docs/instances/reservations-single-project", "https://cloud.google.com/compute/docs/instances/future-reservations-overview", "https://cloud.google.com/sdk/gcloud/reference/compute/reservations/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute reservations and future reservations

A reservation holds zonal capacity for a VM shape. You **pay for the reserved resources whether or not VMs use
them**, at the same on-demand rate as equivalent running VMs.

## 1. Create
```bash
gcloud compute reservations create batch-c3 --project=<P> --zone=europe-west2-b \
  --vm-count=20 --machine-type=c3-standard-22 \
  --require-specific-reservation \
  --share-setting=projects --share-with=<P2>,<P3>
# the API also has auto-delete fields (deleteAfterDuration, deleteAtTime) on the Reservation resource
# GPUs / local SSD must be declared to match
#   --accelerator=count=1,type=nvidia-l4 --local-ssd=size=375,interface=NVME
```
`--require-specific-reservation`: only VMs that name it consume it (prevents a random dev VM
eating prod capacity). Without it, any matching VM with affinity `any` (the default) uses it.

## 2. Consume
```bash
gcloud compute instances create w-1 --zone=europe-west2-b --machine-type=c3-standard-22 \
  --reservation-affinity=specific --reservation=projects/<P>/reservations/batch-c3
```
Instance templates take the same flags.

## 3. Utilisation
```bash
gcloud compute reservations describe batch-c3 --zone=europe-west2-b \
  --format='value(specificReservation.count,specificReservation.inUseCount,status)'
```
Monitor `compute.googleapis.com/reservation/...` metrics or the Reservations page; idle
reservations are pure cost — resize (`gcloud compute reservations update --vm-count`) or delete.

## 4. Future reservations
For capacity on a date (launch, Black Friday, training run):
```bash
gcloud beta compute future-reservations create bf-2026 --zone=europe-west2-b \
  --machine-type=n2-standard-16 --total-count=200 \
  --start-time=2026-11-25T00:00:00Z --end-time=2026-12-02T00:00:00Z \
  --auto-delete-auto-created-reservations
gcloud beta compute future-reservations describe bf-2026 --zone=europe-west2-b   # procurementStatus
```
Google Cloud reviews the request; `status.procurementStatus` moves through values such as `PENDING_APPROVAL`, `APPROVED`,
`PROCURING`, `PROVISIONING` and `FULFILLED` (or `DECLINED`/`FAILED`); at the start date it creates a
normal reservation. Submit well ahead of the date you need.

## Gotchas
- Shape must match exactly (machine type, min CPU platform, GPUs, local SSDs) or VMs land outside the reservation and may fail for capacity.
- Creating a reservation needs unused quota in the project; for a shared reservation the owner project consumes quota when the reservation is created and when it consumes the reserved resources.
- A reservation in zone b does nothing for a regional MIG that places VMs in zones a/c.

## Verify
- [ ] `inUseCount` equals the intended fleet size after rollout.
- [ ] A VM without the specific affinity does not consume capacity (`inUseCount` unchanged).

## Checked

Checked 2026-10-27 against About reservations, Reserve zonal resources for a single project, About future reservation requests, the gcloud reference for reservations create and update and beta future-reservations create, and the Compute Engine v1 API discovery document (procurementStatus values). Fixed: reservations are billed at the on-demand rate, there is no --delete-after-duration flag on gcloud reservations create (the API has deleteAfterDuration and deleteAtTime), and the future reservation status values. Confirmed --require-specific-reservation, --share-setting, --share-with, --vm-count, update --vm-count and the future reservation flags. Removed the unconfirmed CUD, Spot, GKE and calendar-mode claims.

Method: documentation only; no commands were run.
