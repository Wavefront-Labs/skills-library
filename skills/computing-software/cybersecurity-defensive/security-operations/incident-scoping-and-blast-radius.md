---
id: computing-software.cybersecurity-defensive.security-operations.incident-scoping-and-blast-radius
name: incident-scoping-and-blast-radius
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, incident-scoping, blast-radius, ioc-sweep, compromised-accounts, lateral-movement, scoping-matrix]
level: advanced
status: draft
description: "Scope an incident before containing it: pivot from initial indicators to accounts, hosts and data touched, sweep IOCs estate-wide, and keep a living scoping matrix."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf", "https://www.sans.org/white-papers/33901/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident scoping and blast radius

Containing one host while the attacker holds five others and two admin accounts tips them off
and loses the chance to evict them in one move. Scope first (fast), then contain everything at once.

## Start from the initial facts
Known: a host, an account, an IOC, a time. For each, ask:
- **Host**: who logged on (4624 types 3/10, EDR logon events), what ran, what it connected to,
  what persistence exists.
- **Account**: where else it authenticated (DCs 4768/4769/4624, VPN, cloud sign-ins), what it
  changed (group membership, mailbox rules, OAuth consents), MFA events.
- **IOC**: every host/user that touched the hash, domain, IP, or user agent across EDR, proxy,
  DNS, firewall and email logs.
- **Time**: earliest evidence of compromise; extend the search window back past it.

## Iterate (pivot loop)
Each new host or account found becomes a new starting point. Stop when a full loop finds nothing
new. Keep the window wide: dwell times of weeks are normal.

## Scoping matrix (living document)
| Entity | Type | First seen | Evidence | Status (suspected/confirmed/cleared) | Containment action |
Track also: data accessed/exfiltrated (with evidence strength), persistence mechanisms, attacker
tools and infrastructure.

## Estate-wide sweeps
- EDR: hash and filename searches, command-line patterns; Velociraptor/osquery hunts for
  persistence artefacts and tool names.
- Identity: sign-ins from attacker IPs/ASNs, impossible travel, new MFA devices.
- Email: messages from the same sender/infrastructure (message trace), then purge.
- Network: connections to C2 IPs/domains in flow, DNS and proxy logs.

## Data impact
Determine what data the attacker could access (permissions of compromised accounts) vs evidence
they did access it (file access logs, SharePoint audit, database logs, egress volume). Legal and
notification decisions depend on this distinction.

## Then contain in a coordinated window
Reset all confirmed accounts, isolate all confirmed hosts, block infrastructure and remove
persistence at the same time; prepare for the attacker's reaction.

## Gotchas
- Logging gaps limit scoping; record them explicitly as "unknown", not "clear".
- Service accounts and shared admin accounts are often the real blast radius.
- Cloud and SaaS tenants are frequently forgotten in on-prem incidents.

## Verify
Scope review with a second senior responder: every confirmed entity has evidence, every pivot
has been followed, and gaps are documented.
