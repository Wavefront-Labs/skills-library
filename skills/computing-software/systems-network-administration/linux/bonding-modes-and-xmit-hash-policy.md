---
id: computing-software.systems-network-administration.linux.bonding-modes-and-xmit-hash-policy
name: bonding-modes-and-xmit-hash-policy
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bonding, bond-modes, xmit-hash-policy, lacp, balance-alb, proc-net-bonding, link-aggregation]
level: advanced
status: docs-checked
description: "Pick the right Linux bond mode (active-backup, 802.3ad, balance-xor/tlb/alb), set xmit_hash_policy so traffic spreads, match switch config, and read /proc/net/bonding."
sources:
  - https://docs.kernel.org/networking/bonding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bond modes and hashing

## Modes
| Mode | Name | Switch config | Notes |
|---|---|---|---|
| 0 | balance-rr | static LAG (EtherChannel-compatible mode) | packet reordering; the module default mode |
| 1 | active-backup | none | failover only; simplest, works across two independent switches |
| 2 | balance-xor | static LAG | hash-based spread, no negotiation |
| 3 | broadcast | — | special cases only |
| 4 | 802.3ad (LACP) | switch must support IEEE 802.3ad; most need it enabled per port-channel | dynamic aggregation; selects slaves with the transmit hash policy |
| 5 | balance-tlb | none | transmit load balancing; receive on one link |
| 6 | balance-alb | none | tlb + receive load balancing for IPv4 via ARP negotiation |

## Hash policy (balance-xor, 802.3ad and balance-tlb)
`xmit_hash_policy=layer2` (default: MACs and packet type, so all traffic to one peer such as the gateway uses one link), `layer2+3`,
`layer3+4` (IP and ports; one connection never spans slaves), `encap2+3` and `encap3+4` (inner headers for tunnels),
`vlan+srcmac` (per-VLAN spread for a bond shared by VMs, without LACP hardware). A single connection never exceeds one link's speed.
```bash
nmcli con add type bond ifname bond0 con-name bond0 bond.options "mode=802.3ad,miimon=100,lacp_rate=fast,xmit_hash_policy=layer3+4"
nmcli con add type ethernet ifname eth0 master bond0 ; nmcli con add type ethernet ifname eth1 master bond0
```
## Read the state
```bash
cat /proc/net/bonding/bond0
# shows the bonding mode, MII status and per-slave state; for 802.3ad also the LACP aggregator and partner details
```
`ip -d link show bond0`, `ethtool -S eth0` for per-link counters. Per-field output of `/proc/net/bonding` varies by kernel and mode; read it against the bonding documentation.

## Gotchas
- LACP on host + static on switch (or vice versa) = flapping or one link only.
- `miimon=100` (link monitoring; the documented default when `arp_interval` is unset) or `arp_interval`/`arp_ip_target` (up to 16 targets) for failures beyond the local link. Do not enable both: ARP and MII monitoring are mutually exclusive.
- `lacp_rate` defaults to `slow` (partner sends LACPDUs every 30 s); `fast` is every 1 s.

## Verify
- [ ] `/proc/net/bonding/bond0` shows every slave with `MII Status: up` and the intended mode and hash policy; with 802.3ad the slaves aggregate with the switch; pulling a cable keeps traffic flowing.

## Checked

Date: 2026-10-25. Documentation release: Linux kernel Documentation/networking/bonding.rst (torvalds/linux master, read 2026-10-25).
Confirmed: mode names and numbers 0-6 (balance-rr is the default mode); modes 0 and 2 described as EtherChannel-compatible; 802.3ad needs a switch supporting IEEE 802.3ad; tlb and alb need no special switch support; `xmit_hash_policy` applies to balance-xor, 802.3ad and tlb with values layer2 (default), layer2+3, layer3+4, encap2+3, encap3+4, vlan+srcmac; `miimon` default 100 if `arp_interval` unset; `lacp_rate` slow/fast and default slow; ARP and MII monitoring are exclusive; ARP target limit 16.
Removed as unconfirmed: sample `/proc/net/bonding` field names (Aggregator ID, Partner Mac), the LACP "mode active" switch wording, MLAG advice and the alb/bridge claim; the Red Hat URL (Red Hat docs are not readable here).

Method: documentation only; no commands were run.
