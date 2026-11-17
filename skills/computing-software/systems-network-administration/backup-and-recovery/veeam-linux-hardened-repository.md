---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-linux-hardened-repository
name: veeam-linux-hardened-repository
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [hardened-repository, veeam, immutable-backup, xfs-reflink, single-use-credentials, backup-immutability, linux]
level: advanced
status: docs-checked
description: "Veeam Linux hardened repository: immutability period, single-use or certificate authentication, non-root SSH account and sudoers handling, role restrictions."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/hardened_repository.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/hardened_repository_deploy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux hardened repository (Veeam)

**Goal:** a Linux-based backup repository whose backup files cannot be modified or deleted during an immutability period, even if the Veeam server is compromised.

## What the documentation states
- **Immutability:** when you add the repository you specify the period during which backup files must be immutable. In that period files cannot be moved, modified or deleted, but can be copied.
- **Authentication:** you choose the method used to authenticate connections.
  - *Single-use credentials*: used once to deploy Veeam Data Mover while adding the Linux server; they are not stored in the backup infrastructure, so an attacker who compromises the Veeam server cannot obtain them.
  - *Certificate-based*: no user name or password; available for hardened repositories deployed from the Veeam Infrastructure Appliance, recommended where Kerberos is disabled/unavailable or for enhanced security.
- Veeam uses SHA256RSA self-signed certificates with a 2048-bit RSA key to interact with the repository.
- For security reasons you cannot assign other roles to a hardened repository, except VMware backup proxy in Network mode.

## Adding a server not prepared with the Infrastructure Appliance
You must authenticate with SSH. On the Access step of the New Linux Server wizard:
1. Give single-use SSH credentials for a **non-root** account that has a home directory on the Linux server.
2. If the account is not in sudoers, select "Use su if sudo fails" and enter the root password.
3. If you added the account to sudoers, remove it from the file after the server is added.

Prepare the server with the Veeam Infrastructure Appliance, with the backup server as hardened repository, or manually on a supported OS (see the requirements page in the Veeam guide).

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "Hardened Repository" and "Adding Hardened Repositories" (build 13.1.2.57).
Removed (not on those pages): `chattr +i` mechanism, XFS/reflink and mkfs/fstab commands, ISO and Ubuntu/RHEL claims, the "disable SSH, BMC, NTP, firewall" hardening list, retention examples of 14-30 days, extended-lock capacity note, 3-2-1-1-0 remark and the Verify steps.
Method: documentation only; no commands were run.
