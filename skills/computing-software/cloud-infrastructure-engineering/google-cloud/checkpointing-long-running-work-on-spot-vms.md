---
id: computing-software.cloud-infrastructure-engineering.google-cloud.checkpointing-long-running-work-on-spot-vms
name: checkpointing-long-running-work-on-spot-vms
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spot-vms, spot-checkpointing, preemption-notice, ml-training-checkpoints, idempotent-jobs, gcsfuse]
level: practitioner
status: docs-checked
description: "Make long jobs survive Spot preemption: periodic checkpoints to Cloud Storage, catching the ACPI preemption signal via metadata, resumable work units, and checkpoint sizing."
sources: ["https://cloud.google.com/compute/docs/instances/spot", "https://cloud.google.com/compute/docs/instances/create-use-spot", "https://cloud.google.com/storage/docs/gcs-fuse"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checkpointing long-running work on Spot VMs

Spot VMs give ~30 s notice. That is enough to flush a small marker, not to upload a 20 GB model
checkpoint. Design for loss of everything since the last periodic checkpoint.

## Pattern
1. **Periodic checkpoints**: every N minutes or N steps, write state to local SSD/PD, then upload
   to `gs://ckpt/<job>/<step>/` and write `LATEST` pointer last (atomic switch).
2. **On start**: read `LATEST`, restore, continue. Make work units idempotent (output named by
   input shard so reruns overwrite, not duplicate).
3. **On preemption notice**: stop taking new work, write a tiny progress marker.

## Detecting preemption
```bash
# watch metadata (returns TRUE when preempted)
curl -s -H "Metadata-Flavor: Google" \
  "http://metadata.google.internal/computeMetadata/v1/instance/preempted?wait_for_change=true"
```
Or shutdown-script metadata (`shutdown-script`) which runs on the ACPI G2 soft-off; Python apps can
trap SIGTERM from systemd.

## Choosing the interval
Expected lost work = interval/2 per preemption. If checkpoint write takes C seconds and the
preemption rate is r per hour, cost per hour ~ (C x checkpoints/h) + r x (interval/2).
Optimal interval ~ sqrt(2C / r) (Young's formula). E.g. C=60 s, r=0.2/h gives ~ 24 min.

## Framework support
- Training frameworks: use the framework's own checkpoint API and save model weights, optimizer state, RNG state and the data loader position.
- Batch / Spark: rely on task-level retries; Dataproc secondary workers default to standard preemptible VMs (Spot and non-preemptible secondary workers can be mixed in).

## Gotchas
- Prefer writing checkpoints locally and copying them to Cloud Storage in a background thread rather than writing straight through a gcsfuse mount during training.
- Keep a few checkpoints: a corrupted last checkpoint (preempted mid-upload) must not lose all progress.
- Lifecycle rule to delete old checkpoints after N days.

## Verify
- [ ] Killing the VM mid-job and restarting resumes from the last checkpoint with identical results.

## Checked

Checked 2026-10-27 against Spot VMs, Create and use Spot VMs (30-second shutdown window, preempted metadata key) and Dataproc secondary workers. Fixed: Dataproc secondary workers default to standard preemptible VMs, not Spot. The Young's-formula interval was recomputed (sqrt(2 x 60 s / 0.2 per h) is about 24 minutes). Removed framework-specific API names that no Google documentation page backs.

Method: documentation only; no commands were run.
