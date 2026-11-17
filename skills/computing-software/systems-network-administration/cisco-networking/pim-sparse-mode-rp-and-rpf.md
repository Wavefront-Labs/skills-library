---
id: computing-software.systems-network-administration.cisco-networking.pim-sparse-mode-rp-and-rpf
name: pim-sparse-mode-rp-and-rpf
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, multicast, pim, pim-sparse-mode, rendezvous-point, rp, rpf-check, mroute, show-ip-mroute, static-mroute]
level: advanced
status: docs-checked
description: "Diagnose multicast on IOS with show ip mroute, show ip pim neighbor and show ip rpf: reading (*,G) and (S,G) entries, RPF failures, how RPF is chosen, static mroute fix."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/ip-multicast/16450-mcastguide0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multicast RPF and mroute diagnosis

Scope: reading the multicast routing table and fixing reverse path forwarding (RPF) failures, as in Cisco's IP
multicast troubleshooting guide. For enabling PIM, RP choice (static, Anycast, BSR, Auto-RP) and SSM, use Cisco's
PIM configuration guide for your platform; those parts are not covered here.

## Read the multicast table
```
show ip mroute 224.1.1.1
show ip pim neighbor
show ip mroute 224.1.1.1 count
show ip rpf 10.1.1.1
```
- `show ip mroute` flags in the guide's output: D dense, S sparse, C connected, L local, P pruned, R RP-bit set,
  F register flag, T SPT-bit set, J join SPT, M MSDP created entry, A advertised via MSDP (newer output adds B bidir
  group and s SSM group). Entries are `(*, G)` for the shared tree and `(S, G)` per source, each with an
  incoming interface, an RPF neighbour, and an outgoing interface list.
- Check that the downstream router lists its upstream router in `show ip pim neighbor` first; in the guide's case the
  adjacency was fine and the fault was RPF.

## RPF failure
The guide's symptom: hosts on one router receive the feed and hosts behind the next router do not. On the failing
router `show ip mroute` showed an incoming interface (Ethernet2/0) different from the expected one (Ethernet3/1),
`show ip mroute <group> count` showed all packets in the "Other" counts as RPF-failed (Total 471, RPF failed 471),
and `show ip rpf <source>` showed the interface chosen and the RPF type (`unicast (static)`). With debugging, packets
were dropped as "not RPF interface" even though they arrived on the correct link.

How IOS picks the RPF interface (per the guide):
1. Sources searched for a match on the source address: the unicast routing table, MBGP table, DVMRP table and static
   mroute table. With shared trees the RP address is used instead of the source address.
2. If more than one route matches, the lowest administrative distance wins.
3. If distances are equal, the order of preference is static mroutes, DVMRP, MBGP, then unicast routes.
4. Within a single table the longest match is used.

In the example a static /32 unicast route pointed the wrong way and made the wrong interface the RPF interface.

## Fix
Either change the unicast routing so the RPF interface is the one the traffic arrives on, or add a static mroute to
force the RPF path regardless of the unicast table:
```
ip mroute 10.1.1.1 255.255.255.255 10.2.1.1
```
Afterwards `show ip rpf 10.1.1.1` showed RPF interface Ethernet3/1, neighbour 10.2.1.1 and RPF type `static mroute`,
and the packet counters in `show ip mroute count` increased.

## Verify
- [ ] `show ip pim neighbor` lists the upstream router on each transit link.
- [ ] `show ip mroute <group>` has an (S,G) entry whose incoming interface matches the link the traffic arrives on.
- [ ] `show ip mroute <group> count` shows forwarded packets increasing and no RPF-failed drops.

## Checked
Checked 2026-11-08 against Cisco's IP multicast troubleshooting guide (document 16450, RPF failure section). The
Cisco IOS XE PIM configuration book returned only a stub, so these were removed as unconfirmed: `ip multicast-routing`
and `ip pim sparse-mode` lines, static RP, SPT threshold, Anycast RP with MSDP, BSR and Auto-RP, SSM
(`ip pim ssm default`, IGMPv3), and the example addresses and flags of the earlier draft.
Method: documentation only; no commands were run.
