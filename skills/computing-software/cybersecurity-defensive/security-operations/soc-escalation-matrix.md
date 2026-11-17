---
id: computing-software.cybersecurity-defensive.security-operations.soc-escalation-matrix
name: soc-escalation-matrix
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-management, escalation-matrix, severity-levels, on-call, incident-commander, raci, notification-thresholds, soc]
level: practitioner
status: draft
description: "Build a SOC escalation matrix: severity criteria, who is engaged at each level, response time targets, contact routes and when to wake executives."
sources: ["NIST SP 800-61r3 (roles and responsibilities, communication)", "CSF 2.0 RS.MA-02/RS.MA-03 (triage and categorisation)", "CySA+ CS0-003 objective 3.2 and 4.2"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SOC escalation matrix

**Goal:** any analyst at 3 a.m. knows exactly whom to call, how fast, and with what authority,
for each kind of security event.

## Severity criteria (example; adapt impact terms to the business)
| Sev | Criteria (any) | Examples |
|---|---|---|
| 1 Critical | Confirmed active attacker with privileged access; ransomware executing; confirmed exfiltration of regulated data; safety impact | Domain admin compromise, encryption spreading |
| 2 High | Confirmed compromise of a single host/account with potential to spread; sensitive data exposed | Malware with C2 on one server; BEC with payment fraud attempt |
| 3 Medium | Suspicious activity needing investigation; contained malware | Commodity malware blocked post-execution |
| 4 Low | Policy violation, blocked attempt | Phish reported and blocked |

## Matrix
| Sev | Engage | Response target | Route | Decision authority |
|---|---|---|---|---|
| 1 | SOC lead, IR lead (incident commander), CISO, IT ops on-call, legal | 15 min | Phone/pager, bridge opened | IC may isolate any system incl. production |
| 2 | SOC lead, IR on-call, asset owner | 30 min | Pager + case | IC may isolate non-critical systems; production needs owner OK within 1 h |
| 3 | SOC tier 2 | 4 h | Case queue | Analyst |
| 4 | Tier 1 | Next business day | Case queue | Analyst |

Add rows for special triggers regardless of severity: law enforcement contact, media
inquiry, executive/VIP account involved, third-party (supplier) breach notification.

## Make it work
- Contact list with primary and backup and out-of-hours numbers, tested quarterly (call the numbers).
- Pre-authorised actions per severity written down; nothing slows containment like waiting for permission at night.
- Escalation is cheap, de-escalation is normal: say so explicitly to junior analysts.
- Record each escalation time in the case to measure against targets.

## Gotchas
- Severity based only on technical scope misses business impact (a small breach of payroll data is high).
- Matrices kept in a wiki that is unavailable during an outage: keep an offline copy.
- Overusing Sev 1 burns out responders; review classifications after each incident.

## Verify
- [ ] Quarterly test call to each escalation contact recorded.
- [ ] Last 10 incidents' escalation times compared with the matrix targets.
