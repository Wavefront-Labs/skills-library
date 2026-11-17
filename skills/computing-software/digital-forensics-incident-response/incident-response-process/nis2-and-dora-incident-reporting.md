---
id: computing-software.digital-forensics-incident-response.incident-response-process.nis2-and-dora-incident-reporting
name: nis2-and-dora-incident-reporting
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [nis2, dora, breach-notification, regulatory-reporting, dfir]
level: advanced
status: draft
description: "Meet EU NIS2 and DORA incident reporting: significant/major incident tests, 24h early warning, 72h notification, intermediate and final reports."
sources: ["https://eur-lex.europa.eu/eli/dir/2022/2555/oj", "https://eur-lex.europa.eu/eli/reg/2022/2554/oj"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NIS2 and DORA incident reporting

**Goal:** EU essential/important entities (NIS2) and financial entities (DORA) have short,
staged reporting clocks. Responders must feed the reporting team facts on time.

## NIS2 (Directive (EU) 2022/2555, Art. 23)
- Applies to "significant incidents": severe operational disruption or financial loss, or
  considerable damage to others. Member-state transposition and implementing acts define thresholds.
- To the national CSIRT / competent authority:
  - **Early warning within 24 h** of becoming aware: is it suspected unlawful/malicious? possible cross-border impact?
  - **Incident notification within 72 h**: initial assessment, severity, impact, IOCs where available.
  - **Intermediate reports** on request.
  - **Final report within one month** of the notification: detailed description, root cause/threat
    type, mitigation applied, cross-border impact. Progress report if still ongoing.
- Recipients of services may need to be informed of significant cyber threats and remedies.

## DORA (Regulation (EU) 2022/2554, Art. 17-19 + RTS/ITS)
- Classify ICT-related incidents using criteria (clients affected, duration, geographic spread,
  data losses, criticality of services, economic impact) to decide "major".
- Major incident reports to the competent authority: **initial notification** (within 4 h of
  classification and no later than 24 h of awareness), **intermediate** (within 72 h of the
  initial), **final** (within one month), using the prescribed templates.
- Voluntary notification of significant cyber threats.

## What IR must supply
- Detection time ("aware" time) and classification time - log them in the decision log.
- Services and clients affected, duration, data affected, cross-border elements, IOCs, root cause status.

## Gotchas
- The clock starts at awareness, not at confirmation of root cause; report with what you know and update.
- GDPR Art. 33 (72 h to DPA) runs in parallel if personal data is involved; different recipient.
- National transpositions differ; maintain a per-country table with counsel.

## Verify
Each regulatory deadline is on the incident timeline with owner, submission time and reference number.
