---
id: computing-software.networking-hardware-and-wireless.opnsense.config-backup-restore-history
name: config-backup-restore-history
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [backups, config-restore, config-history, xml]
level: practitioner
status: docs-checked
description: "Back up, restore and diff OPNsense configurations under System > Configuration, including password-protected exports and console-settings exclusion."
sources: ["https://docs.opnsense.org/manual/backups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuration backup, restore and history

System > Configuration > Backups is where you export and import the whole configuration. A local backup can be password-protected and can optionally include RRD statistics, which are then stored in the same XML export (RRD data feeds System Health). Because the file holds sensitive data, protect it with a strong password when storing or sharing it.

Restoring: prefer a complete restore. Partial restores are possible but can behave unexpectedly because components depend on each other, and future versions may drop the feature. When restoring onto different hardware or a VM, the console settings of the source machine might not fit, so by default restore does not apply the backup's console settings; uncheck Exclude console settings from import to change that. If interface names do not match the new hardware, no automatic reboot happens; you are prompted to fix the interface assignments.

Defaults resets the firewall to firmware defaults and shuts down when done.

History tracks changes between modifications. Pick a stored version from the dropdown and the previous one is chosen automatically as a comparison target; the lower pane shows a unified diff. Buttons: revert to this backup (this firewall only; no services restart, so a reboot may be needed for a clean state), remove the backup, and download the selected one. If OPNcentral is installed and performing backups, a host selector appears on top. The number of backups to keep is configurable in the Backups menu, which helps where auditability matters.

Remote backup targets are separate topics: SFTP, Git, and cloud backup.

## Checked

2026-11-03. Read the Configuration manual page (backups.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
