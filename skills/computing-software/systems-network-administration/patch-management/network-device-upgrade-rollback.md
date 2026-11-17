---
id: computing-software.systems-network-administration.patch-management.network-device-upgrade-rollback
name: network-device-upgrade-rollback
category: computing-software
field: systems-network-administration
product: patch-management
tags: [network-rollback, boot-variable, install-rollback, auto-abort-timer, commit-confirmed, configure-replace, network-device-upgrade]
level: advanced
status: draft
description: "Roll back network device upgrades: keep old images, IOS XE auto-abort and install rollback, boot variables, Junos rollback and commit confirmed, config replace."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-12/configuration_guide/sys_mgmt/b_1712_sys_mgmt_9300_cg/performing_device_setup_configuration.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/configuration/xe-16/fundamentals-xe-16-book/cf-config-rollback.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rollback for network device upgrades

**Goal:** if the new release misbehaves, get back to the old one in minutes, even remotely.

## Before the upgrade
- Keep the current image on flash; confirm free space for both.
- Save running config and an off-box backup (`copy running-config tftp:` or your config backup system).
- Confirm out-of-band console access (console server or OOB network). Remote upgrades without it are a gamble.

## Cisco IOS XE install mode
```text
install add file flash:cat9k_iosxe.17.12.04.SPA.bin
install activate auto-abort-timer 30      ! reloads into new version; reverts if not committed in 30 min
! test, then
install commit
! problems after commit:
install rollback to committed            ! or: install rollback to id <n>  (show install rollback)
```

## Cisco bundle mode / classic IOS
```text
show boot
conf t
 no boot system
 boot system flash:old-image.bin
end
write memory
reload
```

## NX-OS
`boot nxos bootflash:<old image>` then `copy run start` and reload; or `install all nxos bootflash:<old image>` (check impact).

## Junos
```text
request system software rollback      ! previous installed software set
request system reboot
commit confirmed 10                   ! for config changes: auto-reverts unless confirmed
```

## Configuration rollback
IOS: `archive` + `configure replace flash:pre-change.cfg list`, or `configure terminal revert timer 10` (config rollback with timer).

## Gotchas
- Downgrades can fail on newer hardware revisions or after a ROMMON/FPGA upgrade that the old release does not support; read release notes for anti-rollback notes.
- Licence or config syntax introduced in the new release may not parse on the old; rollback the config too.

## Verify
In the lab, practise the rollback for each platform and time it; record the steps in the change's backout plan.
