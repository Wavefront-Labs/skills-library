---
id: computing-software.digital-forensics-incident-response.log-analysis.attack-navigator-coverage-mapping
name: attack-navigator-coverage-mapping
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [attack-navigator, mitre-attack, detection-coverage, gap-analysis, detection-engineering, dfir]
level: practitioner
status: draft
description: "Map detection coverage in MITRE ATT&CK Navigator: building layers from rule metadata, scoring and colouring, comparing against incident or threat-actor TTPs, and avoiding coverage theatre."
sources: ["https://mitre-attack.github.io/attack-navigator/", "https://github.com/mitre-attack/attack-navigator", "https://github.com/rabobank-cdc/DeTTECT"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ATT&CK Navigator coverage mapping

Navigator visualises ATT&CK matrices as layers: JSON files that score and annotate techniques. Used well, it shows where detections exist relative to the TTPs that matter; used badly it paints the matrix green without testing anything.

## Build a coverage layer from rule metadata
Extract technique IDs from your detection repo (Sigma `tags: attack.t1003.001`, Sentinel `relevantTechniques`, Elastic `threat` blocks) and emit a layer:
```json
{
  "name": "Detection coverage 2026-10",
  "versions": {"attack": "16", "navigator": "5.1", "layer": "4.5"},
  "domain": "enterprise-attack",
  "techniques": [
    {"techniqueID": "T1003.001", "score": 3, "comment": "3 rules, validated 2026-09", "metadata": [{"name":"rules","value":"lsass_access_unusual; procdump_lsass; comsvcs_minidump"}]}
  ],
  "gradient": {"colors": ["#ffffff", "#66b1ff"], "minValue": 0, "maxValue": 5}
}
```
Score by validated quality, not rule count: e.g. 0 none, 1 rule exists untested, 2 tested in lab, 3 tested in production with acceptable FP rate.

## Compare against what matters
- **Incident layer**: TTPs observed in your incident (from the timeline). Overlay with coverage (Layer > create from other layers with expression, e.g. `a - b` or combine scores) to show which incident steps had no detection.
- **Threat-actor layers**: ATT&CK group pages offer Navigator layers; combine actors relevant to your sector to prioritise.
- **Data-source layer**: which techniques your logs could even see (DeTT&CT helps score visibility separately from detection).

## Practice
1. Version layers with the date and ATT&CK version; regenerate from code, do not hand-edit.
2. Export SVG/Excel for reports; keep the JSON for reproducibility.
3. Pair every "covered" technique with a validation (Atomic test) record.
4. Review after ATT&CK releases (technique changes, sub-technique splits).

## Gotchas
- Technique-level coverage hides procedure-level gaps: one rule for T1059.001 does not detect every PowerShell abuse.
- Mixing enterprise, mobile and ICS domains in one layer is not supported; separate layers.
- Coverage maps for executives must explain scores; green does not mean "safe".

## Verify
Every technique scored 2 or more has a linked validation result, and the incident-gap layer's uncovered techniques have backlog items.
