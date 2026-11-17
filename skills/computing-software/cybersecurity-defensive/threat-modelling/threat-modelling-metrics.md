---
id: computing-software.cybersecurity-defensive.threat-modelling.threat-modelling-metrics
name: threat-modelling-metrics
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling-metrics, security-metrics, samm, threat-modelling-programme, kpi]
level: practitioner
status: draft
description: "Measure a threat modelling programme: coverage of critical apps, model freshness, mitigation closure, design flaws found early, and SAMM threat assessment maturity."
sources: ["https://owaspsamm.org/model/design/threat-assessment/", "https://www.threatmodelingmanifesto.org/", "https://www.bsimm.com/framework/intelligence/attack-models.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat modelling programme metrics

Measure outcomes (did designs get safer?) not activity (how many diagrams). Keep the set small and pull it from
systems of record (app inventory, tracker, model repository) so it is not hand-maintained.

## Core metrics
| Metric | Definition | Why |
|---|---|---|
| Coverage | % of tier-1 (critical) applications with a threat model | Are the right systems modelled? |
| Freshness | % of models reviewed within policy (e.g. 12 months or since last major change) | Stale models mislead |
| Trigger compliance | % of significant design changes (new external interface, new data class) with a model update before release | Process actually used |
| Mitigation closure | Open threat mitigations by severity and age; % closed within SLA | Models drive change |
| Early findings | Count/share of findings first found in design vs later in pentest or production for the same class | Shift-left evidence |
| Escaped design flaws | Incidents or pentest findings that a model should have caught | Quality of modelling |
| Risk acceptance hygiene | % of acceptances with owner and unexpired date | Governance |

## Maturity view
OWASP SAMM Design > Threat Assessment practice:
- Stream A (application risk profile): level 1 basic risk classification of apps; level 2 central inventory
  with risk ratings; level 3 periodic review.
- Stream B (threat modelling): level 1 best-effort ad hoc modelling of high-risk apps; level 2 standardised
  method, training and templates across teams; level 3 continuous improvement and automation.
Score annually; use gaps to plan the programme.

## Collecting the data
- App inventory field "threat model link + last reviewed date".
- Label all threat-derived tickets (`threat-model`) to compute closure and age.
- Tag pentest and incident findings with "should a model have caught this? y/n" during retros.

## Gotchas
- Counting threats found rewards long, generic lists; do not target it.
- Coverage without freshness is vanity; report them together.
- Small teams: two metrics (coverage of critical apps, mitigation closure) are enough.

## Verify
Metrics regenerate from source systems without manual edits, and the last quarter's report led to at least one
programme decision (training, template change, tooling).
