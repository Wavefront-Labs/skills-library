---
id: computing-software.systems-network-administration.backup-and-recovery.ransomware-breach-notification
name: ransomware-breach-notification
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [breach-notification, ransomware-recovery, gdpr-article-33, regulatory-reporting, incident-response, data-breach]
level: advanced
status: draft
description: "Meet regulatory and breach-notification duties after ransomware: when encryption or exfiltration is a reportable breach, GDPR, NIS2, HIPAA, SEC and other clocks, and evidence."
sources:
  - https://gdpr-info.eu/art-33-gdpr/
  - https://www.hhs.gov/sites/default/files/RansomwareFactSheet.pdf
  - https://www.sec.gov/newsroom/press-releases/2023-139
  - https://eur-lex.europa.eu/eli/dir/2022/2555/oj
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regulatory and breach notification after ransomware

**Goal:** every mandatory notification is made on time, consistently, with legal leading, while recovery proceeds.

## Is it a breach?
- Encryption alone is a loss of **availability**, which is a personal data breach under GDPR.
- US HIPAA: HHS treats ransomware encryption of ePHI as a presumed breach unless a documented risk assessment shows a low probability of compromise.
- Exfiltration (double extortion) makes confidentiality breach almost certain; establish what data left from logs, EDR and the leak site.

## Common clocks (check current law and contracts)
| Regime | Who | Deadline |
|---|---|---|
| GDPR / UK GDPR Art. 33 | supervisory authority | 72 h from awareness (phased reporting allowed) |
| GDPR Art. 34 | data subjects | without undue delay if high risk |
| NIS2 (EU essential/important entities) | CSIRT/authority | early warning 24 h, notification 72 h, final report 1 month |
| HIPAA | individuals, HHS, sometimes media | within 60 days of discovery |
| SEC Form 8-K Item 1.05 (US listed) | investors | 4 business days after determining materiality |
| US state breach laws | residents, AGs | varies (often 30-60 days) |
| Contracts / DPAs | customers, controllers | often 24-72 h |
Sector regulators (financial, energy, telecom), cyber insurers and law enforcement have their own channels.

## How to run it
1. Legal counsel leads; IR work under privilege where possible.
2. Keep a timeline: awareness time, scope findings, decisions, notifications sent.
3. Notify early with what you know and update; regulators prefer phased reports to late complete ones.
4. Coordinate wording with crisis comms so public statements match regulatory filings.
5. Preserve evidence (images, logs) before rebuilds destroy it.

## Gotchas
- Recovery teams wiping systems before forensics leaves you unable to say what data was taken.
- "Awareness" starts when you have reasonable certainty, not when investigation ends.

## Verify
Post-incident review lists every applicable regime, the deadline, and the timestamp each notification was sent.
