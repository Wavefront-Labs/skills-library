---
id: computing-software.cloud-infrastructure-engineering.google-cloud.vm-deletion-protection-and-auto-delete-disks
name: vm-deletion-protection-and-auto-delete-disks
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, vm-deletion-protection, auto-delete-disks, deletion-protection, data-loss-prevention]
level: practitioner
status: docs-checked
description: "Protect Compute Engine VMs and their data from accidental deletion: deletion protection flag, disk auto-delete settings, IAM and deny guards, and the cases it does not cover."
sources: ["https://cloud.google.com/compute/docs/instances/preventing-accidental-vm-deletion", "https://cloud.google.com/sdk/gcloud/reference/compute/instances/set-disk-auto-delete", "https://cloud.google.com/compute/docs/disks/add-persistent-disk"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM deletion protection and auto-delete disk settings

## Deletion protection
```bash
gcloud compute instances create db-01 --zone=<Z> --deletion-protection ...
gcloud compute instances update db-01 --zone=<Z> --deletion-protection      # enable
gcloud compute instances update db-01 --zone=<Z> --no-deletion-protection   # must do before delete
gcloud compute instances describe db-01 --zone=<Z> --format="value(deletionProtection)"
```
Delete attempts on a protected VM are rejected until you disable the flag.

Does **not** protect against: shutting down from inside the VM, stop, reset, suspend, removal for
fraud and abuse, or project termination. It applies to regular and preemptible VMs, cannot be set on
VMs in a managed instance group (it can on unmanaged instance groups) and cannot be set in instance templates.

## Disk auto-delete
Boot disks default to `autoDelete=true` (deleted with the VM; `--no-boot-disk-auto-delete` turns it off). Disks created
with the VM (`--create-disk`) default to yes; existing disks attached at creation with `--disk` default to no. Auto-delete does not apply once a disk is detached.
```bash
gcloud compute instances describe db-01 --zone=<Z> --format="table(disks[].deviceName,disks[].autoDelete)"
gcloud compute instances set-disk-auto-delete db-01 --zone=<Z> --disk=db-01-data --no-auto-delete
gcloud compute instances delete old-vm --zone=<Z> --keep-disks=data      # one-off keep
```

## Layered guards
- Snapshot schedules on data disks.
- IAM: give operators a custom role without `compute.instances.delete`, or
- an IAM deny policy on `compute.googleapis.com/instances.delete` (a supported deny permission).
- Project liens against project deletion.
- Terraform: `deletion_protection = true` on `google_compute_instance` and `lifecycle { prevent_destroy = true }`.

## Gotchas
- `terraform destroy` fails until deletion_protection is false in config and applied.
- `terraform destroy` on a protected instance also fails (documented in the `google_compute_instance` resource).

## Verify
- [ ] `gcloud compute instances delete` on a protected VM fails; data disks show `autoDelete: False`.

## Checked

Checked 2026-10-27 against Prevent accidental VM deletion, the gcloud reference for instances create, update, delete and set-disk-auto-delete, the IAM deny-permissions support list and the google_compute_instance Terraform documentation. Confirmed the flags, the list of actions deletion protection does not prevent (shutdown from inside the VM, stop, reset, suspend, fraud and abuse removal, project termination), no support for MIG VMs or instance templates, and the auto-delete defaults (boot disk and --create-disk yes, attached --disk no). Removed the exact error text, the non-boot-disk claim and the tag-condition deny detail, which the documentation does not support.

Method: documentation only; no commands were run.
