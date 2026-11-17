---
id: computing-software.cybersecurity-defensive.threat-modelling.owasp-risk-rating
name: owasp-risk-rating
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [attack-trees, owasp-risk-rating, risk-scoring, likelihood-impact, threat-prioritisation, threat-modelling]
level: practitioner
status: docs-checked
description: "Rate threats and findings with the OWASP Risk Rating Methodology: threat agent and vulnerability factors for likelihood, technical and business impact, and calibration."
sources: ["https://owasp.org/www-community/OWASP_Risk_Rating_Methodology", "https://www.first.org/cvss/", "https://csrc.nist.gov/pubs/sp/800/30/r1/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OWASP risk rating methodology

**Goal:** consistent, explainable ratings for threats from threat models and for findings
from tests, combining likelihood and impact in a way the business understands.

## Likelihood factors (each 0-9)
**Threat agent:** skill level, motive, opportunity (access/resources needed), size (how many
potential attackers: developers, authenticated users, anonymous internet).
**Vulnerability:** ease of discovery, ease of exploit, awareness (how well known), intrusion
detection (how likely detection is: active detection is low score, not logged is high).
Likelihood = average of the 8 factors.

## Impact factors (each 0-9)
**Technical:** loss of confidentiality, integrity, availability, accountability (traceability).
**Business:** financial damage, reputation damage, non-compliance, privacy violation (how
many records).
Use business impact when you have reliable business information; otherwise technical.

## Combine
Map each average to a level: 0 to <3 LOW, 3 to <6 MEDIUM, 6-9 HIGH. Then:
| Impact \ Likelihood | Low | Medium | High |
|---|---|---|---|
| High | Medium | High | Critical |
| Medium | Low | Medium | High |
| Low | Note | Low | Medium |

## Worked example
IDOR on `/api/invoices/{id}` exposing other customers' invoices:
- Likelihood: skill 5 (some technical), motive 4, opportunity 7 (any registered user), size 6,
  discovery 7, exploit 8, awareness 6, detection 8 (no alerting) = avg 6.4 HIGH.
- Impact (business): financial 5, reputation 7, non-compliance 7, privacy 7 = 6.5 HIGH.
- Overall: **Critical**.

## Make it consistent
- Customise factor descriptions to your organisation (what financial damage "7" means in dollars).
- Calibrate as a group on a few reference findings; record factor scores with each rating so
  disagreements are about specific factors.
- CVSS rates technical severity of a vulnerability in general; OWASP rating adds your context.
  Use CVSS for vendor CVEs, OWASP for application threats and pen test findings in your apps.

## Gotchas
- Averages hide a single extreme factor; allow overriding with a written rationale.
- Inflated ratings for everything erode trust; calibration sessions fix this.
- Rating without mitigations considered vs after mitigations: state which.

## Verify
Two reviewers independently rate five threats; results agree within one level, and
disagreements trace to specific documented factors.

## Checked
2026-10-28. Confirmed on the OWASP Risk Rating Methodology page: factors scored 0 to 9, the eight likelihood factors and their averaging, technical and business impact factors, level bands (0 to <3 LOW, 3 to <6 MEDIUM, 6 to 9 HIGH), the severity matrix including Note, preferring business impact when known, optional weighting and calibration. The worked example is illustrative, with scores chosen by this skill.
Method: documentation only; no commands were run.
