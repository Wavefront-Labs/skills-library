---
id: computing-software.digital-forensics-incident-response.incident-response-process.cyber-insurance-claims-during-incidents
name: cyber-insurance-claims-during-incidents
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [cyber-insurance, insurance-claim, breach-coach, panel-vendors, ransomware, dfir]
level: practitioner
status: draft
description: "Handle cyber insurance during an incident: prompt notice, panel vendors and consent, cost tracking, ransomware conditions, and evidence the insurer will ask for."
sources: ["https://www.ncsc.gov.uk/guidance/cyber-insurance-guidance", "https://www.cisa.gov/stopransomware/ransomware-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cyber insurance claims during incidents

**Goal:** keep coverage intact while responding at speed. Most claim disputes come from late
notice, using unapproved vendors, or incurring costs without consent.

## Within hours of declaration
1. **Notify the insurer/broker** through the policy's incident hotline; policies require
   notice "as soon as practicable", sometimes with fixed deadlines. Record the reference.
2. Ask for the **breach coach** (panel counsel) and approved DFIR, negotiation and PR
   vendors. Using panel vendors usually means direct billing and pre-approved rates.
3. Get **written consent** before significant spend (DFIR firm, crisis PR, credit
   monitoring, ransom negotiation/payment).

## Coverage areas to check
First-party: IR/forensics, legal, notification, credit monitoring, data restoration,
business interruption (waiting period, e.g. 8-12 h), extortion. Third-party: liability,
regulatory fines (where insurable), PCI assessments. Exclusions: war/state-backed attack
clauses, failure to maintain stated controls (MFA, backups), prior known incidents.

## Ransomware specifics
Insurers may require OFAC screening by the negotiator, law enforcement notification, and
consent before payment; some policies sub-limit or exclude extortion.

## Documentation to keep
Time sheets and invoices per vendor, business interruption calculations (lost revenue,
extra expense) with finance, evidence that controls declared in the application existed
(e.g. MFA rollout records).

## Gotchas
- Statements in the application (e.g. "MFA on all remote access") that turn out false can
  void cover; involve counsel before answering insurer questionnaires mid-incident.
- Two DFIR firms (yours and the insurer's) without coordination.

## Verify
Claim file contains notice timestamp, consents, invoices mapped to coverage sections, and a
BI calculation signed off by finance.
