---
id: computing-software.systems-network-administration.cisco-networking.multichassis-etherchannel-stackwise-virtual
name: multichassis-etherchannel-stackwise-virtual
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, multichassis-etherchannel, mec, stackwise-virtual, svl, dad, etherchannel, high-availability]
level: practitioner
status: draft
description: "Build Multichassis EtherChannel on a Catalyst 9000 StackWise Virtual pair: SVL and DAD links, MEC to access switches and servers, and verifying traffic stays local."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9500/software/release/17-9/configuration_guide/ha/b_179_ha_9500_cg/configuring_cisco_stackwise_virtual.html
  - https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9000/nb-06-cat-9k-stack-wp-cte-en.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multichassis EtherChannel with StackWise Virtual

Two Catalyst 9500/9600 (or 9400) chassis act as one logical switch. A downstream switch bundles
one uplink to each chassis into a single LACP port-channel (MEC): no STP blocking, sub-second
failover.

## StackWise Virtual pair (on both, then reload)
```
switch 1 priority 15          ! on chassis 1; chassis 2 uses switch 2 renumber
stackwise-virtual
 domain 10
interface range HundredGigE1/0/31-32
 stackwise-virtual link 1     ! SVL: carries control + data between chassis
interface HundredGigE1/0/30
 stackwise-virtual dual-active-detection   ! dedicated DAD link
```
After reload: `show stackwise-virtual`, `show stackwise-virtual link`, `show switch`.

## MEC to an access switch
On the SVL pair:
```
interface range TwentyFiveGigE1/0/1, TwentyFiveGigE2/0/1
 channel-group 11 mode active
interface Port-channel11
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
```
On the access switch: a normal LACP port-channel with one link to each chassis.

## Why traffic stays local
Each chassis forwards out its own MEC member when possible; the SVL only carries traffic for
single-attached devices or after a member fails. Size the SVL for failure cases (at least 2 links,
ideally on different line cards/ASICs).
```
show etherchannel 11 summary
show platform software fed switch active etherchannel 11 group-mask
show interfaces HundredGigE1/0/31 | include rate     ! SVL load should be low
```

## Dual-active detection
If the SVL fails completely both chassis think they are active: duplicate router IDs, duplicate
gateway MACs. DAD (dedicated link, or ePAgP via a downstream switch) makes the former standby shut
all its non-excluded ports. Exclude management ports with `dual-active exclude interface`.

## Gotchas
- Single-attached devices (one link to chassis 1 only) send all their traffic over the SVL when
  chassis 1 fails or when the destination is on chassis 2. Dual-attach everything important.
- Software upgrades: use ISSU or accept a reload of both; plan the window.
- SVL links must be same speed; 9500 supports specific port ranges only.
- Do not use LACP fast rate expecting faster failover; member loss is detected by link down already.

## Verify
- [ ] Pulling one chassis' uplink loses at most a few packets on a continuous ping.
- [ ] `show stackwise-virtual dual-active-detection` shows the DAD link up.
