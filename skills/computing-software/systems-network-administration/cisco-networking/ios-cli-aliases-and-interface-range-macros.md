---
id: computing-software.systems-network-administration.cisco-networking.ios-cli-aliases-and-interface-range-macros
name: ios-cli-aliases-and-interface-range-macros
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ios-cli, ios-alias, alias-exec, interface-range-macro, define-interface-range, interface-range, cli-productivity]
level: practitioner
status: draft
description: "Speed up IOS CLI work with alias exec/configure shortcuts and define interface-range macros, and know where aliases break scripts and automation."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/command/fundamentals-cr-book/fundamentals-a1.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg/configuring_interface_characteristics.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IOS CLI aliases and interface-range macros

## Aliases
Aliases are per-mode text substitutions stored in the running config.
```
alias exec srb show running-config | section bgp
alias exec sib show ip interface brief | exclude unassigned
alias exec c configure terminal
alias configure ri router isis
alias interface sh shutdown
show aliases                 ! all modes, including built-ins (h=help, lo=logout, p=ping, r=resume, s=show, u/un=undebug, w=where)
```
- The alias is matched only as the **first word** in that mode; arguments typed after the alias are appended.
- Built-in default aliases exist; `show aliases exec` lists them. Do not shadow common abbreviations
  (`s`, `p`) or other people on the box lose their muscle memory.
- Aliases are local to the device; keep them in your golden config template if you want them everywhere.

## Interface-range macros
```
define interface-range USERS GigabitEthernet1/0/1 - 24 , GigabitEthernet2/0/1 - 24
define interface-range UPLINKS TenGigabitEthernet1/1/1 - 2
interface range macro USERS
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
show running-config | include define
```
- Spaces around `-` and `,` are required in ranges.
- The macro must be defined before use.
- `interface range` itself (without macro) accepts up to five comma-separated ranges.

## Gotchas
- Automation (Netmiko, Ansible `ios_config`) sends full commands; an alias that collides with a
  real keyword can change what a script does. Keep aliases short and unique, or avoid them on
  automated estates.
- Aliases appear in `show run`; config compliance tools may flag them as drift.
- A range that includes a missing stack member fails with `% Invalid input` for the whole line.

## Verify
- [ ] `show aliases exec` shows yours and no collisions with commands your scripts use.
- [ ] `interface range macro <NAME>` enters the expected ports (`show run | include define`).
