---
id: computing-software.cloud-infrastructure-engineering.ansible.scheduled-controller-backups-and-retention
name: scheduled-controller-backups-and-retention
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, controller-backup, backup-retention, scheduled-backup, awxbackup, awx-operator, cronjob, containerized-installer]
level: advanced
status: docs-checked
description: "Plan scheduled controller/AWX backups: operator AWXBackup resources and variables, installer backups on VMs, what is captured, retention, and restore proof."
sources: ["https://raw.githubusercontent.com/ansible/awx-operator/devel/roles/backup/README.md", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/proc-backup-aap-container.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/proc-backup-aap-rpm.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/con-aap-backup-recommendations.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled controller backups and retention

Goal: a restorable controller backup exists on a regular schedule, old ones are pruned to a policy,
and copies live somewhere that survives losing the cluster or host.

Red Hat recommends backing up at least before upgrading the platform, before upgrading the OpenShift
cluster, and once per week (particularly if automatic upgrades are enabled).

## What a backup contains
- Operator (AWXBackup): the AWX custom resource spec values, a PostgreSQL database backup, the `secret_key`, `admin_password` and `broadcast_websocket` secrets, and the database configuration.
- Containerized installer: archives of PostgreSQL databases, configuration files and data files.
Keep backups as protected as a credential store, since they include secrets.

## Operator: AWXBackup resources
```yaml
apiVersion: awx.ansible.com/v1beta1
kind: AWXBackup
metadata:
  name: awxbackup-2026-11-09
  namespace: my-namespace
spec:
  deployment_name: mytower
  backup_pvc: awx-backup-volume-claim   # optional pre-created PVC
  clean_backup_on_delete: true
```
`kubectl apply -f` creates the backup; the resulting PVC holds a tar usable to restore to a new
deployment, and later backups are separate tars on the same PVC. Variables from the role README:
- `backup_pvc`, or `backup_storage_class` plus `backup_storage_requirements` (for example 20Gi) to create one; with neither, the default storage class is used.
- `backup_pvc_namespace`: store in another namespace (the same must be given on restore).
- `clean_backup_on_delete: true`: deleting the AWXBackup object deletes its `backupDirectory` on the PVC, so retention on objects is retention on disk.
- `pg_dump_suffix`: extra pg_dump arguments, for example `--exclude-table-data 'main_jobevent*'` to shrink the dump.
- `postgres_label_selector`, `image_pull_policy`, `backup_resource_requirements`.
To schedule, create AWXBackup objects with a Kubernetes CronJob (or any scheduler) using a service account allowed to create and delete them, and delete the oldest objects to keep your retention count.

## VM installs
- RPM-based: `./setup.sh -e 'backup_dir=/ansible/mybackup' -e 'use_compression=True' @credentials.yml -b` writes `<platform_installation_directory_name>.tar.gz` under `backup_dir`.
- Containerized: `ansible-playbook -i <inventory> ansible.containerized_installer.backup`. Use the installer that matches the installed version; backup works only with the PostgreSQL versions supported by that version. Defaults to `./backups`; change with `backup_dir`. Compression variables: `use_archive_compression`, `use_db_compression` (and per-component variants).
- Content in Azure Blob Storage or Amazon S3 is backed up through the vendor, not by the installer.
Schedule these runs from cron or from another automation system and copy results off the host.

## Gotchas
- A backup PVC on the same storage as the database protects against bad upgrades, not storage loss; keep an off-cluster copy.
- Check that each backup completed before pruning older ones.

## Verify
- [ ] A backup object or archive exists per scheduled run and the retention count holds.
- [ ] Periodically restore the latest backup into a scratch environment and run a job.

## Checked

- Date: 2026-11-09. Sources: ansible/awx-operator devel roles/backup/README.md; ansible/aap-docs main (backup recommendations, RPM and containerized backup procedures).
- Confirmed: contents of operator and containerized backups, AWXBackup manifest fields and role variables, `clean_backup_on_delete` behaviour, pg_dump_suffix example, setup.sh and containerized backup commands, compression variables, installer-version and PostgreSQL caveats, vendor-managed object storage note, recommended backup moments.
- Removed unconfirmed claims: the full CronJob manifest (image, RBAC and retention pipeline), AWXBackup status conditions, `AutomationControllerBackup` field parity, Velero/OADP copy, the `find -mtime` pruning command and 14-day policy, the `automation-platform-backup-<date>.tar.gz` file name, SECRET_KEY stored in clear, running cleanup system jobs to keep backups small, 2.4/2.5 version labels.

Method: documentation only; no commands were run.
