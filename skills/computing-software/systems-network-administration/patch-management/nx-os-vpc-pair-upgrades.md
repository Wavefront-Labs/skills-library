---
id: computing-software.systems-network-administration.patch-management.nx-os-vpc-pair-upgrades
name: nx-os-vpc-pair-upgrades
category: computing-software
field: systems-network-administration
product: patch-management
tags: [nxos-upgrade, nx-os, vpc, nexus, install-all, network-device-patching]
level: practitioner
status: draft
description: "Upgrade Cisco Nexus switches in a vPC pair with no outage: compatibility checks, install all impact, upgrade order (secondary then primary), and post-checks."
sources:
  - https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/104x/upgrade/cisco-nexus-9000-series-nx-os-software-upgrade-and-downgrade-guide-104x.html
  - https://www.cisco.com/c/en/us/support/docs/switches/nexus-9000-series-switches/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NX-OS vPC pair upgrades

Hosts dual-homed via vPC keep running while one peer reloads, if you upgrade one peer at a time and verify in between.

## Pre-checks (both peers)
```text
show version
show vpc brief                        ! peer status ok, keepalive alive, consistency success
show vpc consistency-parameters global
show port-channel summary
show spanning-tree summary
show install all impact nxos bootflash:nxos64-cs.10.4.3.F.bin   ! disruptive? per module
show incompatibility-all nxos bootflash:nxos64-cs.10.4.3.F.bin
```
Check the upgrade path in the guide (some versions need an intermediate hop). Save configs and copy to a server.

## Order
1. Upgrade the **vPC operational secondary** first:
```text
copy scp://user@10.0.0.5/nxos64-cs.10.4.3.F.bin bootflash: vrf management
show file bootflash:nxos64-cs.10.4.3.F.bin sha512sum
install all nxos bootflash:nxos64-cs.10.4.3.F.bin
```
2. Wait for it to return, vPC peer adjacency up, all vPCs up, consistency success, MAC/ARP tables populated; allow a few minutes for vPC delay-restore.
3. Upgrade the primary the same way.

## During
- The upgrading peer's vPC member ports go down; traffic shifts to the other peer. Orphan ports (single-attached) on the reloading switch lose connectivity.
- Mixed-version vPC pairs are supported temporarily; finish both in the same window.

## Gotchas
- Enhanced ISSU (non-disruptive) works only on supported platforms/versions with `boot mode lxc`; most 9k upgrades are disruptive per switch.
- `install all` may also upgrade BIOS/EPLD; EPLD upgrades are separate (`install epld`) and disruptive.
- Peer-keepalive on mgmt0: ensure management connectivity, or a dual-active scenario follows.

## Verify
Both peers on the target version, `show vpc` all up and consistent, no orphan-port outages beyond expected, routing adjacencies and HSRP/VRRP states as before.
