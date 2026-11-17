---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-config-backup-restore-revisions
name: fortigate-config-backup-restore-revisions
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [config-backup, fortios, backup-config, restore-config, revision-history, sftp-backup, encrypted-backup]
level: practitioner
status: draft
description: "Back up and restore FortiGate configuration via CLI, protect it with a password and use automatic revisions."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: a recoverable copy of the config before every change.

```
execute backup config sftp fgt-edge-01.conf 192.0.2.5 backupuser <PASSWORD> <BACKUP-PASSWORD>
execute restore config sftp fgt-edge-01.conf 192.0.2.5 backupuser <PASSWORD> <BACKUP-PASSWORD>
show full-configuration | grep -f "config system interface"
```
The last argument encrypts the file; without it, the backup stores certificates and secrets only weakly protected, so treat any backup as sensitive.

Revisions: enable the setting that saves a revision on logout or when changes are made:
```
config system global
    set revision-backup-on-logout enable
    set revision-image-auto-backup enable
end
```
Revisions are listed under System > Config > Revisions (GUI). Restoring a revision reboots the unit.

Gotchas
- Restoring to a different model or firmware often fails or drops interfaces; restore only to the same model and OS version, or use a text edit approach.
- Restore reboots; schedule a window.
- Keep a periodic automated backup (cron plus the REST API backup endpoint with a read-only token) rather than relying on revisions on disk.

## Verify
After backup, confirm the file on the server has a recent timestamp and size. After restore, `get system status` shows the right hostname and `diagnose debug config-error-log read` is empty or only expected messages.
