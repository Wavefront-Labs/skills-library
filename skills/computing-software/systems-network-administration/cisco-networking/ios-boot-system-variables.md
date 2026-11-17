---
id: computing-software.systems-network-administration.cisco-networking.ios-boot-system-variables
name: ios-boot-system-variables
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, boot-system, boot-variable, bundle-mode, install-mode, rommon, confreg, config-register, packages-conf]
level: practitioner
status: draft
description: "Control what IOS/IOS XE boots: boot system statements, BOOT variable, bundle vs install mode, config-register and recovering from a bad boot variable."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg/performing_device_setup_configuration.html
  - https://www.cisco.com/c/en/us/support/docs/routers/10000-series-routers/50421-config-register-use.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Boot system statements and the BOOT variable

## What decides the image
1. Config register boot field (`0x2102` = boot normally from `boot system` statements; `0x2100` = stay in ROMMON; `0x2142` = ignore startup-config).
2. `boot system` statements in **startup-config**, tried in order (routers), or the BOOT environment variable (Catalyst).
3. Fallback: first valid image in flash.

```
show boot                    ! Catalyst: BOOT variable, manual boot, config file
show version | include register|System image
show bootvar                 ! routers/IOS XE
```

## Setting it
```
conf t
 no boot system
 boot system flash:packages.conf          ! IOS XE install mode
 ! or bundle mode:
 boot system flash:cat9k_iosxe.17.09.05.SPA.bin
 boot system flash:cat9k_iosxe.17.06.06.SPA.bin   ! fallback (routers try in order)
 config-register 0x2102
end
write memory                 ! boot system lives in startup-config; unsaved = not used
```
On Catalyst 9000 `boot system` writes the BOOT variable immediately (`show boot` shows it), but
still save the config.

## Bundle vs install
| | Bundle | Install |
|---|---|---|
| boot target | the `.bin` | `packages.conf` |
| boot time / memory | slower, unpacks into RAM | faster, packages expanded in flash |
| upgrade | copy + change boot var | `install add file ... activate commit` |
| features | some (ISSU, SMUs, stack member auto-upgrade) need install mode | full support |

## Recovery
- Boot var points at a deleted file: switch lands in `switch:` ROMMON. `dir flash:` then
  `boot flash:packages.conf` (or the .bin), then fix `boot system` and save.
- On routers `rommon 1 > confreg 0x2102` then `reset` if the register was left at 0x2142.
- Stack members must share the same boot mode; mismatched members go to V-mismatch state.

## Verify
- [ ] `show boot` / `show bootvar` points to a file that exists (`dir flash: | i packages.conf|.bin`).
- [ ] Config register is 0x2102 (`show version | i register`), next reload value the same.
- [ ] Old images removed only after a successful reload on the new one (`install remove inactive`).
