---
id: computing-software.cybersecurity-defensive.network-defence.nat-policy
name: nat-policy
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [nat-policy, source-nat, destination-nat, port-forwarding, hairpin-nat, firewall-policy, nat-security]
level: practitioner
status: draft
description: "Write secure NAT policy: destination NAT exposure review, matching security rules to pre/post-NAT addresses, SNAT for egress attribution, hairpinning and logging translations."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-networking-admin/nat", "https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/", "https://csrc.nist.gov/pubs/sp/800/41/r1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NAT policy security

## Principles
- NAT is not a security control; the security policy is. But destination NAT (port forwarding) **is** exposure, so every DNAT rule needs the same scrutiny as an inbound allow rule.
- Inventory DNAT/VIPs regularly against the external attack surface scan; forgotten port forwards (RDP 3389 to an internal host) are a classic initial access vector.

## Rule matching gotchas (PAN-OS)
- NAT policy evaluates using **pre-NAT** zones and addresses.
- Security policy uses **pre-NAT IP addresses** but **post-NAT zone** for destination NAT. Getting this wrong produces "allow" rules that never match or match too broadly.
- FortiGate: VIP objects referenced in firewall policies (policy uses the VIP as destination); "match-vip" settings affect deny policies.

## Source NAT
- Dedicated egress IPs per zone or per sensitive segment so external logs (SaaS, partners) attribute traffic.
- SNAT pool exhaustion causes intermittent failures; monitor port allocation.

## Hairpin / U-turn NAT
Internal users reaching an internal server by its public IP; configure explicitly or use split DNS -
prefer split DNS to avoid confusing logs.

## Logging
Log translated addresses and ports (session logs include NAT source/destination); keep for attribution
requests (law enforcement asks "who had public IP x:port at time t").

## Verify
- [ ] Every DNAT rule has an owner, ticket and matching restrictive security rule (source restricted where possible).
- [ ] External scan shows only intended services.
- [ ] NAT logs retained per policy.
