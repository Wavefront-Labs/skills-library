---
id: computing-software.systems-network-administration.cisco-networking.lldp-enable-and-tlv-selection
name: lldp-enable-and-tlv-selection
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, lldp, lldp-run, lldp-tlv, lldp-timer, lldp-holdtime, lldp-transmit, lldp-receive, lldp-tlv-select, multivendor, ieee-802-1ab]
level: practitioner
status: docs-checked
description: "Enable and tune LLDP (802.1AB) on Catalyst IOS XE for multivendor neighbours: global and per-port transmit/receive, timers, TLV selection and verifying what is advertised."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg/configuring_lldp__lldp_med__and_wired_location_service.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/command_reference/b_179_9300_cr/interface_and_hardware_commands.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling LLDP and selecting TLVs

CDP covers Cisco devices only. The switch supports IEEE 802.1AB LLDP for non-Cisco devices and
interoperability. LLDP is **disabled** globally by default, so turn it on wherever you have
non-Cisco switches, phones, APs or servers.

## Enable (Catalyst 9300, IOS XE 17.9)
```
lldp run                       ! global
lldp timer 30                  ! update interval, 5-65534 s, default 30
lldp holdtime 120              ! hold time at receiver, 0-65535 s, default 120
lldp reinit 2                  ! init delay on an interface, 2-5 s, default 2
!
interface Gi1/0/48
 lldp transmit
 lldp receive
interface Gi1/0/1
 no lldp transmit              ! e.g. untrusted public port
```
The guide's enable procedure sets `lldp transmit` and `lldp receive` on each interface; the
command reference lists the interface-level default as disabled, so confirm with
`show lldp interface`.

## TLVs
Basic management TLVs the switch supports: port description, system name, system description,
system capabilities, management address. For LLDP-MED it also advertises the Port VLAN ID TLV
(802.1) and the MAC/PHY configuration/status TLV (802.3).

LLDP-MED TLVs are selected per interface; all are enabled by default when LLDP is enabled:
```
interface Gi1/0/1
 lldp med-tlv-select inventory-management   ! also: location, network-policy, power-management
 lldp tlv-select power-management
```
On this platform the interface-level `lldp tlv-select` takes only `power-management`. By default the
switch sends plain LLDP until it receives LLDP-MED from the endpoint, then adds the MED TLVs.

When CDP and LLDP both run and CDP negotiates power, disable LLDP on that interface with
`no lldp tlv-select power-management` or `no lldp transmit` / `no lldp receive`. LLDP is
disabled automatically on tunnel ports.

## Inspect
```
show lldp                              ! frequency, holdtime, reinit delay
show lldp interface Gi1/0/48
show lldp neighbors detail
show lldp traffic                      ! packets sent/received/discarded, unrecognised TLVs
show lldp entry <NEIGHBOR-NAME>
```

## Verify
- [ ] `show lldp` shows LLDP running with the intended timers.
- [ ] `show lldp neighbors` lists the non-Cisco devices on their ports.
- [ ] `show lldp traffic` shows no discards or unrecognised TLVs increasing.

## Checked
2026-11-08. Confirmed against the Catalyst 9300 17.9 Interface and Hardware guide LLDP chapter
and the 17.9 command reference entry for `lldp` (interface configuration): defaults and ranges,
supported TLVs, LLDP-MED behaviour, tunnel-port and CDP power notes, show commands. Removed
unsupported claims: mandatory Chassis ID/Port ID/TTL wording, `no lldp tlv-select
system-description` and `lldp management-address` (not on this platform's command page),
the link-local MAC, hypervisor, NIC-firmware and Linux/Windows tool notes. The original guide URL
404s; the chapter is in the int_hw guide.
Method: documentation only; no commands were run.
