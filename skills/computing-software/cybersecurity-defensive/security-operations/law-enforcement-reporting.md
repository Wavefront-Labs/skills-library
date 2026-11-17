---
id: computing-software.cybersecurity-defensive.security-operations.law-enforcement-reporting
name: law-enforcement-reporting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [law-enforcement-reporting, incident-reporting, fbi-ic3, cisa, ncsc, bec, cybercrime-reporting]
level: practitioner
status: draft
description: "Report cyber incidents to law enforcement (FBI IC3, CISA, NCSC/Action Fraud, national police): when and what to report, evidence to provide, BEC wire recall and coordination."
sources: ["https://www.ic3.gov/", "https://www.cisa.gov/report", "https://www.ncsc.gov.uk/section/respond-recover/incident-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Law enforcement reporting

## Why
Recovery of funds (BEC), access to decryptors/intel, disruption of actors, and sometimes legal or
contractual expectations. Reporting is usually not mandatory for private firms except specific
sectors/regimes (e.g. CIRCIA in the US for covered entities, NIS2 CSIRT reporting in the EU).

## Where
- **US**: FBI IC3 (ic3.gov) and the local FBI field office cyber squad; CISA (report.cisa.gov) for
  incident reporting and assistance; Secret Service for financial crimes.
- **UK**: NCSC (significant incidents) and Action Fraud / Report Fraud (cyber crime), regional
  police cyber units.
- **EU**: national CSIRT/CERT and police cybercrime units; Europol via national police.
Establish contacts with the local field office before an incident.

## BEC / fraudulent wire
Speed matters: contact your bank immediately to request a recall, file IC3 within 72 hours
(FBI Recovery Asset Team can freeze funds domestically), include transaction details (amount,
date, beneficiary bank, account numbers, SWIFT/IBAN).

## What to provide
Timeline, IOCs (IPs, domains, hashes, wallet addresses, ransom notes, emails with headers), affected
systems, losses, contact details. Agree with counsel what is shared; you control evidence sharing.

## Coordination
- Law enforcement involvement rarely means seizing your systems; they ask for copies of evidence.
- They may request delaying public notification for investigative reasons (some laws allow).
- Ransomware: ask whether decryptors exist (also check nomoreransom.org).

## Gotchas
- Report through counsel when privilege matters; keep a log of what was shared.
- Sanctioned entities: ransom payments may be illegal; law enforcement and counsel advise.

## Verify
Report reference numbers recorded in the incident file, with what was shared, when and by whom.
