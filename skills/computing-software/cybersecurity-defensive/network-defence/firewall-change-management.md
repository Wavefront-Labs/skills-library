---
id: computing-software.cybersecurity-defensive.network-defence.firewall-change-management
name: firewall-change-management
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [firewall-change-management, firewall-rule-request, change-control, rule-recertification, firewall-policy, cis-control-12]
level: practitioner
status: draft
description: "Run firewall change management: rule request fields, risk review, peer approval, implementation and verification, emergency changes, rule expiry and recertification."
sources: ["https://www.cisecurity.org/controls/v8", "https://csrc.nist.gov/pubs/sp/800/41/r1/final", "https://docs-cortex.paloaltonetworks.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firewall change management

## Rule request (required fields)
Requester and business owner, application, source (host/subnet/group, not "any"), destination, service
(port/protocol or App-ID), direction, justification, data classification, **expiry/review date**,
ticket ID. Reject requests with `any` in more than one field without architect sign-off.

## Review
1. Does an existing rule/object already cover it (avoid duplicates)?
2. Risk: internet-exposed? crosses a zone boundary (PCI, OT, tier 0)? clear-text protocol? broad ranges?
3. Peer review of the exact rule text (diff), not the request.
4. Approval: owner of the destination zone/system.

## Implement
- In the change window, with a rollback plan (config snapshot / commit revert: PAN-OS `load config version`, FortiGate revision history).
- Rule name/description carries the ticket ID and expiry; place above any broader deny.
- Log at session end on every rule.
- Policy-as-code where possible (Terraform providers for PAN-OS/Fortinet/cloud firewalls) with pipeline checks.

## Verify after change
- Requester confirms the flow works; hit count increases; no unrelated drops spike.
- Unused for 90 days -> flag for removal (see firewall-rule-cleanup).

## Emergency changes
Allowed with verbal approval for incidents; must be ticketed and reviewed within 24-72 h.

## Recertification
Annual (PCI DSS: review rule sets at least every 6 months) - owners reconfirm each rule or it is disabled then removed.

## Gotchas
- Changes made directly on devices outside the process: compare running config to the approved source daily (config backup diff, Tufin/AlgoSec/FireMon change reports) and alert on unapproved diffs.
- Expiry dates that nobody enforces; automate reports of expired rules.

## Verify
- [ ] Sample of last month's changes all trace to approved tickets.
- [ ] Unapproved diff alerting in place.
