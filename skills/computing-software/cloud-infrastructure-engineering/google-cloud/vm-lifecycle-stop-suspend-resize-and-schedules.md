---
id: computing-software.cloud-infrastructure-engineering.google-cloud.vm-lifecycle-stop-suspend-resize-and-schedules
name: vm-lifecycle-stop-suspend-resize-and-schedules
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, vm-lifecycle, suspend-resume, change-machine-type, instance-schedules, resource-policy-schedule, cost-optimisation]
level: practitioner
status: docs-checked
description: "Manage VM states: stop vs suspend vs reset, change machine type safely, and start/stop dev fleets on a timetable with instance schedule resource policies."
sources: ["https://cloud.google.com/compute/docs/instances/instance-life-cycle", "https://cloud.google.com/compute/docs/instances/suspend-resume-instance", "https://cloud.google.com/compute/docs/instances/changing-machine-type-of-stopped-instance", "https://cloud.google.com/compute/docs/instances/schedule-instance-start-stop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM lifecycle: stop, suspend, resize and schedules

## 1. States and what you pay
| Action | Memory | Billing while off | Command |
|---|---|---|---|
| stop | lost (clean OS shutdown) | disks, snapshots and attached external IPs still bill; no VM-hour charge | `gcloud compute instances stop vm --zone=<Z>` |
| suspend | saved to persistent storage (uses Persistent disk standard quota) | disks + saved memory storage | `gcloud compute instances suspend vm` / `resume vm` |
| reset | lost, hard reboot, no shutdown | n/a | `gcloud compute instances reset vm` |
| delete | — | nothing (unless `--keep-disks`) | `gcloud compute instances delete vm --keep-disks=boot` |
Suspend is not supported for VMs with GPUs or TPUs or with more than 208 GB of memory. For a VM with Local SSD,
`stop` and `suspend` require `--discard-local-ssd=true` (discard) or `--discard-local-ssd=false` (preserve, which costs extra and has limits).

## 2. Change machine type
```bash
gcloud compute instances stop app-1 --zone=<Z>
gcloud compute instances set-machine-type app-1 --zone=<Z> --machine-type=n2-standard-8
# custom: --custom-cpu=6 --custom-memory=24GB
gcloud compute instances start app-1 --zone=<Z>
```
In-place changes work only for VMs without Local SSD that are not in a MIG, and across series only
between first and second generation series (excluding T2A and A2). Moving from a first or second
generation series to a third generation or later series (C3, N4, M3 and later) needs the "move your
workload to a new instance" procedure. MIG members: change the template and roll out. Stopping a MIG
member can get it recreated.

## 3. Instance schedules (start/stop on a timetable)
```bash
gcloud compute resource-policies create instance-schedule dev-office-hours --region=europe-west2 \
  --vm-start-schedule='0 8 * * 1-5' --vm-stop-schedule='0 19 * * 1-5' --timezone=Europe/London
gcloud compute instances add-resource-policies dev-1 --zone=europe-west2-a --resource-policies=dev-office-hours
# Compute Engine service agent must be allowed to start/stop
PN=$(gcloud projects describe <P> --format='value(projectNumber)')
gcloud projects add-iam-policy-binding <P> \
  --member=serviceAccount:service-$PN@compute-system.iam.gserviceaccount.com --role=roles/compute.instanceAdmin.v1
```
Office-hours only (55 of 168 hours) cuts compute cost by about two-thirds.

## Gotchas
- A scheduled operation can run up to 15 minutes after the cron time; keep start and stop at least 15 minutes apart. Schedules apply to VMs in the policy's region; a VM follows one schedule.
- For VMs in a MIG, use schedule-based autoscaling or resize the MIG.
- Stop runs the shutdown script, which must finish before the VM stops; long drains need a pre-stop step in your tooling.
- Reserve a static external IP if clients pin the address.

## Verify
- [ ] `gcloud compute resource-policies describe dev-office-hours --region=<R>` lists attached VMs.
- [ ] Next morning: VMs `RUNNING` by 08:15; evening: `TERMINATED` by 19:15.

## Checked

Checked 2026-10-27 against Suspend and resume, Stop and start, Edit the machine type of a VM, Schedule a VM to start and stop, the gcloud reference for instances stop, set-machine-type and resource-policies create instance-schedule, and the IAM service agents page. Confirmed: suspend is unsupported with GPUs, TPUs or more than 208 GB of memory and stores memory in Persistent disk standard quota; Local SSD needs --discard-local-ssd; schedules can run up to 15 minutes late, need start and stop at least 15 minutes apart, one schedule per VM, and the Compute Engine service agent needs roles/compute.instanceAdmin.v1. Fixed the machine-type change section: in-place changes need no Local SSD and no MIG, and only work between first and second generation series.

Method: documentation only; no commands were run.
