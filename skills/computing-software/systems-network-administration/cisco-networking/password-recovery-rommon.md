---
id: computing-software.systems-network-administration.cisco-networking.password-recovery-rommon
name: password-recovery-rommon
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, password-recovery, rommon, config-register, confreg, 0x2142, break-sequence, switch-ignore-startup-config, no-service-password-recovery, console]
level: practitioner
status: draft
description: "Recover a Cisco router or Catalyst switch with lost passwords: break to ROMMON, bypass startup-config, restore and reset secrets, and put the config register back."
sources:
  - https://www.cisco.com/c/en/us/support/docs/routers/2800-series-integrated-services-routers/112033-c2900-password-recovery-00.html
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/215486-perform-password-recovery-on-catalyst-9.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Password recovery via ROMMON

Needs physical console access. Plan a short outage: the device reloads twice.

## ISR / IOS XE routers (config register method)
1. Console at 9600 8N1, power-cycle, send **Break** within 60 s (PuTTY: Special Command >
   Break; `screen`: Ctrl-A then `b`; some terminals need Ctrl-Break).
2. At `rommon 1 >`:
   ```
   confreg 0x2142        ! ignore startup-config
   reset
   ```
3. Answer `no` to the setup dialogue, then:
   ```
   enable
   copy startup-config running-config     ! NOT the other way round
   configure terminal
    enable secret algorithm-type scrypt secret <NEW_SECRET>
    username admin privilege 15 algorithm-type scrypt secret <NEW_SECRET>
    config-register 0x2102
   end
   write memory
   ```
4. `show version | i register` shows `0x2142 (will be 0x2102 at next reload)`.

## Catalyst 9000 switches
1. Unplug power, hold the **Mode** button, reconnect, release when the SYST LED goes amber
   (about 15 s) to land at `switch:`.
2. `SWITCH_IGNORE_STARTUP_CFG=1` then `boot`.
3. Same restore as above, then `no system ignore startup-config switch all` (IOS XE 16.x+),
   `write memory`. In ROMMON you can instead set `SWITCH_IGNORE_STARTUP_CFG=0` next time.

## Gotchas
- **Interfaces come up shut** after `copy start run` on some platforms if the startup
  config was never loaded; check `show ip int brief` and `no shutdown` as needed.
- `no service password-recovery` blocks this procedure: the only option is to erase the
  config (the device offers to reset to factory defaults). Back up configs off-box.
- Forgetting to restore `0x2102` means the next reload boots with an empty config.
- Type 7 passwords (`service password-encryption`) are reversible; replace them with type 8/9
  secrets while you are in.

## Verify
- [ ] Login works with the new credentials over SSH and console.
- [ ] `show version` register is `0x2102`; `show romvar` on Catalyst shows ignore=0.
- [ ] `show run` matches the pre-incident backup apart from the new secrets.
