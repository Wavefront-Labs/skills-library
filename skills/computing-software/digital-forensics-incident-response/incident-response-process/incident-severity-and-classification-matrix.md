---
id: computing-software.digital-forensics-incident-response.incident-response-process.incident-severity-and-classification-matrix
name: incident-severity-and-classification-matrix
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [severity-matrix, incident-classification, severity, nist-sp-800-61, dfir]
level: practitioner
status: draft
description: "Build an incident severity and classification matrix from functional, information and recoverability impact, with SLAs and escalation per level."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://www.cisa.gov/federal-incident-notification-guidelines"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident severity and classification matrix

**Goal:** two analysts rate the same incident the same way within five minutes, and the
rating drives who gets woken and how fast.

## Classification (what kind)
Use a fixed category list so metrics work. A workable set, aligned with CISA's federal
notification attack vectors: unauthorised access, malware/ransomware, phishing/BEC, denial of
service, data loss/exfiltration, insider misuse, web application compromise, cloud/identity
compromise, third-party/supply chain, lost or stolen device, other.

## Severity (how bad): score three impacts (NIST SP 800-61r2 3.2.6)
| Factor | None | Low | Medium | High |
|---|---|---|---|---|
| Functional impact | No effect | Minimal, all services continue | Critical service degraded for some users | Critical service unavailable |
| Information impact | None | Non-sensitive internal data | Personal or regulated data exposed | Sensitive data, credentials or IP exfiltrated |
| Recoverability | Regular | Supplemented (more resources) | Extended (unpredictable) | Not recoverable |

Take the **highest** factor as the base severity, then raise for: privileged or domain admin
accounts involved, active attacker presence, media or regulator attention, safety/OT impact.

## Levels and SLAs (example)
| Sev | Meaning | Acknowledge | Bridge | Exec notified | Legal |
|---|---|---|---|---|---|
| SEV1 | Critical outage or confirmed large data theft, active attacker | 15 min | 30 min | 1 h | Immediately |
| SEV2 | Contained compromise of an important system or regulated data at risk | 1 h | 4 h | Same day | Same day |
| SEV3 | Single host or account compromise, no sensitive data | 4 h | as needed | Weekly report | If PII |
| SEV4 | Policy violation, blocked attack | 1 business day | | | |

## Rules that stop arguments
- Severity can move **up or down** as facts change; log every change with the reason.
- Unknown impact is rated as the plausible worst case until scoped.
- Classification and severity are separate fields; "phishing" can be SEV4 or SEV1.
- Keep "breach" out of the matrix; it is a legal determination by counsel.

## Verify
Back-test the matrix on the last 20 closed incidents. If more than a few would change level,
tune the definitions before publishing.
