---
id: computing-software.digital-forensics-incident-response.evidence-handling.privacy-constraints-during-evidence-collection
name: privacy-constraints-during-evidence-collection
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [collection-privacy, rfc-3227, data-minimisation, gdpr, privileged-material, dfir]
level: practitioner
status: draft
description: "Respect privacy during evidence collection (RFC 3227 2.3): authorisation, data minimisation, privileged and personal content, cross-border transfers and examiner access limits."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://gdpr-info.eu/art-5-gdpr/", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Privacy constraints during evidence collection

RFC 3227 2.3: respect the privacy rules and guidelines of your company and legal jurisdiction, make sure you have authority to collect, and do not intrude on privacy without strong justification. In practice the risk is collecting more personal data than the investigation needs.

## Before collecting
- **Authority**: written authorisation naming scope (systems, accounts, date range). For employee investigations, Legal and HR sign-off; some jurisdictions require works council or employee notice.
- **Lawful basis and purpose** (GDPR Art. 5/6): security incident handling is usually legitimate interest or legal obligation; document it in the case.
- **Scope**: which custodians and data types are needed to answer the investigative questions. Write them down.

## Minimise
- Prefer targeted logical collection (specific mailboxes, date ranges, artefact sets via KAPE targets) over full images when the questions allow.
- When a full image is needed (reliability, deleted data), collect fully but restrict examination to scope using keyword/date filters and record the filter used.
- Avoid collecting personal devices unless consented or legally compelled.

## Special categories
- **Attorney-client privileged** material: set up a filter team or keyword screen (law-firm domains) before examiners read mail.
- **Health, union, religious data, private messages** stumbled on: stop, note the location, do not review further unless in scope; report to Legal.
- **Third-party data** on shared systems (customers' data on a server): access only what is needed.

## Cross-border
Moving evidence out of the EU/UK/China etc. may be a restricted transfer. Check with privacy counsel before shipping images or uploading to an IR firm's cloud; consider examining in-region.

## Access control
Need-to-know access on evidence storage, examiner activity logging, and retention limits tied to case closure and legal holds.

## Gotchas
- Monitoring an employee's live communications is usually far more restricted than examining stored data.
- Screenshots in reports can leak personal data; redact what is not needed.

## Verify
The case file contains the authorisation, the scope statement, the filters applied, and any privileged or out-of-scope material is logged as not reviewed.
