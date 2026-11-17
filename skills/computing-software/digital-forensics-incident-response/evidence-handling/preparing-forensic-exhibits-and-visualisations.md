---
id: computing-software.digital-forensics-incident-response.evidence-handling.preparing-forensic-exhibits-and-visualisations
name: preparing-forensic-exhibits-and-visualisations
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [forensic-exhibits, visualisation, timeline-chart, forensic-reporting, dfir]
level: practitioner
status: draft
description: "Prepare exhibits and visualisations for forensic reports and court: traceable screenshots, timeline graphics, attack-path diagrams, tables, labelling and avoiding misleading charts."
sources: ["https://www.swgde.org/documents/published-complete-listing", "https://csrc.nist.gov/pubs/sp/800/86/final", "https://www.law.cornell.edu/rules/fre/rule_1006"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Preparing forensic exhibits and visualisations

Exhibits are how non-technical readers (executives, judges, juries) understand findings. Every exhibit must be traceable to evidence and must not overstate it. In US courts, summary charts of voluminous records are allowed under FRE 1006 if the underlying data is available to the other side.

## Types and rules
| Exhibit | How to make it defensible |
|---|---|
| Screenshot of an artefact | Show the tool, version, evidence item, path and the full record row; caption with exhibit ID and source; never crop out timestamps or time zone |
| Timeline graphic | One time zone stated in the title (UTC), each event numbered and keyed to a table with evidence references |
| Attack-path / network diagram | Hosts labelled as in evidence; solid lines for proven connections, dashed for inferred; legend explains |
| Tables (files exfiltrated, logons) | Exported from the tool, not retyped; include query used and row count |
| Charts (volume over time) | Axis starts at zero for bars, bin size stated, no 3D or dual-axis tricks |

## Procedure
1. Decide the questions each exhibit answers; one point per exhibit.
2. Generate from working copies; record how each exhibit was produced (tool, query, settings) in the notes so it can be reproduced.
3. Number exhibits consistently (`Exhibit 7` / `Figure 3.2`), and reference them in the report text.
4. Redact personal or privileged data not needed for the point; log redactions.
5. Have a peer check each exhibit against the evidence before release.
6. For court, provide native data underlying summaries and be ready to explain every mark on a diagram.

## Gotchas
- Colour alone to convey meaning fails in greyscale prints and for colour-blind readers; add labels or patterns.
- Rounded or local times in a chart that disagree with UTC times in the text undermine credibility.
- Inferences drawn as facts (a solid arrow for an assumed lateral movement) are the first thing opposing experts attack.

## Verify
For any exhibit, a reviewer can follow its reference to the evidence item and reproduce it using the recorded method.
