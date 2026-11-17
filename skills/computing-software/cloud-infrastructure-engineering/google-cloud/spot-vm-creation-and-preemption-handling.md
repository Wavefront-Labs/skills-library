---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spot-vm-creation-and-preemption-handling
name: spot-vm-creation-and-preemption-handling
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spot-vms, spot-vm-creation, provisioning-model, preemption-notice, shutdown-script-spot, graceful-shutdown, checkpointing]
level: practitioner
status: docs-checked
description: "Create Spot VMs with the right termination action and run-duration limits, detect the 30-second preemption notice, and checkpoint work in shutdown handlers."
sources: ["https://cloud.google.com/compute/docs/instances/create-use-spot", "https://cloud.google.com/compute/docs/instances/spot", "https://cloud.google.com/compute/docs/instances/limit-vm-runtime", "https://cloud.google.com/compute/docs/shutdownscript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spot VM creation and preemption handling

## 1. Create
```bash
gcloud compute instances create render-1 --zone=<Z> --machine-type=c3-standard-8 \
  --provisioning-model=SPOT --instance-termination-action=DELETE \
  --image-family=debian-12 --image-project=debian-cloud \
  --metadata-from-file=shutdown-script=./on-preempt.sh
```
| Flag | Meaning |
|---|---|
| `--provisioning-model=SPOT` | Spot (no max runtime, unlike legacy `--preemptible` 24 h) |
| `--instance-termination-action=STOP` | default for Spot; VM stays TERMINATED, no VM-hour charge, disks keep billing; restart manually or via automation |
| `--instance-termination-action=DELETE` | nothing left behind; best for stateless batch |
| `--max-run-duration=4h` / `--termination-time=...` | self-terminate (works for standard VMs too) |
Spot VMs cannot live migrate or be set to automatically restart after a host event, are excluded from the Compute Engine SLA, and can be preempted at any time.

## 2. Detect preemption
Google sends ACPI soft-off with **~30 seconds** before hard stop.
```bash
MD=http://metadata.google.internal/computeMetadata/v1/instance
curl -s -H 'Metadata-Flavor: Google' "$MD/preempted?wait_for_change=true"          # TRUE when preempted
curl -s -H 'Metadata-Flavor: Google' "$MD/maintenance-event?wait_for_change=true"  # host maintenance events
```
A sidecar loop on these lets the app stop pulling new work immediately.

## 3. Shutdown handler
```bash
#!/bin/bash
# on-preempt.sh — must finish well under 30 s
systemctl kill -s SIGTERM worker.service      # worker flushes current item
timeout 20 gcloud storage cp /var/work/checkpoint.bin gs://<B>/ckpt/$(hostname).bin || true
```
Design work so losing up to N minutes is fine: idempotent tasks, small units, periodic
checkpoints to GCS, a queue (Pub/Sub, Cloud Tasks) that redelivers unacked work.

## 4. Observe
```bash
gcloud compute operations list --filter="operationType=compute.instances.preempted"
```
Track preemption rate per zone/machine type and move to less contended shapes.

## Gotchas
- Shutdown scripts are best effort; the 30 s includes OS shutdown. Large uploads will not finish.
- `STOP` Spot VMs do not come back on their own — pair with a MIG (autohealing recreates) or a scheduler.
- Spot capacity can be unavailable at create time (`ZONE_RESOURCE_POOL_EXHAUSTED`); retry in other zones or types.
- Spot VMs use standard quota unless you request dedicated preemptible quota for a region; once granted, Spot VMs in that region can only use the preemptible quota.

## Verify
- [ ] `gcloud compute instances describe render-1 --format='value(scheduling.provisioningModel,scheduling.instanceTerminationAction)'` → `SPOT DELETE`.
- [ ] Stopping the test VM runs the shutdown script and the checkpoint lands in GCS.

## Checked

Checked 2026-10-27 against the Compute Engine documentation (Spot VMs, create and use Spot VMs, limit VM run time, shutdown scripts, VM creation troubleshooting, resource usage and quotas) and the Compute Engine v1 API discovery document. Confirmed: Spot VMs cannot live migrate or be set to restart after host events and are excluded from the SLA; the default termination action is STOP and a stopped Spot VM has no VM-hour charge while disks keep billing; the preemption shutdown script runs for up to 30 seconds after the ACPI soft-off; the preempted metadata key and wait_for_change; the compute.instances.preempted operation filter; the preemptible quota behaviour; ZONE_RESOURCE_POOL_EXHAUSTED. Removed unconfirmed claims (CUD and sustained-use exclusion, the audit-log methodName query, simulate-maintenance-event for Spot, the maintenance-event enum string).

Method: documentation only; no commands were run.
