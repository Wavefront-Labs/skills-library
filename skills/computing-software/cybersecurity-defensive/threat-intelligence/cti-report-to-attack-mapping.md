---
id: computing-software.cybersecurity-defensive.threat-intelligence.cti-report-to-attack-mapping
name: cti-report-to-attack-mapping
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [mitre-attack, cti-report-mapping, ttp-extraction, attack-techniques, procedure-examples]
level: advanced
status: docs-checked
description: "Map CTI reports to MITRE ATT&CK techniques: extract procedures, choose technique and sub-technique with evidence, record confidence, and avoid common mis-mappings."
sources: ["https://www.cisa.gov/news-events/news/best-practices-mitre-attckr-mapping", "https://attack.mitre.org/software/S0154/", "https://attack.mitre.org/techniques/T1218/011/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping CTI reports to ATT&CK

**Goal:** turn a narrative threat report into a defensible list of techniques with the procedure text that justifies each.
CISA and MITRE publish a full guide, "Best Practices for MITRE ATT&CK Mapping" (linked from the source page); follow it where this summary differs.

## Procedure (analyst practice)
1. **Read the whole report** first; note the adversary, timeframe, victims, and whether the source observed activity directly.
2. **Find behaviours**, not tools: "used rundll32 to execute a DLL export from a ZIP in %TEMP%" is a behaviour; "used Cobalt Strike" is a software reference (ATT&CK Software entry S0154, Cobalt Strike), so map only techniques actually described.
3. **Identify the tactic** (the adversary's goal at that step).
4. **Pick technique and sub-technique**: search ATT&CK for the behaviour; prefer the most specific sub-technique the evidence supports (T1218.011 Rundll32, a sub-technique of T1218, rather than T1218).
5. **Record**: technique id, tactic, verbatim procedure excerpt, source page/paragraph, confidence (high when explicitly described, low when inferred).
6. **Peer review** a sample; mapping is subjective, and two analysts disagreeing is normal - resolve with the evidence.

## Output
A table or STIX relationships in your threat intelligence platform; a Navigator layer for the report/actor, scored by frequency across reports.

## Common mistakes
- Mapping capabilities a tool has rather than what was used.
- Over-mapping generic statements ("the actor exfiltrated data") to a specific sub-technique without detail.
- Using deprecated/revoked technique ids - note the ATT&CK version used.
- Assuming one behaviour serves several tactics; map extra tactics only if the report supports them.

## Verify
- [ ] Every mapped technique has a supporting excerpt.
- [ ] ATT&CK version recorded; layer file stored with the report.

## Checked
2026-11-01. Confirmed on attack.mitre.org: S0154 is Cobalt Strike (software entry); T1218.011 Rundll32 is a sub-technique of T1218. The CISA page confirms the existence of the CISA/MITRE mapping guide (January 2023 update) but not its step-by-step text, so the procedure is labelled analyst practice, not quoted guidance. Removed: scheduled-task example, MISP/OpenCTI and TRAM named tooling.
Method: documentation only; no commands were run.
