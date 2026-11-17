---
id: computing-software.systems-network-administration.network-design.firewall-nat-rule-ordering
name: firewall-nat-rule-ordering
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, firewall-design, firewall-nat, nat-order-of-operations, pre-nat-post-nat, static-nat]
level: practitioner
status: docs-checked
description: "Get NAT and security policy order right on firewalls: pre- vs post-NAT addresses per vendor, manual vs auto NAT sections, twice NAT, hairpin NAT and no-NAT exemptions."
sources:
  - https://www.cisco.com/c/en/us/td/docs/security/asa/asa920/configuration/firewall/asa-920-firewall-config/nat-basics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall NAT rule ordering

## Which address does the security rule use?
Vendors differ on whether security policy is evaluated on the original (pre-NAT) or translated (post-NAT) address, and
which zone or interface is used for the destination. Getting this wrong is a common cause of "NAT works but traffic is
denied". Look this up for your platform and software version in the vendor's order-of-operations document before
writing rules; do not rely on a cross-vendor rule of thumb. (The Palo Alto knowledge-base article in `sources` returned
no readable text in this review.)

## Cisco ASA NAT order (ASA 9.2 NAT basics)
The NAT rules sit in one table in three sections, applied in order until a match is found:
1. **Section 1, twice NAT**: first match, in configuration order. Put specific rules before general ones: static before
   dynamic, and rules with destination translation before rules with source translation only. Twice NAT rules are added
   here by default.
2. **Section 2, network object NAT**: static rules, then dynamic rules; within each type, the smaller quantity of real
   addresses first, then the lower address number, then the object name alphabetically.
3. **Section 3, twice NAT**: first match, in configuration order; keep your most general rules here (`after-auto`).
Identity NAT translates an address to itself, which bypasses NAT: place such exemptions (for example VPN traffic) so they
match before a broad dynamic rule.

## Common designs
- **Static NAT / port forward** for published servers; restrict by source where possible.
- **Hide NAT / PAT** for outbound users.
- **No-NAT (identity) exemption** for site-to-site VPN and internal routed traffic.
- **Hairpin NAT**: internal clients reaching a server through its public address need translation on the inside
  interface; split DNS returning the private address avoids it.
- **Twice NAT** for overlapping networks.

## Testing
Use the platform's packet-simulation or policy-match tooling to see which NAT and security rule a test flow hits
(for example Packet Tracer on ASA); check your vendor's CLI reference for the exact command.

## Verify
- [ ] For each published service, the test tool shows the expected NAT rule and security rule; no-NAT exemptions hit
  before PAT.

## Checked
2026-10-28. Confirmed in the Cisco ASA 9.2 "NAT basics" page: three NAT sections and their ordering rules, identity NAT,
`after-auto`. Removed as unconfirmed: the per-vendor pre-NAT/post-NAT table (Palo Alto, FortiGate, Check Point, ASA ACL
statement), PAT flow-count figure, specific test commands for Palo Alto and FortiGate, and the "prefix length" ordering
(the page orders by number of real addresses).
Method: documentation only; no commands were run.
