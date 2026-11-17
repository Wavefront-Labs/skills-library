---
id: computing-software.cloud-infrastructure-engineering.google-cloud.backup-and-dr-vaults-plans-restores-and-reporting
name: backup-and-dr-vaults-plans-restores-and-reporting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, backup-and-dr, backup-vault-create, backup-dr-setup, backup-plan-associations, backup-schedules, backup-dr-restore, restore-vm, backup-dr-monitoring, backup-reports, immutable-backups]
level: practitioner
status: docs-checked
description: "Protect VMs with Backup and DR Service: immutable backup vaults with enforced retention, backup plans and associations, and listing backups for restore tests."
sources: ["https://docs.cloud.google.com/backup-disaster-recovery/docs/concepts/backup-vault", "https://docs.cloud.google.com/backup-disaster-recovery/docs/cloud-console/compute/compute-instance-backup", "https://docs.cloud.google.com/sdk/gcloud/reference/backup-dr/backup-vaults/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup and DR: vaults, plans, restores and reporting

## 1. Backup vault (immutable storage)
```bash
gcloud backup-dr backup-vaults create prod-vault --project=<BACKUP_PROJECT> --location=europe-west2 \
  --backup-min-enforced-retention=30d --description="prod VM backups"
```
The vault is a regional, Google-managed resource. With enforced retention set, backups cannot be manually
deleted by you, any other user or Google until the period has passed. The minimum enforced retention is
mandatory at creation (between 1 day and 99 years); the gcloud value is a relative time such as `1d` or `p1m1d`.
Any backup plan using the vault must have retention equal to or longer than the vault minimum. You can
lock the setting with an effective date: before it you can adjust the minimum, afterwards nobody (not even a
Project Owner) can decrease it, only increase it. Keep vaults in a **separate backup project** with its own admins.
`--access-restriction` defaults to `within-org`; `--backup-retention-inheritance` takes
`inherit-vault-retention` (default) or `match-backup-expire-time`.

## 2. Backup plan and associations
```bash
gcloud backup-dr backup-plans create vm-daily --project=<BACKUP_PROJECT> --location=europe-west2 \
  --backup-vault=prod-vault \
  --resource-type=compute.googleapis.com/Instance \
  --backup-rule=rule-id=daily,retention-days=35,recurrence=DAILY,backup-window-start=1,backup-window-end=5
gcloud backup-dr backup-plan-associations create db-vm-1-assoc --location=europe-west2 \
  --resource=projects/<VM_PROJECT>/zones/europe-west2-a/instances/<VM_ID> \
  --backup-plan=projects/<BACKUP_PROJECT>/locations/europe-west2/backupPlans/vm-daily
```
Rule recurrence can be hourly, daily, weekly, monthly or yearly (hourly frequency has a six-hour default
minimum). Get the instance ID with `gcloud compute instances describe <VM> --zone=<ZONE> --format="value(id)"`.
To back up only boot disks, pass `--compute-instance-properties=boot-disk-only=true` to `backup-plans create`;
`disk-exclusion-labels=env:scratch` excludes matching disks.
Associate at scale with Terraform (`google_backup_dr_backup_plan`) rather than per VM.

## 3. Restore tests
```bash
gcloud backup-dr data-sources list --backup-vault=prod-vault --location=europe-west2 --project=<BACKUP_PROJECT>
gcloud backup-dr backups list --data-source=<DS> --backup-vault=prod-vault --location=europe-west2 --project=<BACKUP_PROJECT>
```
Follow the current restore page for Compute Engine instances for the restore options, and plan DNS and
application changes in the runbook.

## 4. Scope
Vaults managed from the Google Cloud console cover resources such as Compute Engine and Cloud SQL.
Workloads such as Oracle and Google Cloud VMware Engine use the appliance management console and its own vaults.

## Gotchas
- If the VM is in a different project from the vault, grant `roles/backupdr.computeEngineOperator` to the
  backup vault service agent within the VM's project.
- Backups cannot be deleted during enforced retention, so they incur storage charges for the full duration:
  test plans on small resources first and check the pricing page.

## Verify
- [ ] Every production VM has an association (list them by label).
- [ ] Quarterly restore drill restores a VM and the application starts.

## Checked
2026-10-28. Confirmed against the Backup vaults concept page (retention rules, lock, 1 day to 99 years,
access restriction, console versus appliance), the Compute Engine backup page (plan and association
commands, recurrence, selective disk flags, cross-project role) and the gcloud `backup-vaults create`
reference (flag formats and defaults). Removed: restore-to-new-VM defaults, log and report-sink claims
(restore and reports pages return 404), disk resource type, monthly rule example and a success-rate target.
Method: documentation only; no commands were run.
