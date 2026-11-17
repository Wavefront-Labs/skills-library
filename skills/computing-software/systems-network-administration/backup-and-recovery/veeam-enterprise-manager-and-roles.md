---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-enterprise-manager-and-roles
name: veeam-enterprise-manager-and-roles
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, enterprise-manager, role-based-access, self-service-restore, rbac, four-eyes-authorization]
level: practitioner
status: draft
description: "Use Veeam Backup Enterprise Manager for multi-server views, delegated restores and roles, and set B&R console roles, MFA and four-eyes authorization."
sources:
  - https://helpcenter.veeam.com/docs/backup/em/introduction.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/four_eyes_authorization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enterprise Manager and role-based access

## Enterprise Manager (EM)
A web console (port 9443) that aggregates multiple backup servers: job status, reporting, licence management, and **self-service restore**.
- Install on a separate server (or the backup server in small sites); add each B&R server under Configuration > Backup Infrastructure.
- Roles: Portal Administrator, Portal User, Restore Operator. Assign AD groups, not users.
- **Restore scopes**: give the service desk a Restore Operator role limited to certain VMs and to file-level restore only, optionally "restore to original location only".
- Self-service: application owners restore their own VM files, Exchange items or SQL databases without console access.
- EM also hosts the encryption **key loss protection** (password recovery for encrypted backups when a password is lost); enable it before you need it.

## B&R console roles
Users and Roles in the console: Veeam Backup Administrator, Backup Operator (start/stop jobs), Restore Operator, Backup Viewer, Tape Operator.
- Enable **MFA** for all users; use a service account exemption only for automation.
- Turn on **four-eyes authorization** (v12+): deleting backups or changing users requires a second admin to approve.
- Set auto-logoff after idle time.

## Gotchas
- EM indexes guest files only if guest indexing is on in the jobs.
- Removing a B&R server from EM loses its historical reporting.

## Verify
A Restore Operator logs into EM and can restore a file only from in-scope VMs; deleting a backup in the console creates a pending approval request.
