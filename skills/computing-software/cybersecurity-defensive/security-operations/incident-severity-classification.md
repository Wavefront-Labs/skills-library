---
id: computing-software.cybersecurity-defensive.security-operations.incident-severity-classification
name: incident-severity-classification
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, incident-severity-classification, severity-matrix, triage, escalation, impact-assessment, nist-800-61]
level: practitioner
status: draft
description: "Classify incidents by type and severity with a matrix of functional, information and recoverability impact, mapping each level to escalation and response times."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://www.cisa.gov/news-events/news/cisa-national-cyber-incident-scoring-system-nciss", "https://www.enisa.europa.eu/publications/reference-incident-classification-taxonomy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident classification and severity

**Goal:** consistent, fast severity calls that drive who is woken up and how fast,
independent of which analyst is on shift.

## Classify the type
Use a short fixed taxonomy (based on ENISA RITC / NIST categories): malware, ransomware,
account compromise, phishing/BEC, unauthorised access, data exposure/exfiltration, denial
of service, insider misuse, web application compromise, third-party/supply chain, policy
violation. Type selects the playbook.

## Score the impact (NIST 800-61 factors)
- **Functional impact:** none, low (minimal efficiency loss), medium (a critical service
  degraded for some users), high (critical service unavailable).
- **Information impact:** none, privacy breach (personal data), proprietary breach,
  integrity loss (data changed).
- **Recoverability:** regular (existing resources), supplemented (extra resources, predictable),
  extended (unpredictable, outside help), not recoverable.
Plus scope: number of hosts/accounts, privileged accounts involved, crown-jewel systems.

## Example matrix
| Severity | Criteria (any) | Response |
|---|---|---|
| SEV1 Critical | Ransomware spreading; domain admin/tenant admin compromise; confirmed exfiltration of regulated data; critical service down | IC within 15 min, execs and legal immediately, 24x7 until contained |
| SEV2 High | Confirmed compromise of servers or privileged account, contained scope; personal data possibly exposed | IC within 1 h, legal informed same day |
| SEV3 Medium | Single workstation/user compromise, no privileged access, no data loss indicated | SOC handles in business hours, daily updates |
| SEV4 Low | Blocked attack, policy violation, no compromise | Ticket, normal queue |

## Rules
- Classify on what is known now and **re-assess at each update**; severity can go up or down.
- When unsure between two levels, pick the higher and downgrade later.
- Regulatory clocks (GDPR 72 h, sector rules) start at awareness, so personal data
  involvement forces legal notification regardless of technical severity.
- Record the rationale in the case: which criteria met.

## Gotchas
- Severity based only on alert severity from a tool misses business impact.
- "Critical" used for everything burns out on-call; keep SEV1 rare and real.

## Verify
Give five past incidents to three analysts separately; they should land on the same
severity. Disagreements show criteria that need sharper wording.
