---
id: computing-software.cloud-infrastructure-engineering.ansible.restoring-controller-to-a-new-cluster
name: restoring-controller-to-a-new-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, controller-restore, restore-new-cluster, cross-cluster-restore, awxrestore, disaster-recovery, secret-key, awx-operator]
level: sme
status: docs-checked
description: "Restore AWX or automation controller from backup into a different Kubernetes cluster or new VMs: AWXRestore, backup PVC, setup.sh -r, and post-restore cleanup."
sources: ["https://github.com/ansible/awx-operator/blob/devel/roles/restore/README.md", "https://github.com/ansible/awx-operator/blob/devel/roles/backup/README.md", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/con-controller-restore-different-cluster.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/ref-controller-backup-restore-clustered-environments.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/proc-restore-aap.adoc", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/proc-controller-cluster-deprovision-instances.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring controller to a new cluster

Goal: the old cluster is gone or being migrated; bring objects and job history up on new infrastructure with credentials still decryptable.

## What a backup holds
- Operator backup: the `spec` of the AWX custom resource, a PostgreSQL backup, the `secret_key`, `admin_password` and `broadcast_websocket` secrets, and the database configuration.
- Installer (clustered) backup: a database dump, UI artifacts (inside the dump), the controller configuration from `/etc/tower`, the secret key and manual projects.
- Job output and job events live in the database, so they come back with it. Instance groups are not created by a restore: resources that used groups probably need reassigning to groups that exist on the new cluster.

## Operator: restore into a cluster
1. The awx-operator must already be deployed in the target cluster. Pre-create the target namespace (`kubectl create ns <namespace>`); do not delete a namespace that holds the backup PVC, since that deletes the backup too.
2. Before restoring over an existing deployment, delete the old AWX CR and the old database PVC (named like `postgres-<postgres version>-<deployment-name>-postgres-<postgres version>-0`).
3. The backup must be on a PVC the restore can see. Find its values on the AWXBackup object: `status.backupDirectory` and `status.backupClaim`.
4. Apply an `AWXRestore`:
```yaml
apiVersion: awx.ansible.com/v1beta1
kind: AWXRestore
metadata: {name: restore1, namespace: my-namespace}
spec:
  deployment_name: mytower            # the AWX deployment to create and restore into
  backup_pvc: awx-backup-volume-claim
  backup_dir: /backups/tower-openshift-backup-2021-04-02-03:25:08
```
`backup_name: <AWXBackup name>` can be used instead of `backup_pvc` and `backup_dir` while the AWXBackup object still exists. If a custom Postgres configuration secret was used, set `postgres_configuration_secret`.
5. The restored `admin_password_secret` value replaces the password of the `admin_user` user.

## VM installs
Run the installer restore: `./setup.sh -e 'restore_backup_file=/path/to/backup.tar.gz' -r`. If the backup TAR sits next to `setup.sh`, the restore finds it; `restore_backup_file` is only needed to point elsewhere. Use the latest installer of the same minor version as the platform that took the backup. Per-node controller backups restore only to nodes with the same hostname as the backup.

Containerized: `ansible-playbook -i <path_to_inventory> ansible.containerized_installer.restore` (backup directory `./backups` by default, `backup_dir` to change). Restoring to different hostnames is documented as a workaround only.

## After restore
- If restoring to a new cluster, shut the old cluster down first; two clusters can conflict when accessing the database.
- Remove instances that no longer exist: stop the services on that instance, then from another instance run `awx-manage deprovision_instance --hostname=<name used in inventory>` and restart services on the rest.
- Moving to new hostnames breaks the platform credentials set up for Event-Driven Ansible; update the Controller URL and credentials by hand so rulebook activations work again.
- Check that a project sync with a git credential works; it proves the secret key was restored correctly.

## Verify
- [ ] Only the new instances are listed in the Instances page.
- [ ] A job using a machine or vault credential succeeds.
- [ ] Job history from before the backup is visible.

## Checked
2026-11-09. Checked against the AWX operator restore and backup role READMEs and the ansible/aap-docs modules for restore to a different cluster, clustered backup and restore, `setup.sh` restore, containerized restore and instance deprovisioning. Confirmed the AWXRestore fields, status fields to read, CR/PVC cleanup, namespace pre-creation, `restore_backup_file`/`-r`, same-hostname rule, and EDA credential breakage.
Removed as unsupported: Velero/OADP and `kubectl cp` helper-pod transfer, the "do not create an AWX CR" instruction as worded, `./setup.sh -r` on "2.4" version labelling, webhook, `host_config_key` and SSO redirect claims, `awx-manage list_instances` checks, receptor peer re-pointing, the claim that a wrong SECRET_KEY restore "succeeds" silently, and the external-database remark.
Method: documentation only; no commands were run.
