---
id: computing-software.systems-network-administration.cisco-networking.switchport-host-and-smartport-macros
name: switchport-host-and-smartport-macros
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, switchport-host, smartport-macro, macro-apply, auto-smartports, access-port, portfast]
level: practitioner
status: draft
description: "Configure access ports fast with switchport host and Smartport/macro templates, and know what each macro changes and how to audit or remove it."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst3750x_3560x/software/release/15-2_2_e/configuration/guide/b_1522e_3750x_3560x_cg/b_1522e_3750x_3560x_cg_chapter_011.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/command_reference/b_179_9300_cr/interface_and_hardware_commands.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# switchport host and Smartport macros

## switchport host
A one-line macro for an end-host port:
```
interface Gi1/0/5
 switchport host
! expands to:
!  switchport mode access
!  spanning-tree portfast
!  (older releases also: switchport nonegotiate / no channel-group)
```
It is a shorthand applied once; the resulting commands, not `switchport host`, appear in `show run`.

## Built-in Smartport macros (Catalyst IOS/IOS XE)
```
show parser macro brief                ! cisco-desktop, cisco-phone, cisco-switch, cisco-router, cisco-wireless
show parser macro name cisco-phone     ! see what it will do first
interface Gi1/0/6
 macro apply cisco-phone $access_vlan 20 $voice_vlan 100
 macro trace cisco-phone $access_vlan 20 $voice_vlan 100   ! apply and echo each command
show parser macro description interface Gi1/0/6
```
`cisco-phone` sets access + voice VLAN, port-security, portfast, BPDU guard and AutoQoS trust
on many releases; read it before applying.

## Custom macro
```
macro name USER-PORT
 switchport mode access
 switchport access vlan $DATA
 switchport voice vlan $VOICE
 spanning-tree portfast
 spanning-tree bpduguard enable
@
interface range Gi1/0/1 - 24
 macro apply USER-PORT $DATA 20 $VOICE 100
```
Variables start with `$`; end the macro body with `@`.

## Removing
A macro is not undone by `no macro`; you must negate each command, or `default interface Gi1/0/6`
and reapply. `macro description` only records that a macro was applied.

## Gotchas
- Auto Smartports (dynamic macros by device type via CDP/LLDP) is deprecated on current IOS XE;
  use templates in automation or Catalyst Center instead.
- Macros configure what they configure at that moment; later template changes do not flow back.

## Verify
- [ ] `show running-config interface <port>` contains the expected expanded lines.
- [ ] `show spanning-tree interface <port> portfast` is enabled on host ports only.
