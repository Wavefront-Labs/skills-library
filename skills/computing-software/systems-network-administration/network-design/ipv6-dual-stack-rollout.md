---
id: computing-software.systems-network-administration.network-design.ipv6-dual-stack-rollout
name: ipv6-dual-stack-rollout
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ipv6, dual-stack, ipv6-deployment, happy-eyeballs, ra-guard, ipv6-security, rollout-plan]
level: practitioner
status: docs-checked
description: "Roll out dual-stack IPv6 in an enterprise in safe phases: core and DMZ first, security parity, RA Guard and DHCPv6 Guard, monitoring, and Happy Eyeballs effects."
sources:
  - https://www.rfc-editor.org/rfc/rfc8305
  - https://www.rfc-editor.org/rfc/rfc6105
  - https://www.rfc-editor.org/rfc/rfc9099
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual-stack IPv6 rollout

Dual stack: every host and link runs IPv4 and IPv6 side by side. The usual path, and the
point where IPv6 problems become user-visible (apps prefer IPv6 when it is present).

## Phases
1. **Plan:** address plan (nibble-aligned prefix per site), IPAM, training, inventory of IPv6-capable
   kit/software (firewalls, load balancers, proxies, monitoring, logging parsers).
2. **Core and WAN:** routing (OSPFv3 or BGP with the IPv6 address family).
3. **DMZ / external services:** AAAA for websites/mail behind dual-stack LBs; the quickest
   external win and low risk.
4. **Security parity:** every IPv4 ACL/firewall rule has an IPv6 equivalent; IPv6 ICMP
   types required for PMTUD and ND permitted.
5. **Access layer:** per VLAN, SLAAC or DHCPv6; first-hop security: **RA Guard** (RFC 6105)
   and the other first-hop protections your switches offer.
6. **Clients** in pilot groups, then broad rollout.

## Happy Eyeballs (RFC 8305)
Clients race IPv6 and IPv4 with short delays (RFC 8305 recommends a 50 ms Resolution Delay and a
250 ms default Connection Attempt Delay). Broken IPv6 is
hidden as slight delay instead of failure, which makes problems hard to see: monitor IPv6
success rates explicitly.

## Gotchas
- IPv6 may already be on: hosts with IPv6 enabled can accept router advertisements from any device on the link.
  Enable RA Guard before or during rollout, not after.
- Logging/SIEM parsers that expect dotted quads drop IPv6 events silently.
- Proxy PAC/WPAD and split DNS need AAAA-aware rules.
- MTU: blocking ICMPv6 Packet Too Big breaks path MTU discovery.

## Verify
- [ ] Per phase: IPv6 reachability tests from clients, IPv6 traffic share in NetFlow, firewall rule parity report, RA Guard drop counters.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 8305 Resolution Delay 50 ms and Connection Attempt Delay 250 ms; RFC 6105 defines RA-Guard.
- Removed: the /48, /127 and /128 sizes, the RFC 4890 reference and the DHCPv6 Guard attribution to RFC 6105, the 'routers do not fragment' remark, test-ipv6.com and curl -6.

Method: documentation only; no commands were run.
