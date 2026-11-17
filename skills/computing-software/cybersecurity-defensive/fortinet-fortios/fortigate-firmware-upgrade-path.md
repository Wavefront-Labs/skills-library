---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-firmware-upgrade-path
name: fortigate-firmware-upgrade-path
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [firmware-upgrade, fortios, upgrade-path, ha-upgrade, firmware-image, fortiguard-upgrade-path]
level: practitioner
status: draft
description: "Plan and run a FortiGate firmware upgrade - upgrade path tool, backup, image install and HA cluster ordering."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/upgrade-path"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: upgrade without hitting an unsupported path or losing config.

1. Open the Fortinet Upgrade Path tool (support portal) and note each required hop; skipping a required intermediate release can fail or lose config.
2. Read release notes for known issues, feature changes (for example defaults or removed features; confirm each).
3. Back up config (see the config-backup skill).
4. Upgrade:
```
get system status
execute restore image tftp FGT_7.4.x.out 192.0.2.5
execute restore image sftp FGT_7.4.x.out 192.0.2.5 backupuser <PASSWORD>
```
or use System > Firmware in the GUI. Dual partition: the unit boots from the new image; the old stays in the alternate partition for rollback (`execute set-next-boot primary|secondary`).

HA cluster: with uninterruptible upgrade enabled (default), upgrade the secondary first, then the primary after a failover. Do not reboot manually halfway.

Gotchas
- Hardware models drop support for newer releases; check the compatibility matrix before downloading.
- FortiManager-managed devices need FortiManager at a compatible version.
- Config conversion can change defaults; compare `show` outputs before and after.

## Verify
```
get system status
diagnose sys ha status
get system ha status
```
Version is new, cluster members in sync, and the dashboard shows license/FortiGuard still valid.
