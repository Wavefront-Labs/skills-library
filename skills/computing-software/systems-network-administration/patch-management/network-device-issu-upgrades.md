---
id: computing-software.systems-network-administration.patch-management.network-device-issu-upgrades
name: network-device-issu-upgrades
category: computing-software
field: systems-network-administration
product: patch-management
tags: [issu, in-service-software-upgrade, cisco-ios-xe, nx-os, junos, sso, network-device-upgrade]
level: advanced
status: docs-checked
description: "Upgrade redundant network devices with ISSU on Cisco IOS XE, NX-OS and Junos: prerequisites, compatibility checks, commands and when ISSU is not worth it."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9600/software/release/17-12/configuration_guide/ha/b_1712_ha_9600_cg/configuring_issu.html
  - https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/104x/upgrade/cisco-nexus-9000-series-nx-os-software-upgrade-and-downgrade-guide-104x.html
  - https://www.juniper.net/documentation/us/en/software/junos/high-availability/topics/topic-map/issu-understanding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-service software upgrades (ISSU)

**Goal:** patch core switches and routers with redundant control planes without a forwarding outage.

## Prerequisites
- Redundant supervisors/routing engines (or a StackWise Virtual pair), healthy before you start.
- Source and target releases that the vendor supports for ISSU. On IOS XE, ISSU is not supported from 16.x to 17.x or for downgrades, and only one upgrade operation (not hardware plus software) at a time. On Junos, unified ISSU upgrades at most three major releases ahead.
- Install mode (not bundle mode) on IOS XE: the ISSU install command errors on a bundle-mode boot.

## Cisco IOS XE (Catalyst 9600 and StackWise Virtual; 9200 and 9300 do not support ISSU)
```text
show issu comp-matrix
show issu state detail
install add file bootflash:cat9k_iosxe.17.12.04.SPA.bin activate issu commit
show install summary
```
The command extracts the files, reloads the standby, waits for it to rejoin, then fails over and reloads the former active. It starts reloading immediately, with no confirmation prompt. On StackWise Virtual each chassis reloads once, so devices attached to only one chassis lose connectivity for a full reboot cycle; Cisco recommends dual-homed MEC connections.

## Cisco NX-OS (Nexus 9000)
Use the Cisco Nexus 9000 Series NX-OS Software Upgrade and Downgrade Guide for your release for the compatibility check, impact preview and non-disruptive install commands; it also has a chapter on migrating switches in a vPC topology.

## Junos (dual RE)
Requires dual Routing Engines with graceful Routing Engine switchover enabled; unified ISSU works together with nonstop active routing. The primary RE first validates the configuration and /var disk space on both REs. The `no-old-master-upgrade` option skips upgrading the former primary:
```text
request system software in-service-upgrade /var/tmp/junos-install-mx-x86-64-23.4R2.tgz
```

## When to skip ISSU
Devices are already redundant at the network level (MLAG/vPC pairs, ECMP): a normal reboot of one peer at a time is simpler and better tested than ISSU's moving parts.

## Gotchas
- Read the release notes' ISSU caveats; Junos checks that the configuration and PICs are supported by unified ISSU.
- Back up config and verify console access first.

## Verify
`show version` on both supervisors shows the new release, redundancy is healthy again, and monitoring saw no packet loss beyond the expected reconvergence.

## Checked
2026-10-28. Confirmed against Cisco's Catalyst 9600 17.12 ISSU configuration guide (activate issu commit, bundle-mode error, 16.x to 17.x and downgrade limits, one operation at a time, show issu commands), Cisco's Catalyst 9000 upgrade guide (ISSU sequence, no confirmation, StackWise Virtual and MEC note, 9200 and 9300 unsupported) and Juniper's Understanding Unified ISSU (dual REs, GRES, NSR, three-release limit, validation, no-old-master-upgrade). Removed: all NX-OS commands and enhanced ISSU (the fetched guide was a table of contents only), SSO and hot-standby wording, line card example.
Method: documentation only; no commands were run.
