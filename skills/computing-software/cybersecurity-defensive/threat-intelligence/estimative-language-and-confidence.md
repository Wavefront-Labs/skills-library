---
id: computing-software.cybersecurity-defensive.threat-intelligence.estimative-language-and-confidence
name: estimative-language-and-confidence
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [adversary-profiling, estimative-language, confidence-levels, icd-203, probability-yardstick, analytic-standards]
level: practitioner
status: draft
description: "Write intelligence judgments with calibrated estimative language and separate confidence levels, using ICD 203 or the UK probability yardstick consistently across products."
sources: ["ODNI Intelligence Community Directive 203 - Analytic Standards", "UK Defence Intelligence / PHIA Professional Head of Intelligence Assessment probability yardstick", "Sherman Kent - Words of Estimative Probability"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Estimative language and confidence

**Goal:** readers understand how likely you think something is and how solid your basis is, the same way every time.

## Likelihood terms (ICD 203)
| Term | Probability |
|---|---|
| almost no chance / remote | 1-5% |
| very unlikely / highly improbable | 5-20% |
| unlikely / improbable | 20-45% |
| roughly even chance | 45-55% |
| likely / probable | 55-80% |
| very likely / highly probable | 80-95% |
| almost certain / nearly certain | 95-99% |
The UK yardstick uses similar bands (remote, highly unlikely, unlikely, realistic possibility, likely, highly likely, almost certain) with deliberate gaps between them. Pick one scale organisation-wide and publish it in every product's footer.

## Confidence levels (separate from likelihood)
- **High** - judgment based on high-quality information from multiple sources, or the nature of the issue makes a solid judgment possible.
- **Moderate** - credible and plausible information but not corroborated enough for high confidence.
- **Low** - information is scant, questionable, fragmented, or from sources of uncertain reliability.
Example: "We assess with moderate confidence that the actor will likely (55-80%) exploit the new VPN vulnerability against our sector within 30 days."

## Rules
- Do not combine terms from different scales or invent new ones ("probably possible").
- State the basis: what evidence, what sources, key assumptions, and what would change the judgment.
- Avoid "may/could/might" for judgments - they carry no probability.
- Distinguish facts ("the domain was registered on 3 May") from assessments ("we assess...").

## Verify
- [ ] Each key judgment uses a term from the published scale and states a confidence level.
- [ ] Peer review checks wording before dissemination.
