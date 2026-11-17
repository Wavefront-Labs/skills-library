---
id: computing-software.systems-network-administration.network-design.firewall-rulebase-design
name: firewall-rulebase-design
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, firewall, firewall-rules, rulebase-design, least-privilege-rules, stateful-firewall, stateless, zone-based-firewall, default-deny, object-groups, rule-ordering, change-request, flow-matrix, ngfw, app-id, ips]
level: practitioner
status: draft
description: "Design a reviewable firewall rule base: stateful vs stateless, zone model, default deny, object naming, rule order and documentation fields, NGFW app-ID and IPS."
sources:
  - https://csrc.nist.gov/pubs/sp/800/41/r1/final
  - https://www.cisecurity.org/controls
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firewall rule base design

## Stateful vs stateless
| | Stateful (firewalls, security groups) | Stateless (router ACLs, cloud NACLs) |
|---|---|---|
| Return traffic | allowed automatically by the session table | needs explicit rules (ephemeral ports, `established`) |
| Protocol awareness | tracks TCP state, helpers for FTP/SIP | none |
| Use | policy enforcement between zones | coarse filtering, anti-spoofing, high-rate edge, CoPP |
Use stateful between trust zones; stateless for infrastructure protection and in front of
firewalls (bogons, DDoS scrubbing).

## Zone model
Define zones by trust and function (Inside-Users, Servers-Prod, DMZ, Guest, Mgmt, PCI, Internet)
and write rules **between zones**. Interfaces belong to zones; never write rules per interface.

## Rule principles
1. **Default deny** at the end of every zone pair, with logging.
2. Least privilege: specific source objects, destination objects and **services** (application-ID
   where available). No `any any` except documented, temporary, and logged.
3. Objects named by meaning: `H-APP-DB01`, `G-PROD-WEB`, `N-10.20.0.0_16-USERS`,
   `SVC-TCP-5432`. Groups for roles, never IPs typed into rules.
4. Order: specific denies (block-lists) first, high-hit allow rules early for performance,
   broad allows later, cleanup deny last. Avoid **shadowed** rules (a later rule never matched
   because an earlier broader rule covers it).
5. Every rule carries: ticket/change ID, owner, business justification, creation date, review
   or expiry date. Use the comment/description fields and tags.

## NGFW features
- App-ID (identify application regardless of port): allow `ms-teams` instead of port ranges;
  pair with "application-default" ports to stop port evasion.
- User-ID (rules by AD group), URL filtering, IPS/threat profiles applied to allow rules,
  TLS decryption policy (with privacy exclusions: banking, health).
- Logging: log at session end for allows; log denies; send to SIEM.

## Request workflow
Flow matrix per application (source, destination, protocol/port, direction, justification),
reviewed by owner + security, implemented via change, verified with a test and the hit counter.

## Verify
- [ ] No unexplained `any` in source, destination or service on allow rules.
- [ ] Every rule has an owner and ticket; zero-hit rules over 90 days flagged for review.
- [ ] Default deny logs show expected traffic only.
