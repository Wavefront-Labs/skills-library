---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-enterprise-application-plug-ins
name: veeam-enterprise-application-plug-ins
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-plug-in, rman-plugin, oracle, sap-hana, sap-on-oracle, application-backup]
level: advanced
status: draft
description: "Use Veeam plug-ins for Oracle RMAN, SAP HANA, SAP on Oracle, Db2 and MongoDB so DBAs keep native tools while backups land in Veeam repositories."
sources:
  - https://helpcenter.veeam.com/docs/backup/plugins/overview.html
  - https://helpcenter.veeam.com/docs/backup/plugins/rman_plugin.html
  - https://helpcenter.veeam.com/docs/backup/plugins/sap_hana_plugin.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Veeam enterprise application plug-ins

**Why:** DBAs keep using RMAN, HANA backint or Db2 commands; Veeam supplies the storage, retention, immutability and monitoring.

## Oracle RMAN plug-in
1. Install the plug-in package on the DB server (`rpm -i VeeamPluginforOracleRMAN*.rpm` on Linux, MSI on Windows).
2. Run the configuration wizard `OracleRMANConfigTool --wizard`: backup server address, credentials (a Veeam user with access to the repository), target repository, channels.
3. It prints the RMAN `CONFIGURE CHANNEL DEVICE TYPE SBT_TAPE PARMS 'SBT_LIBRARY=...libOracleRMANPlugin.so'` lines; apply them in RMAN.
4. Keep the DBA's existing scripts (`BACKUP DATABASE PLUS ARCHIVELOG`); retention stays controlled by RMAN (`CONFIGURE RETENTION POLICY` and `DELETE OBSOLETE`).
5. Back up the control file autobackup to the same SBT channel.

## SAP HANA plug-in
Installs as a **backint** implementation: `SapBackintConfigTool --wizard`, then point HANA's `catalog_backup_using_backint` and data/log backint parameters to it. Schedule from HANA Cockpit or cron.

## Management
- Backups show in the Veeam console as plug-in jobs; Veeam can copy them with backup copy jobs to a second site or object storage with immutability.
- Restores are run from the native tool (RMAN `RESTORE/RECOVER`, HANA recovery wizard), optionally to another host by configuring the plug-in there with "restore from another server" authorisation.

## Gotchas
- Plug-in version must match or be supported by the B&R version; upgrade plug-ins after B&R.
- Firewall from DB server to repository (data mover ports 2500-3300).

## Verify
RMAN `LIST BACKUP SUMMARY` shows SBT_TAPE pieces; Veeam console shows the plug-in job session; a test restore to a scratch host succeeds.
