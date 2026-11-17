---
id: computing-software.cybersecurity-defensive.threat-intelligence.tram-mapping-threat-reports-to-attack
name: tram-mapping-threat-reports-to-attack
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [tram, attack-mapping, mitre-attack, threat-report-mapping, cti]
level: practitioner
status: draft
description: "Use MITRE CTID TRAM to speed mapping threat report text to ATT&CK techniques, with analyst review and export into Navigator layers."
sources: ["https://github.com/center-for-threat-informed-defense/tram", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TRAM: report-to-ATT&CK mapping

**Goal:** turn prose threat reports into reviewed technique mappings faster than by hand.

## What it is
TRAM (Threat Report ATT&CK Mapper) is an open-source tool from MITRE's Center for Threat-Informed Defense. It uses a machine-learning text classifier to suggest ATT&CK techniques for sentences of an ingested report, which an analyst accepts or corrects. It runs as a web app you host yourself.

## Workflow
1. Deploy from the project repository (container or from source) following its README; keep it on an internal host.
2. Upload or paste the report (supported formats per the version you run).
3. Review sentence by sentence: accept, reject, or re-map each suggestion; add missing techniques the model missed.
4. Export the approved mappings (check the supported export formats, for example layer/JSON) and load into ATT&CK Navigator or your TIP.
5. Record the source report, analyst and ATT&CK version used.

## Quality rules
- Treat model output as suggestions: expect false positives and misses, especially for techniques described indirectly or behind tool names.
- Map observed behaviour, not marketing claims; use sub-techniques when evidence supports them.
- Keep a second reviewer for reports that drive detection engineering.
- Retrain/finetune only with reviewed data, tracked by version.

## Verify
Pick a report you mapped by hand; compare techniques per sentence and measure agreement before relying on the tool.

Unconfirmed: current supported formats and model version; check the repository release notes.
