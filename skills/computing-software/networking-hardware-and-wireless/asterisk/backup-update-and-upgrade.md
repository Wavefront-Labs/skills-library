---
id: computing-software.networking-hardware-and-wireless.asterisk.backup-update-and-upgrade
name: backup-update-and-upgrade
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, backup, upgrade, update, upgrade-txt, changes, menuselect-makeopts, make-samples, restore]
level: practitioner
status: docs-checked
description: "Back up Asterisk configuration, astdb, databases and logs, and plan minor updates versus major upgrades using UPGRADE.txt, CHANGES, ChangeLog and menuselect.makeopts."
sources:
  - https://docs.asterisk.org/Operation/Maintenance-and-Upgrades/Asterisk-Backups/
  - https://docs.asterisk.org/Operation/Maintenance-and-Upgrades/Updating-or-Upgrading-Asterisk/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# backup, update and upgrade
**Back up:** configuration, the internal database (astdb), any other databases Asterisk uses, and logs and reports. Archive with tar or your usual backup tooling, for example from cron to off-site storage. Restoring means putting files back in their original locations and starting Asterisk; restoring onto a new major version needs the same steps as an upgrade.

**Update** = new minor version (bug and security fixes, normally no features). **Upgrade** = new major version (new features, changes, deprecations, support-status change). Do either only when necessary: an affected bug or vulnerability, or a needed feature. Know the support life-cycle.

Research files in the source root: `UPGRADE.txt` (changes between major versions, especially breaking ones), `CHANGES` (new or enhanced functionality), `ChangeLog` (all changes, verbose).

Upgrade process: research, back up, install on a non-production test system, migrate configuration, databases and data, then test, especially areas noted in UPGRADE.txt or CHANGES, custom AGI, AMI and ARI applications, and the whole dialplan.

Tips:
- Samples are not refreshed unless you run `make samples` or copy them; do not overwrite your configuration.
- Keep old `menuselect.makeopts` for rebuilds (may work for updates, not upgrades).
- Rebuild or reinstall third-party modules, or you may get a post-build warning.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Asterisk-Backups, Updating-or-Upgrading-Asterisk) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
