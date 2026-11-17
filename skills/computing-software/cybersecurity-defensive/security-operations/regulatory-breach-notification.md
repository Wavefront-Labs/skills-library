---
id: computing-software.cybersecurity-defensive.security-operations.regulatory-breach-notification
name: regulatory-breach-notification
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-reporting, regulatory-notification, gdpr-article-33, sec-8-k-item-1-05, nis2, hipaa-breach-notification, cert-in, breach-notification, notification-timelines]
level: practitioner
status: draft
description: "Track and meet breach notification clocks (GDPR 72h, NIS2 24h/72h, SEC 4 business days, HIPAA 60 days, state laws) with security feeding legal accurate facts."
sources: ["GDPR Articles 33 and 34", "NIS2 Directive (EU) 2022/2555 Article 23", "SEC Form 8-K Item 1.05 cybersecurity incident disclosure rule (2023)", "HHS HIPAA Breach Notification Rule 45 CFR 164.400-414"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regulatory breach notification timelines

**Goal:** security gives legal the facts needed to decide and file notifications on time.
Legal owns the decision; this skill is the security team's part. Confirm current rules with
counsel: they change and vary by jurisdiction and sector.

## Common clocks (verify for your jurisdictions)
| Regime | Trigger | Deadline | To |
|---|---|---|---|
| GDPR Art. 33 | Personal data breach likely to result in risk | 72 hours from awareness | Supervisory authority; Art. 34 to individuals without undue delay if high risk |
| UK GDPR | Same | 72 hours | ICO |
| NIS2 Art. 23 | Significant incident (essential/important entities) | Early warning 24 h, notification 72 h, final report 1 month | National CSIRT/authority |
| DORA (EU financial) | Major ICT incident | Initial report within hours of classification (per RTS) | Competent authority |
| SEC 8-K Item 1.05 (US public companies) | Material cybersecurity incident | 4 business days after determining materiality | SEC filing |
| HIPAA | Breach of unsecured PHI | Without unreasonable delay, max 60 days; HHS (immediately if 500+) | Individuals, HHS, media if 500+ in a state |
| US state laws | Personal information breach | Varies (e.g. 30-60 days in many states) | Residents, sometimes AG |
| CIRCIA (US critical infrastructure) | Covered incident / ransom payment | 72 h / 24 h once final rule applies | CISA |
| PCI DSS | Card data compromise | Immediately per card brand rules | Acquirer / brands |

## What security must provide, fast
1. Time of awareness (documented; this starts most clocks).
2. Nature of the incident and systems affected.
3. Data categories and approximate number of records and individuals; jurisdictions of data subjects.
4. Whether data was encrypted and whether keys were exposed.
5. Evidence for or against exfiltration, with confidence.
6. Containment status and measures taken.
7. Likely consequences and mitigation for individuals.

## Practice
- Maintain a data inventory mapping systems to data categories and jurisdictions before incidents.
- Use a notification decision log: date/time, facts known, decision, who decided.
- Phased reporting is allowed under GDPR and NIS2: file what you know on time, then update.

## Gotchas
- Awareness is not "investigation complete"; delaying to be certain misses the clock.
- Ransomware with encryption only can still be a reportable breach (availability, and exfiltration often follows).
- Contracts with customers often impose shorter notice periods (24-48 h) than the law.

## Verify
- [ ] Notification matrix for your organisation reviewed by legal in the last year.
- [ ] Each past incident's awareness time and notification times recorded.
