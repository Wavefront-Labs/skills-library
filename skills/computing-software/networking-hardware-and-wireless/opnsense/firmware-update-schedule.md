---
id: computing-software.networking-hardware-and-wireless.opnsense.firmware-update-schedule
name: firmware-update-schedule
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [firmware, updates, major-upgrade, release-type]
level: practitioner
status: docs-checked
description: "How OPNsense versions and updates work: two majors a year, fortnightly minors, mirror and release type settings, and offline major upgrades."
sources: ["https://docs.opnsense.org/manual/updates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Firmware updates and major upgrades

OPNsense ships two major releases per year, each receiving minor updates roughly every two weeks. Version numbers are year.month, so 25.1 is the January 2025 release, and 25.1.3 is its third update.

System > Firmware > Settings holds two knobs: Firmware Mirror, where updates are fetched from (change it if updating is slow or failing), and Release Type, Production (regular tested fortnightly releases) versus Development (newest, not fully tested). Leave it at Production unless you understand the implications. The same page offers "Run an audit"; choose Connectivity to debug problems reaching the update server.

Minor updates: System > Firmware > Status, click Check for updates, then install if the button appears.

Major upgrades should be done with a VGA display or serial console attached. They are installed offline, so no web or SSH server runs during the upgrade; on failure you need a second connection or console access to revert to a snapshot or repair. On the console menu choose option 12; you are asked whether to upgrade to the newest version or the next major release, and you type the major version (for example 19.1). The firewall downloads all release files, reboots, installs, and reboots again. Serial access setup is covered in the serial_access how-to.

## Checked

2026-11-03. Confirmed against the OPNsense Updates manual page: two major releases a year, fortnightly minors, version naming, Firmware Mirror and Release Type, the connectivity audit, minor update steps, console option 12 and the offline major upgrade. Nothing removed.

Method: documentation only; no commands were run.
