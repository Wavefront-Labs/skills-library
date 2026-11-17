---
id: computing-software.cybersecurity-defensive.network-defence.ipv6-first-hop-security
name: ipv6-first-hop-security
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ra-guard, ipv6-first-hop-security, dhcpv6-guard, rogue-router-advertisement, network-access-control]
level: advanced
status: docs-checked
description: "Protect access networks against rogue IPv6 Router Advertisements with RA-Guard (RFC 6105) and the RFC 7113 implementation rules that stop fragment evasion."
sources: ["https://datatracker.ietf.org/doc/html/rfc6105", "https://datatracker.ietf.org/doc/html/rfc7113"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 first-hop security and RA-Guard

Without SEND on all devices, a rogue Router Advertisement (RA), malicious or from a misconfigured router, on a
shared L2 segment can disrupt every IPv6 host on it. RA-Guard (RFC 6105) filters RAs in the L2 fabric.

## RA-Guard model (RFC 6105)
- Applies only where all messages between IPv6 end devices traverse the controlled L2 device. It does not
  protect shared media such as hubs, and does not protect where IPv6 traffic is tunnelled.
- It complements SEND rather than replacing it, filtering RAs by criteria from "RA disallowed on this
  interface" up to "RA allowed only from authorised sources".
- **Stateless**: decide from the frame or device configuration: sender link-layer address, receiving port,
  IP source address, prefix list, router priority. Simplest form: one port statically marked as the router
  port forwards RAs and all other ports block them.
- **Stateful (learning)**: states OFF, LEARNING, BLOCKING, FORWARDING. During a manually started learning
  period the device records which ports have valid routers; afterwards ports without one block RAs and ports
  with one forward them.
- **SEND-based**: the L2 device validates the CGA and RSA signature and the router certificate chain against
  a provisioned trust anchor, and drops RAs that fail.
- Security note from the RFC: enter LEARNING only intentionally by manual configuration, and have the network
  manager verify the learned router list against the expected one.

## Evasion and the RFC 7113 rules
RFC 7113 (updates RFC 6105) describes evading RA-Guard with IPv6 extension headers (for example a
Destination Options header) combined with fragmentation, so that the fragment carrying the ICMPv6 header
cannot be identified. Its implementation rules include:
- Do not limit the number of bytes inspected when parsing the header chain; an implementation with such a
  limit must pass the packet at the limit and must not claim compliance.
- A first fragment (Fragment Offset 0) that does not contain the entire header chain up to and including the
  upper-layer header must be dropped and should be logged as a security fault.
- A packet identified as a Router Advertisement, or with an unrecognised Next Header value, must be dropped;
  the knob controlling dropping of unrecognised Next Header values must default to "drop".
- Otherwise pass the packet. Provide a dedicated RA-Guard drop counter.
RFC 7113 also says similar protection for forged DHCPv6 messages can be circumvented with the same
techniques, so apply the same scrutiny to DHCPv6 guard features.

## Practical checks
- Choose switch and wireless platforms whose documentation states RFC 7113 behaviour; the vendor
  configuration syntax is not covered here, take it from your platform's current documentation.
- Mark only uplinks to real routers as router ports; everything else is a host port.

## Verify
- [ ] A lab host sending RAs from a host port is dropped and the drop counter increments.
- [ ] An RA wrapped in extension headers and fragmented is also dropped (lab test).
- [ ] Real router uplinks still deliver RAs to hosts.

## Checked
Checked 2026-11-09 against RFC 6105 and RFC 7113 (both read in full). Removed: the Cisco SISF configuration
block and device-tracking claims (Cisco page returned 404), mitm6, DHCPv6 Guard and ND inspection details,
the IPv4-only advice including DisabledComponents, the Windows Firewall mitigation and wireless controller
settings, none of which these pages confirm.
Method: docs-checked 2026-11-09 against RFC 6105 and RFC 7113.
