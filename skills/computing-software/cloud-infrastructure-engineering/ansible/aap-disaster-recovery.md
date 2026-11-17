---
id: computing-software.cloud-infrastructure-engineering.ansible.aap-disaster-recovery
name: aap-disaster-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, disaster-recovery-iac, aap-disaster-recovery, controller-backup, backup-restore]
level: advanced
status: docs-checked
description: "Plan Ansible Automation Platform disaster recovery: what a backup holds, SECRET_KEY, same-version restores, operator and installer backup commands, config-as-code rebuild."
sources: ["https://github.com/ansible/aap-docs/blob/main/downstream/modules/aap-hardening/proc-disaster-recovery-operations.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/ref-controller-backup-restore-clustered-environments.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/proc-backup-aap-container.adoc", "https://github.com/ansible/awx-operator/blob/devel/roles/backup/README.md", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AAP disaster recovery

## What must survive
| Item | Why |
|---|---|
| Backup of the platform database | holds the objects and the encrypted credentials |
| The `SECRET_KEY` (included in installer and operator backups) | decrypts the credentials stored in the database |
| Controller configuration under `/etc/tower` and manual projects | restored with a controller backup |
| Config-as-code repo | rebuild objects without a database restore |
| Installer inventory | reinstall with the same topology |

Backups contain the database and the secret key that decrypts credentials, so store them encrypted and limit access to platform administrators.

## Strategies
1. **Backup and restore**: take installer or operator backups, copy them off-site, restore onto fresh infrastructure. Always use the same versions of PostgreSQL and the platform for backup and restore.
2. **Rebuild from config as code**: install a clean platform and apply the objects from git with the `infra.aap_configuration` collection (it targets AAP 2.5+). Job history is not in git, so it is lost.
3. **Combine both**: restore for history, keep config as code as the fast clean rebuild.

How you run backups depends on the deployment:
- Containerized: `ansible-playbook -i <path_to_inventory> ansible.containerized_installer.backup`; the default backup directory is `./backups`, changed with `backup_dir`.
- RPM installer: `./setup.sh -b`, with `backup_dir` choosing the staging directory.
- Operator (AWX): an `AWXBackup` custom resource writes a backup to a PVC; an `AWXRestore` restores it.

## Runbook outline
1. Declare the incident and freeze changes.
2. If restoring to a new cluster, make sure the old cluster is shut down; two clusters can conflict when accessing the database.
3. Restore from the backup with a matching version (see the restore skills for the exact steps).
4. Repoint DNS or the load balancer.
5. Validate: project sync, a credential-using job, then re-enable schedules deliberately.
6. After a restore to new hostnames, fix the Controller URL and credentials used by Event-Driven Ansible; they break and rulebook activations fail until updated.

## Gotchas
- A restore to different hostnames: per-node controller backups are restored only to nodes with the same hostname as the backup.
- Restoring a containerized platform to different hostnames is documented as a workaround, not a recommended path.
- Test restores regularly; an untested backup is not a plan.

## Verify
- [ ] Last DR test date and the runbook version are recorded.

## Checked
2026-11-09. Checked against the ansible/aap-docs repository (hardening guide disaster-recovery module, controller clustered backup/restore reference, containerized backup procedure), the AWX operator backup role README and the infra.aap_configuration README. Confirmed: backup contains the database and secret key; same PostgreSQL and platform versions; containerized backup playbook and `backup_dir`; `./setup.sh -b`; AWXBackup/AWXRestore; shut down the old cluster first; per-node backups restore only to same-hostname nodes; EDA credentials break after a hostname change; collection targets AAP 2.5+.
Removed as unsupported: warm-standby Postgres replication recipe and RTO figures, hub content and subscription manifest rows, certificate and mesh peer address claims, "schedules fire on restore" claim, `/api/v2/ping/` step.
Method: documentation only; no commands were run.
