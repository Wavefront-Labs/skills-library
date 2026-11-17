---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-backup-server-install-and-config-database
name: veeam-backup-server-install-and-config-database
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-install, veeam-postgresql, veeam-backup-server, configuration-database, sql-server, installation]
level: practitioner
status: draft
description: "Install a Veeam Backup & Replication server: sizing, PostgreSQL vs SQL Server configuration database, service account, ports, licence file and post-install checks."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/install_vbr.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/system_requirements.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/postgresql_instance_configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Install the Veeam backup server and configuration database

**Goal:** a backup server that is supported, recoverable and not a ransomware target.

## Before you start
- Check the system requirements page for your version (CPU, RAM per concurrent task, OS build). Rule of thumb: 4 cores / 8 GB minimum, plus about 1 core and 1-2 GB per 10 concurrent jobs if the server is also a proxy.
- Decide where it lives: a dedicated VM or physical box, **not domain-joined to production AD** (or joined to a separate management forest). Veeam's own best-practice guide recommends a workgroup or dedicated domain.
- Have the licence file (`.lic`) ready; without it the install runs as Community Edition (10 instance limit).

## Configuration database choice
| Option | When |
|---|---|
| Bundled **PostgreSQL** (default since v12) | New installs; no SQL licence needed, no 10 GB Express cap |
| Existing **Microsoft SQL Server** | You already run SQL with DBA backup/HA; Express is capped at 10 GB per DB |

- With bundled PostgreSQL, run the hardware-aware tuning after install: `Set-VBRPSQLDatabaseServerLimits` (PowerShell) and restart the PostgreSQL service so `shared_buffers` and friends match the host RAM.
- Migrating SQL to PostgreSQL later is done with Configuration Backup + restore into a server pointed at PostgreSQL (`Configuration Database Connection Settings` utility to repoint).

## Install
1. Mount the ISO, run Setup, choose **Install Veeam Backup & Replication**.
2. Accept defaults for components (console, catalog, mount server) unless you split roles.
3. Service account: LocalSystem is fine for a workgroup server; use a dedicated account only if a remote SQL requires Windows auth.
4. Keep default ports (9392 console, 9401 secure mount, 6160/6162 installer/transport) or document changes; firewall rules are created automatically.
5. Enter the licence file, finish, then install the latest cumulative patch before adding any infrastructure.

## Post-install checklist
- Configure **Configuration Backup** to a repository that is not on the backup server itself, with encryption enabled (needed to keep stored credentials).
- Enable MFA for console users (Users and Roles) and add only named admin accounts.
- Set email notifications (General Options > Notifications).
- Exclude Veeam folders and processes from AV per Veeam KB1999.

## Verify
`Get-VBRServer` lists the local server; a test configuration backup completes; console connects from an admin workstation on port 9392.
