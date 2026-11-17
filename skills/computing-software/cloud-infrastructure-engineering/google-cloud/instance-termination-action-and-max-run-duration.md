---
id: computing-software.cloud-infrastructure-engineering.google-cloud.instance-termination-action-and-max-run-duration
name: instance-termination-action-and-max-run-duration
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spot-vms, instance-termination-action, max-run-duration, termination-time, flex-start, provisioning-model]
level: practitioner
status: docs-checked
description: "Choose STOP vs DELETE when Spot VMs are preempted, and bound any VM's lifetime with --max-run-duration or --termination-time, including disk and billing consequences."
sources: ["https://cloud.google.com/compute/docs/instances/spot#termination-action", "https://cloud.google.com/compute/docs/instances/limit-vm-runtime", "https://cloud.google.com/sdk/gcloud/reference/compute/instances/create#--instance-termination-action"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance termination action and max run duration

## Spot termination action
```bash
gcloud compute instances create render-1 --zone=<Z> --provisioning-model=SPOT \
  --instance-termination-action=STOP     # or DELETE
```
| Action | After preemption | Cost while terminated | Use |
|---|---|---|---|
| `STOP` (default for Spot) | VM in TERMINATED, disks kept | no VM-hour charge; disks keep billing | stateful single VMs you restart later |
| `DELETE` | VM deleted (disks per auto-delete) | none | MIG/Batch/GKE fleets that recreate |

A MIG with Spot VMs recreates preempted VMs when capacity returns. You can stop and restart a
preempted Spot VM as many times as you like, as long as capacity is available.

## Limiting VM runtime (any provisioning model)
```bash
# run for at most 4 hours from start, then delete
gcloud compute instances create train-1 --zone=<Z> --max-run-duration=4h --instance-termination-action=DELETE
# or terminate at a timestamp
gcloud compute instances create demo-1 --zone=<Z> --termination-time=2027-01-20T18:00:00Z --instance-termination-action=STOP
gcloud compute instances describe train-1 --zone=<Z> --format="yaml(scheduling)"
```
`--max-run-duration` accepts 30s to 120d (for example `30m` or `1d2h3m4s`); set either it or
`--termination-time`, not both. Useful for: sandbox/demo VMs and training jobs with a hard budget.

## Gotchas
- The read-only `terminationTimestamp` is set when a VM with a limit enters RUNNING, cleared on stop
  or suspend, unchanged by reset or reboot, and recalculated on restart or resume (a duration is
  added to the latest start time; an absolute time must still be in the future).
- Shutdown scripts get up to 30 s on Spot preemption (best effort).
- `--instance-termination-action` is optional only for Spot VMs (default STOP); a non-Spot VM with a
  time limit must set it.
- A deleted VM is gone; persist outputs early.

## Verify
- [ ] `gcloud compute instances describe train-1 --zone=<Z> --format="yaml(scheduling)"` shows the limit and action.
- [ ] A test VM with a short `--max-run-duration` is terminated on schedule.

## Checked

Checked 2026-10-27 against Limit the run time of a VM, Spot VMs and the Compute Engine v1 API discovery document. Confirmed: --max-run-duration range 30s to 120d, --termination-time as an RFC 3339 timestamp, only one of the two, the termination action is optional only for Spot VMs (default STOP) and required otherwise, the terminationTimestamp lifecycle (cleared on stop or suspend, kept on reset or reboot, recalculated on restart), shutdown scripts up to 30 seconds on preemption. Fixed the wrong claim that the termination action is rejected without Spot or a limit. Removed the unconfirmed static-IP billing and Flex-start run-duration claims.

Method: documentation only; no commands were run.
