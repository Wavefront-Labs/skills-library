---
id: computing-software.systems-network-administration.virtualisation.vsphere-nic-teaming-and-failover-policy
name: vsphere-nic-teaming-and-failover-policy
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-networking, vsphere-nic-teaming, load-based-teaming, nic-teaming, route-based-on-ip-hash, failover-order, notify-switches, beacon-probing, vmware, esxi, vsphere]
level: practitioner
status: draft
description: "Pick vSphere teaming: originating port ID, load-based teaming, IP hash (needs static EtherChannel), explicit failover order, link-state vs beacon detection and notify switches."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere NIC teaming and failover policy

**Goal:** use every uplink, survive a NIC or switch failure, and never configure a policy
the physical switch does not agree with.

## Load-balancing algorithms
| Policy | Switch config | Use |
|---|---|---|
| Route based on originating virtual port (default) | Plain trunks, no port channel | Safe default: each vNIC pinned to one uplink |
| Route based on physical NIC load (LBT, vDS only) | Plain trunks | Best general choice on vDS: moves ports when an uplink exceeds ~75% for 30 s |
| Route based on IP hash | **Static** EtherChannel (mode on) on all ports, same switch or stack/vPC | Single VM needing more than one link across many flows |
| Source MAC hash | Plain trunks | Rarely useful |
| Use explicit failover order | Plain trunks | VMkernel ports needing determinism (iSCSI, vMotion pairs) |
| LACP (vDS LAG) | LACP on switch | See the vDS LACP skill |
IP hash without a port channel (or a port channel with port-ID teaming) causes MAC
flapping and packet loss on the physical switch.

## Failover settings
- **Network failure detection:** link status only (default). Beacon probing needs at
  least three uplinks to be meaningful and catches upstream failures; do not combine with
  IP hash.
- **Notify switches: Yes** so physical switches learn MAC moves after failover or vMotion.
  Set **No** for Microsoft NLB in unicast mode.
- **Failback: Yes** returns traffic to the preferred uplink when it recovers; set No if a
  flapping link would bounce traffic.
- **Active/standby/unused:** e.g. vMotion vmk1 active vmnic2 standby vmnic3, vmk2 the
  reverse, for multi-NIC vMotion. iSCSI port binding: exactly one active, others unused.

## Check from the host
```sh
esxcli network vswitch standard policy failover get -v vSwitch0
esxcli network nic list                       # link state and speed
esxtop  # press n: see which vmnic each port uses (TEAM-PNIC column)
```

## Verify
Pull each cable (or `esxcli network nic down -n vmnicX` in a window) while pinging a VM
and a vmk: loss should be a few packets at most, and traffic should come back after
failback.
