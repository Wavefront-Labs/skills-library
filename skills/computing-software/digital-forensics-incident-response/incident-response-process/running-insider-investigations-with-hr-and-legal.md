---
id: computing-software.digital-forensics-incident-response.incident-response-process.running-insider-investigations-with-hr-and-legal
name: running-insider-investigations-with-hr-and-legal
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [hr-investigation, insider-threat, legal-hold, employee-investigation, privacy, dfir]
level: practitioner
status: draft
description: "Run an insider threat investigation jointly with HR and legal: authorisation, privacy limits, covert collection, interviews, evidence standards and outcomes."
sources: ["https://insights.sei.cmu.edu/library/common-sense-guide-to-mitigating-insider-threats-seventh-edition/", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running insider investigations with HR and legal

**Goal:** investigate an employee lawfully and fairly, with evidence that supports
disciplinary action, litigation or a criminal referral (CERT Common Sense Guide to
Mitigating Insider Threats).

## Before collecting anything
- **Written authorisation** from legal/HR naming the subject, allegation, scope and
  permitted data sources.
- Check the acceptable use policy and employment contracts: monitoring consent, BYOD terms.
- Privacy law: GDPR requires proportionality and often a DPIA; works councils in some EU
  countries must be consulted; US states vary on monitoring notices.
- Need-to-know: restrict the case to named people; do not use standard SOC queues.

## Covert collection
- Collect quietly: remote triage via EDR or Velociraptor rather than seizing the laptop
  while the subject is present; mailbox and OneDrive holds/exports via Purview.
- Preserve before confronting: legal hold on mailbox, OneDrive, Teams; image the device when
  it can be taken without alerting (or at the interview).
- Do not access personal accounts or personal devices without legal authority.

## Evidence standard
Same as any forensic case: chain of custody, hashes, contemporaneous notes. Findings must be
factual and neutral; avoid conclusions about intent (that is for HR/legal).

## Interview
HR leads, investigator supports with facts; never reveal all evidence at once; record or
take verbatim notes; offer the subject a chance to explain.

## Outcomes
Disciplinary action, recovery of data (signed attestation of deletion, device inspection),
civil action (injunction for trade secrets), criminal referral via counsel.

## Gotchas
- Investigating outside authorised scope can make evidence inadmissible and expose the
  company to claims.
- Departing employees: preserve their device before re-imaging; the IT offboarding process
  often wipes key evidence.

## Verify
Every collection step maps to the written authorisation, and the report states facts with
sources and no speculation about motive.
