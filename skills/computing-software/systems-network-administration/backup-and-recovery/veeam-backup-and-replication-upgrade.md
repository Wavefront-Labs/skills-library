---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-backup-and-replication-upgrade
name: veeam-backup-and-replication-upgrade
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-upgrade, upgrade-planning, configuration-backup, compatibility-matrix]
level: practitioner
status: docs-checked
description: "Upgrade Veeam Backup & Replication safely: upgrade path, compatibility checks, order of components, disabling jobs, configuration backup and post-upgrade verification."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/upgrade_vbr.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/upgrade_vbr_byb.html
  - https://www.veeam.com/kb2680
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrade Veeam Backup & Replication

Applies to the Windows upgrade to version 13.1 as documented in the Veeam Help Center.

## Prerequisites
- You must be running 12.3.1 (build 12.3.1.1139) or later on a supported Windows OS. For earlier versions see the Veeam KB article on upgrading from earlier versions; KB2680 lists all versions and build numbers.
- Licensing: a version 10, 11 or 12 licence file works for version 13 (same format since v10). The support contract must be active on the date the build you install was built (checked against the support expiration date in the installed licence); you can install a new licence during the upgrade.
- If the backup server OS is unsupported: take a configuration backup, install Veeam Backup & Replication 13.1.1 (build 13.1.1.18) on a supported OS, and restore the configuration backup.
- Disk space: allocate at least the minimum calculated by the wizard's configuration check, but not less than 3 times the ISO size in the install path plus 5 GB on the system volume for database operations.
- All backup infrastructure servers must run 64-bit operating systems.
- VMware ESXi and vCenter must be at least version 7.0 and VMware Cloud Director at least 10.4, or remove those servers from the configuration to continue.
- Customers planning to migrate from a Windows installation to the Veeam Software Appliance should not upgrade to 13.1; stay on the latest 13.0 patch release and contact Veeam Customer Support.

## Upgrade wizard steps
Start the wizard, select the component, accept the licence agreement, provide a licence file, install missing software, run the configuration check, review components and start. Then perform the finalizing steps from the guide. A silent-mode upgrade is documented separately.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "Upgrading to Veeam Backup & Replication 13 on Windows" and "Upgrade Checklist" (build 13.1.2.57), and KB2680 (build list).
Removed (not on the pages read): component upgrade order (Enterprise Manager/Veeam ONE first), snapshot and job-disable preparation, post-upgrade patch and rollback advice, Verify section. See the checklist page for the remaining items, which were not read in full.
Method: documentation only; no commands were run.
