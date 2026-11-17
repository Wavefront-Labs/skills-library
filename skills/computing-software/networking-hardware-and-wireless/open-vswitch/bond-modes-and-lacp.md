---
id: computing-software.networking-hardware-and-wireless.open-vswitch.bond-modes-and-lacp
name: bond-modes-and-lacp
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, add-bond, bond-mode, lacp, active-backup, balance-slb, balance-tcp, bonding]
level: practitioner
status: docs-checked
description: "Create an Open vSwitch bond with add-bond, pick active-backup, balance-slb or balance-tcp, enable LACP, and use lacp-fallback-ab and lacp-time."
sources:
  - https://docs.openvswitch.org/en/latest/topics/bonding/
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bond modes and lacp
Create: `ovs-vsctl add-bond br0 bond0 eth0 eth1` (at least two interfaces; `--fake-iface` creates a fake interface named after the port, only for legacy software; for DPDK interfaces the transaction must also set the interface type to `dpdk`).

Port column `bond_mode`: `active-backup`, `balance-slb`, `balance-tcp`; defaults to `active-backup` if unset.
`ovs-vsctl set port bond0 bond_mode=balance-slb`

Mode guidance:
- Active-backup: all flows on one member, failing over when it is disabled; the only mode in which interfaces may be plugged into different upstream switches.
- SLB (`balance-slb`): balances by source MAC and VLAN without the remote switch's cooperation, so do not configure a bond on the upstream switch; useful only with many source MACs; relies on MAC learning and is incompatible with `flood_vlans`.
- `balance-tcp`: balances on L3/L4 information; needs an upstream switch with 802.3ad and successful LACP negotiation. If negotiation fails and `other_config:lacp-fallback-ab` is true, active-backup is used.

LACP: `ovs-vsctl set port bond0 lacp=active` (values `active`, `passive`, `off`; default `off`). `active` ports may initiate negotiation, `passive` ports only take part in negotiations a remote switch starts.
- `other_config:lacp-time` is `fast` (heartbeat once per second) or `slow` (once every 30 seconds; the default).
- `other_config:lacp-fallback-ab=true` lets the bond fall back to active-backup when the partner does not support LACP (false disables the bond); once the partner is in LACP mode the bond uses LACP. Useful because several physical switches block all traffic on LACP ports until LACP is negotiated.
- `other_config:bond-primary` names an interface that is made active if it exists in the bond and is up (relevant for active-backup or an active-backup fallback).

Inspect: `ovs-appctl bond/show` and `ovs-appctl lacp/show` (see bond-runtime-inspection).

A bond always has at least two members in vswitchd; if a configuration error leaves only one, the port becomes an ordinary port and bond features do not apply.

## Checked
2026-11-04. Confirmed against the OVS bonding topic page, ovs-vsctl(8) add-bond and ovs-vswitchd.conf.db(5) (Port table bonding and LACP columns). Removed the claim that adding the NICs as separate ports creates a loop (not on the pages).
Method: documentation only; no commands were run.
