---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-backup-restore-and-upgrade
name: controller-backup-restore-and-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, controller-backup, awx-backup, backup-restore, controller-upgrade, awxbackup, awxrestore, awx-operator-backup, setup-sh-backup, containerized-backup, secret-key, pg-dump, postgresql-backup, disaster-recovery, aap-upgrade, operator-upgrade, migration, pvc-backup]
level: advanced
status: docs-checked
description: "Back up, restore and upgrade AWX/automation controller: AWXBackup/AWXRestore CRs, setup.sh -b/-r and containerized backup playbooks, SECRET_KEY, DR drills, safe upgrades."
sources: ["https://github.com/ansible/awx-operator/blob/devel/config/crd/bases/awx.ansible.com_awxbackups.yaml", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/rpm_installation/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/containerized_installation/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/operating_ansible_automation_platform/", "https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/database-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller backup, restore and upgrade

**Goal:** you can rebuild the controller on new infrastructure from last night's
backup with every credential still decryptable, and upgrade a minor/major version
with a tested rollback.

## 1. What a backup must contain
1. The PostgreSQL database (all config, job history, encrypted credentials).
2. The **`SECRET_KEY`** (operator: secret `<name>-secret-key`; RPM/containerized: the SECRET_KEY file, staged with the backup) — without it, every credential in the restored DB is unreadable.
3. Custom settings/certs (`/etc/tower/conf.d`, TLS, `custom_ca`), projects directory (manual projects, PVC), custom EE images in the hub (backed up separately).
Backing up the DB without the key is the classic unrecoverable backup.

## 2. Operator (Kubernetes)
```yaml
apiVersion: awx.ansible.com/v1beta1
kind: AWXBackup
metadata: {name: awx-backup-2026-10-15, namespace: awx}
spec:
  deployment_name: awx
  backup_pvc: awx-backup-claim          # or backup_storage_class / backup_pvc_namespace
  clean_backup_on_delete: false
  use_db_compression: true
```
Produces a timestamped backup directory on the PVC containing the database dump, the CR spec and
the secrets (including the SECRET_KEY and DB credentials). Schedule it with a CronJob
that `kubectl apply`s a dated CR, and copy the PVC contents off-cluster (restic/velero or `kubectl cp`).
Restore (same or new cluster with the operator installed):
```yaml
apiVersion: awx.ansible.com/v1beta1
kind: AWXRestore
metadata: {name: awx-restore, namespace: awx}
spec:
  deployment_name: awx                  # new AWX object name
  backup_name: awx-backup-2026-10-15    # backup_source: CR; or backup_pvc + backup_dir with PVC
```
The restore creates the AWX CR, the secrets and loads the DB. For an **external** DB the backup
still pg_dumps it; make sure `postgres_configuration_secret` points at the target DB before restoring.

## 3. RPM / containerized installers
```bash
# RPM: from the setup bundle dir, same inventory as install (backup mode stages
# /var/backups/automation-platform via backup_dir and includes the SECRET_KEY file)
./setup.sh -e 'backup_dest=/var/backups/aap' -b
./setup.sh -e 'restore_backup_file=/var/backups/aap/aap-backup-<date>.tar.gz' -r
# Containerized (2.5):
ansible-playbook -i inventory ansible.containerized_installer.backup
ansible-playbook -i inventory ansible.containerized_installer.restore
```
Backups are restored onto hosts with the **same inventory layout** (hostnames/roles); DR to new
hosts means reinstalling with the inventory updated and restoring on top. Keep the installer bundle
version that made the backup — restore with the same version, then upgrade.
Database-only quick backups between full ones: `pg_dump -Fc awx > awx.dump` on the DB host, plus the key file.

## 4. Upgrade
- **Operator**: read release notes (each operator version pins an AWX version), take an `AWXBackup`, bump `ref=`/`newTag` in kustomization, `kubectl apply -k .`, watch the operator log (it runs the database migrations). Jump at most across a few versions at a time; some releases require passing through an intermediate.
- **AAP**: download the new setup bundle, copy the old `inventory`, run `setup.sh` / the containerized `install` playbook — the installer upgrades in place (DB migrations, new images). 2.4 → 2.5 introduces the platform gateway: new inventory sections (`[automationgateway]`), new passwords, and the installer migrates auth settings.
- Before: cancel/let finish running jobs, disable schedules, note `ansible-core` version in the default EE (new AAP ships new EEs; your custom EEs keep their old core until rebuilt), take a backup, snapshot VMs/PVCs.
- After: run a known-good job template, check project syncs (Galaxy creds), check SSO login, re-enable schedules, update the `awx` CLI/collections to match.
Rollback = restore the backup onto the old version (operator: re-apply the old kustomization then `AWXRestore`; RPM: old bundle `-r`).

## 5. DR drill
Quarterly: restore into a scratch namespace/VM from the off-site copy, log in, open a credential's
"test" button (proves the key), run a check-mode job against a lab host, then destroy. Record the time it took.

## Gotchas
- Restoring into a cluster where an AWX with the same `deployment_name` exists fails or clobbers; delete first or use a new name.
- Backups contain secrets (SECRET_KEY, DB password); encrypt at rest and restrict the PVC/bucket.
- Job events make the DB large; run the cleanup management jobs so backups stay small and restores fast.
- Changing the DB password after backup without updating the secret → restore loads the DB but pods crash-loop on auth.
- Hub (galaxy_ng) and EDA have their own backups; a "platform" restore needs all of them from the same point in time.
- Downgrading AWX is unsupported; only restore-from-backup rolls back.

## Verify
- [ ] Backup artefact contains the DB dump **and** the secret key (operator: `secrets.yml`; RPM: tarball lists `SECRET_KEY`).
- [ ] A restore into a scratch environment lets you open and use an existing credential (no `$encrypted$` decryption errors in job output).
- [ ] After upgrade, `/api/v2/ping/` shows the new version, a demo job runs, SSO works, schedules are re-enabled.

## Checked

- 2026-10-31: AWXBackup/AWXRestore CRs and their spec fields (deployment_name required; backup_pvc,
  backup_pvc_namespace, backup_storage_class, clean_backup_on_delete, use_db_compression,
  backup_source CR|PVC, backup_name, backup_dir) confirmed in the awx-operator CRDs; the `<resourcename>-secret-key`
  secret confirmed in the operator admin guide; `ansible.containerized_installer.backup`/`.restore`,
  backup staging at /var/backups/automation-platform via `backup_dir`, the SECRET_KEY file in
  backups, `ansible-automation-platform-containerized-setup-bundle-<version>-<arch>.tar.gz` and
  2.4→2.5 gateway inventory changes confirmed in the AAP 2.5 RPM/containerized installation guides.
- Removed: the `tower-openshift-backup-<timestamp>/` file layout specifics (`tower.db`, `awx_object`,
  `secrets.yml`), the `-e 'use_compression=true'` installer flag (the CRD field `use_db_compression`
  is documented instead) and the `awx-manage migrate` command (replaced with "the operator runs
  the database migrations").
Method: documentation only; no commands were run.
