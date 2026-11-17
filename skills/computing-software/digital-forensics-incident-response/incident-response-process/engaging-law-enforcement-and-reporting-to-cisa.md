---
id: computing-software.digital-forensics-incident-response.incident-response-process.engaging-law-enforcement-and-reporting-to-cisa
name: engaging-law-enforcement-and-reporting-to-cisa
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [law-enforcement-engagement, cisa-reporting, fbi, ic3, circia, regulatory-reporting, dfir]
level: practitioner
status: draft
description: "Engage law enforcement and report incidents to CISA, FBI or national CERTs: when and how, what to share, CIRCIA, and keeping control of your investigation."
sources: ["https://www.cisa.gov/report", "https://www.fbi.gov/investigate/cyber", "https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/cyber-incident-reporting-critical-infrastructure-act-2022-circia"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Engaging law enforcement and reporting to CISA

**Goal:** get the benefits of government help (decryptors, intelligence, fund freezing,
prosecution) without losing control of the response or creating legal exposure.

## Who (US; equivalents elsewhere)
- **FBI** field office cyber squad (relationship ideally built before an incident) and IC3
  for fraud; **US Secret Service** for financial crimes; **CISA** (report.cisa.gov) for
  technical assistance and sector awareness.
- **CIRCIA** (Cyber Incident Reporting for Critical Infrastructure Act): covered entities
  report substantial incidents to CISA within 72 h and ransom payments within 24 h once
  the final rule is in force; check current applicability.
- UK: Action Fraud and NCSC; EU: national CSIRTs under NIS2 (24 h early warning); Australia:
  ASD ReportCyber.

## When
- Ransomware and extortion (OFAC sanctions screening of payments needs it), BEC fraud,
  nation-state indicators, threats to life or critical infrastructure, insider crimes
  counsel wants to refer.
- Decision owned by legal per RACI; document it either way.

## What to share
IOCs, ransom note, attacker communications, wallet addresses, timeline summary. Agree in
advance what is shared and through counsel; you are not obliged to hand over full images
voluntarily. Ask for their IOCs and whether a decryptor or key exists.

## Expectations
- Law enforcement does not run your remediation and rarely asks you to leave the attacker in
  place; if they ask, decide with counsel and execs.
- Reporting to CISA/FBI is generally voluntary information sharing, with protections under
  CISA 2015 for cyber threat indicators shared appropriately.
- Preserve evidence in a way that could support prosecution (chain of custody).

## Verify
Record in the case: date/time of each report, reference numbers, contacts, what was shared
and who approved it.
