---
id: computing-software.systems-network-administration.cisco-networking.ipv6-ra-guard-and-dhcpv6-guard
name: ipv6-ra-guard-and-dhcpv6-guard
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, ipv6-first-hop-security, ra-guard, dhcpv6-guard, rogue-ra, ipv6-security]
level: practitioner
status: docs-checked
description: "Block rogue IPv6 router advertisements and rogue DHCPv6 servers on access ports with RA Guard and DHCPv6 Guard policies, trusted uplinks, and verification."
sources:
  - https://www.rfc-editor.org/rfc/rfc6105
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ipv6_first_hop_security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 RA Guard and DHCPv6 Guard

A rogue router advertisement (RA), whether malicious or from a misconfigured device, can disrupt every host on a
shared layer-2 segment (RFC 6105 section 1). RA Guard (RFC 6105, Informational) has the layer-2 switch filter RAs:
the simplest form permits RAs only on a port statically set as the router port and blocks them on every other port.
DHCPv6 Guard does the same for DHCPv6 server messages. Syntax below follows the Catalyst 9300 17.9 guide.

## RA Guard
```
ipv6 nd raguard policy HOSTS
 device-role host                 ! host mode: all RAs and router redirects are disallowed on the port
ipv6 nd raguard policy ROUTERS
 device-role router               ! router-facing ports

interface range Gi1/0/1-48
 ipv6 nd raguard attach-policy HOSTS
interface Te1/1/1
 ipv6 nd raguard attach-policy ROUTERS
```
`device-role` accepts host, monitor, router or switch; the default is host. The guide states that with a host policy on
host-facing ports or a VLAN, a policy with `device-role router` on the router-facing ports is mandatory for RA Guard to
work properly. Optional checks in the policy include `hop-limit`, `managed-config-flag`, `other-config-flag`,
`match ipv6 access-list`, `router-preference maximum` and `trusted-port`. A policy can also be attached to VLANs
(`vlan configuration 335` then `ipv6 nd raguard attach-policy HOSTS`) or per interface with
`ipv6 nd raguard attach-policy HOSTS vlan 222,223,224`.

## DHCPv6 Guard
```
ipv6 dhcp guard policy CLIENTS
 device-role client
ipv6 dhcp guard policy SERVERS
 device-role server
interface range Gi1/0/1-48
 ipv6 dhcp guard attach-policy CLIENTS
interface Te1/1/1
 ipv6 dhcp guard attach-policy SERVERS
```
`device-role client` is the default: server messages (replies and advertisements) are dropped on the port. `server`
allows server messages. Optional filters under a server policy: `match server access-list`,
`match reply prefix-list`, `preference max|min` (0 to 255). `trusted-port` sets the port trusted with no further
policing, and when it is configured the `device-role` option is not available, so use one or the other in a policy.

## Verify
```
show ipv6 nd raguard policy HOSTS
show ipv6 dhcp guard policy CLIENTS
```
Test in a lab: send an RA from a host on an access port and confirm other hosts gain no new default route.

## Gotchas
- RA Guard works only if every message between IPv6 devices crosses the controlled layer-2 device. It does nothing on
  shared media such as hubs, or where IPv6 is tunnelled (RFC 6105 section 5).
- If the real gateway sits behind an access port, give that port the router policy or IPv6 breaks.
- A SISF-based device-tracking policy at security level guard blocks external RAs and DHCPv6 server packets even on a
  trusted uplink. Apply an RA Guard or DHCPv6 Guard policy on the uplink, or lower the snooping security level (the
  guide calls that the less preferable option).
- SISF-based device tracking forwards router solicitations only on interfaces with an RA Guard policy that are
  router-facing; with none, solicitations are dropped and onboarding hosts wait for the next unsolicited RA.
- A physical port with an FHS policy cannot join an EtherChannel, and a member port cannot take a policy; attach to the
  EtherChannel interface.

## Checklist
- [ ] Rogue RA test from an access port is dropped.
- [ ] Legitimate hosts still receive the real gateway's RA.

## Checked
Checked 2026-11-08 against RFC 6105 (sections 1, 2, 3, 5) and the Catalyst 9300 17.9 Configuring IPv6 First Hop
Security guide (RA Guard, DHCP Guard, SISF notes, restrictions). Corrected: the SERVERS policy no longer combines
`device-role server` with `trusted-port` (guide says they are exclusive). Removed unsourced claims: the IPv4-only
framing, RA evasion via extension headers or fragments and its fix by newer code, WLC default RA guard, named attack
tools, `show device-tracking counters`, and OS route commands.
Method: documentation only; no commands were run.
