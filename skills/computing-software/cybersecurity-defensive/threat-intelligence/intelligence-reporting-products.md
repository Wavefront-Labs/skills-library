---
id: computing-software.cybersecurity-defensive.threat-intelligence.intelligence-reporting-products
name: intelligence-reporting-products
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [intelligence-lifecycle, intel-reporting, bluf, threat-assessment, flash-report, dissemination, tlp-marking]
level: practitioner
status: draft
description: "Write CTI products for different audiences: flash alerts, tactical reports, operational briefs and strategic assessments with BLUF, confidence, TLP marking and actionable recommendations."
sources: ["SANS FOR578 Cyber Threat Intelligence - Dissemination", "ODNI Intelligence Community Directive 203 Analytic Standards", "FIRST Traffic Light Protocol 2.0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intelligence reporting products

**Goal:** each product answers a requirement for a specific audience, fast to read, with clear confidence and actions.

## Product types
| Product | Audience | Content | Timing |
|---|---|---|---|
| Flash alert | SOC, IR, IT ops | What, are we affected, actions now, IOCs/detections | hours |
| Tactical report | SOC/detection engineers | TTPs, ATT&CK mapping, detection queries, IOCs with context | days |
| Operational brief | security leadership, IR | campaign/actor activity relevant to us, likely next moves | weekly |
| Strategic assessment | executives, board, risk | trends, likely threats over 6-24 months, business impact, investment implications | quarterly / on demand |

## Structure
1. **Title** stating the judgment ("Ransomware group X likely to target our sector's VPN appliances in Q3").
2. **BLUF** - two or three sentences: judgment, confidence, so-what.
3. Key judgments with estimative language and confidence levels (ICD 203).
4. Evidence/analysis, separating facts from assessments; source reliability where relevant.
5. **Impact to us** - exposed assets, controls in place.
6. **Recommendations** - specific owners and actions.
7. Appendices: IOCs (machine-readable separately), ATT&CK layer, references.
8. Marking: TLP label at top, handling caveats, date, author, requirement id (PIR) answered.

## Style
Short sentences, active voice, no jargon for strategic readers; define acronyms; one idea per paragraph; charts only where they clarify.

## Feedback
Include a feedback link/question; track readership and actions taken; use it in PIR reviews.

## Gotchas
- Dumping IOC lists without context or relevance assessment.
- Vendor-style hype; overstating confidence.
- Missing "are we affected?" - the first question readers ask.

## Verify
- [ ] Every product references the PIR it answers and has a TLP marking.
- [ ] Recommendations have owners; follow-up tracked.
