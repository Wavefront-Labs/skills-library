---
id: computing-software.cloud-infrastructure-engineering.google-cloud.backup-and-dr-service
name: backup-and-dr-service
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, backup-and-dr, backup-dr, backup-vault, backup-plans, immutable-backups, backup-retention, compute-engine-backup, disk-backup, cloud-sql-backup-vault, gke-backup, backup-for-gke, vmware-backup, database-backup, ransomware-protection, centralized-backup, restore-testing]
level: practitioner
status: docs-checked
description: "Centralise backups with Backup and DR Service: immutable vaults with enforced retention, plans for Compute Engine VMs and disks, Backup for GKE, database agents, tested restores."
sources: ["https://docs.cloud.google.com/backup-disaster-recovery/docs/concepts/backup-dr", "https://docs.cloud.google.com/backup-disaster-recovery/docs/concepts/backup-vault", "https://docs.cloud.google.com/sdk/gcloud/reference/backup-dr/backup-vaults/create", "https://docs.cloud.google.com/sdk/gcloud/reference/beta/container/backup-restore/backup-plans/create", "https://docs.cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/concepts/backup-for-gke"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Backup and DR Service

**Goal:** every VM, disk, database and GKE workload that matters is backed up on a schedule
into storage that an attacker with project Owner cannot delete, and you have restored from it on purpose.

## 1. Two generations of the product
- **Backup vaults + backup plans** (console-native): Compute Engine VMs/disks and Cloud SQL, with enforced-retention (immutable) vault storage. Use this for everything it supports.
- **Management console + backup/recovery appliance**: for resources managed through the appliance management console (for example Google Cloud VMware Engine VMs); a vault must allow appliance access for these (see the access restriction below).
- **Backup for GKE** is a GKE add-on with its own plans (`gcloud beta container backup-restore backup-plans`), separate from backup vaults; its delete protection comes from `--backup-delete-lock-days`.

## 2. Vault and plan
```bash
gcloud backup-dr backup-vaults create prod-vault --location=europe-west1 \
  --backup-min-enforced-retention=30d --access-restriction=within-org   # or within-project / within-org-but-unrestricted-for-ba / unrestricted
gcloud backup-dr backup-plans create vm-daily --location=europe-west1 --backup-vault=prod-vault \
  --resource-type=compute.googleapis.com/Instance \
  --backup-rule=rule-id=daily,retention-days=35,recurrence=DAILY,backup-window-start=22,backup-window-end=6 \
  --backup-rule=rule-id=weekly,retention-days=180,recurrence=WEEKLY,days-of-week=SUNDAY,backup-window-start=22,backup-window-end=6
gcloud backup-dr backup-plan-associations create app-1-assoc --location=europe-west1 \
  --backup-plan=vm-daily --resource=projects/<P>/zones/europe-west1-b/instances/app-1 --resource-type=compute.googleapis.com/Instance
```
- **Minimum enforced retention** is the immutability guarantee: backups cannot be deleted by anyone, including Google, before it elapses (set between 1 day and 99 years at vault creation); backup plans in the vault need retention equal to or longer than it. Backups incur standard storage charges for the whole period. You can also lock the setting so it can only be increased.
- The access restriction is permanent: `within-org` limits backup and restore to your organization, `within-project` to the project, `unrestricted` allows any project or organization.
- Plans attach per resource (association); automate association with labels or infrastructure as code.

## 3. Restore
- VM: `gcloud backup-dr backups restore` or console, restoring beside the original rather than overwriting, then swap. Disks restore as new disks for attach-and-copy.
- **Restore testing**: monthly, restore the most critical VM into an isolated VPC, boot, check the app, delete. Record it; auditors ask for evidence, and backups that were never restored are hypotheses.

## 4. Backup for GKE
Enable the Backup for GKE add-on on the cluster (see the Backup for GKE page), then:
```bash
gcloud beta container backup-restore backup-plans create prod-ns-daily --cluster=projects/<P>/locations/europe-west1/clusters/prod \
  --location=europe-west1 --selected-namespaces=payments,orders --include-volume-data --include-secrets \
  --cron-schedule="0 2 * * *" --backup-retain-days=30 --backup-delete-lock-days=7
```
Captures Kubernetes resources + PV data (PD snapshots); `--backup-delete-lock-days` (max 90, must be below `--backup-retain-days`, max 365) is the delete-lock window and `--locked` freezes the retention policy; cron times are UTC with a 10-minute minimum interval; restores map to a target cluster with conflict policies. Restore testing here means restoring to a scratch cluster.

## 5. Databases in VMs (legacy console path)
Use the **management console** and a **backup/recovery appliance** for resources it supports (see the Backup and DR concepts page for the supported database list). Prefer native managed backups (Cloud SQL, AlloyDB, Spanner) whenever the database is managed.

## Gotchas
- Vault immutability also blocks *you*: decommissioning a vault means waiting out retention on its last backup.
- Backup plans are regional; create plan and vault in the region of the resource.
- Compute Engine backups can be crash-consistent; databases should use native backups or the agent path.
- Deleting a VM does not delete its backups (good); clean up associations on decommission.

## Checked
2026-10-31. Confirmed against the Backup and DR concepts and backup vault pages, the gcloud reference for `backup-dr backup-vaults create`, `backup-dr backup-plans create`, `backup-dr backups restore` and `beta container backup-restore backup-plans create` (flags, 90/365-day limits, 10-minute minimum interval, UTC cron, access restriction values, enforced retention 1 day to 99 years). Removed unconfirmed: Actifio lineage, vault-deletion rule, 30-90 day advice, incremental-forever claim, Terraform resource name, restoreUser and computeEngineOperator roles, service agent address, add-on enable command, metric name. Changed the GKE command to `gcloud beta` (check_commands: beta-only).
Method: documentation only; no commands were run.

## Verify
- [ ] The vault's backup list shows daily entries for every protected VM; a deletion attempt inside enforced retention is refused.
- [ ] Restore of app-1 to an isolated network boots and passes the app health check; timing is recorded against the RTO.
- [ ] Backup for GKE restore into a scratch cluster recreates the namespace with PVC data intact.
- [ ] A monitoring alert on failed backup jobs fires in a test.
