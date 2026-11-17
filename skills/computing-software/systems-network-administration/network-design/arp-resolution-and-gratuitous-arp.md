---
id: computing-software.systems-network-administration.network-design.arp-resolution-and-gratuitous-arp
name: arp-resolution-and-gratuitous-arp
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, arp-process, gratuitous-arp, arp-cache, proxy-arp, ip-conflict, osi-model]
level: practitioner
status: docs-checked
description: "Explain and troubleshoot ARP: request/reply flow, cache timers, gratuitous ARP for failover and conflict detection, proxy ARP surprises, and stale entries after moves."
sources:
  - https://www.rfc-editor.org/rfc/rfc826
  - https://www.rfc-editor.org/rfc/rfc5227
  - https://www.cisco.com/c/en/us/support/docs/ip/dynamic-address-allocation-resolution/13718-5.html
  - https://man7.org/linux/man-pages/man8/arping.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARP resolution and gratuitous ARP

## Flow
1. Host needs to send to an on-link IP (or to its gateway for off-link destinations).
2. Cache miss -> broadcast ARP request (`who-has 10.0.0.1 tell 10.0.0.20`).
3. Owner replies unicast with its MAC; both sides cache.

Destination off-subnet -> ARP for the **gateway**, not the remote host. A host ARPing for remote
IPs has a wrong mask or relies on proxy ARP.

## Timers and caches
ARP cache timeouts and switch MAC aging differ per platform; look them up in the vendor docs.
An ARP timeout much longer than the switch MAC aging time can cause unicast flooding for silent
hosts: align the two on routers facing hosts.

## Gratuitous ARP (GARP)
ARP with sender IP = target IP. Uses: announce a new MAC after VRRP/HSRP/firewall failover or VM
migration; duplicate-address detection at boot (RFC 5227 ARP probes with sender IP 0.0.0.0).
If failover "works but traffic stalls for minutes", upstream devices are ignoring GARP (some
firewalls/providers do): lower their ARP timeout or use a virtual MAC that does not change.

## Commands
```
ip neigh show                 # Linux
arp -a                        # Windows/macOS
arping -I eth0 -c 3 10.0.0.1  # who answers for this IP
```

## Faults
- Two MACs answering for one IP -> address conflict (arping shows replies from both).
- Proxy ARP on a router answering for everything hides mask errors; `no ip proxy-arp` on SVIs.
- Incomplete entries -> host down, wrong VLAN, or ARP blocked by DAI (check DHCP snooping bindings).

## Verify
- [ ] After a failover test, upstream ARP entries point at the new active MAC within seconds.

## Checked
2026-10-28. Confirmed against RFC 826 (request/reply, cache of sender pair, broadcast request), RFC 5227 (ARP Probe has an all-zero sender IP; ARP Announcement) and the Cisco proxy ARP note (proxy ARP on by default on IOS, `no ip proxy-arp`). Removed: the EtherType value, the per-platform timer table and `arp timeout` figure, and two Cisco show commands, none of which the sources state.
Method: documentation only; no commands were run.
