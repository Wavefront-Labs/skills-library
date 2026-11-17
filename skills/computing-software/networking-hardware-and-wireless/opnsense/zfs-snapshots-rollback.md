---
id: computing-software.networking-hardware-and-wireless.opnsense.zfs-snapshots-rollback
name: zfs-snapshots-rollback
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [snapshots, zfs, boot-environments, rollback]
level: practitioner
status: docs-checked
description: "Use ZFS snapshots on OPNsense for safe upgrades: known-good workflow, states N/R/NR, GUI activation and boot menu option 8 rollback."
sources: ["https://docs.opnsense.org/manual/snapshots.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Snapshots and rollback

System > Snapshots creates restore points of the base system. They require ZFS; UFS cannot do filesystem snapshots. They are differential: a new snapshot is the current running state, there are no incremental chains, and each snapshot is self-contained and can be created or deleted independently. A snapshot grows as it diverges from the active one. Hypervisor-based VMs may prefer VM-level snapshots instead.

Recommended workflow:
1. Create a snapshot named known-good (System > Snapshots, the + button).
2. Make the risky change, such as a firmware upgrade, in the active default snapshot.
3. Reboot and test. If fine, delete known-good. If broken, activate known-good (check mark in the GUI, or the boot menu), reboot, delete the bad default snapshot, then rename known-good back to default.

States column: N active now, R active after reboot, NR active now and used on reboot, - inactive. Before deleting, confirm the snapshot you are keeping shows NR.

If the GUI is unreachable: during boot, press Space to pause the boot menu, press 8 for Boot Environments, press 2 to cycle the active snapshot until it shows zfs:zroot/ROOT/known-good, press 1 to return to the main menu, then Enter for Boot Multi user. Appliances without VGA can use the serial console.

Tip: activating a fresh snapshot immediately makes the system return to the last known good configuration on any reboot or power cycle. Snapshots may be kept for a few days after an upgrade, but rolling back loses configuration changes made since, so take a config backup and import it afterwards.

## Checked

2026-11-03. Read the Snapshots manual page (snapshots.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
