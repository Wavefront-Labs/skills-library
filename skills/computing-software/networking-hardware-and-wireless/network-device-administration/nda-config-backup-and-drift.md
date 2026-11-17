---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-config-backup-and-drift
name: nda-config-backup-and-drift
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [network-config-backup, config-drift-detection, golden-config]
level: practitioner
status: draft
description: "Automate config backups to version control and diff against a golden configuration to catch drift and unauthorised change."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Config backup and drift

- Collect configs on a schedule and on change events (syslog trigger) using tools such as Oxidized, RANCID or a vendor controller; store in Git for diffs and history.
- Mask secrets on export; protect the repository.
- Golden config templates per role (access, distribution, edge) with variables for site specifics; a diff against the template flags drift.
- Backups include controller databases (UniFi backup, Mist/Meraki cloud export, Junos `rescue configuration`).
- Test restores periodically.

## Verify
- [ ] A deliberate test change appears as a Git diff within the backup interval.
