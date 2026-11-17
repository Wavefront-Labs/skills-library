---
id: religion-philosophy.applied-ethics-and-bioethics.technology-and-ai-ethics.running-an-ai-ethics-impact-assessment
name: running-an-ai-ethics-impact-assessment
category: religion-philosophy
field: applied-ethics-and-bioethics
product: technology-and-ai-ethics
tags: [applied-ethics-and-bioethics, technology-and-ai-ethics, ai-ethics, data-ethics, responsible-ai, algorithmic-impact-assessment, aia, ethics-review, algorithmic-fairness, bias-audit, demographic-parity, equalized-odds, calibration, four-fifths-rule, disparate-impact, nist-ai-rmf, eu-ai-act, oecd-ai-principles, unesco-ai-ethics, iso-42001, model-cards, datasheets-for-datasets, human-oversight, explainability, red-teaming, dpia]
level: practitioner
status: draft
description: "Run an AI/data ethics impact assessment: map the system and affected people, tier the risk, choose fairness metrics, probe harms, set mitigations and sign-off with model cards and monitoring."
sources:
  - "NIST — AI Risk Management Framework (AI RMF 1.0)"
  - "EU Artificial Intelligence Act (Regulation (EU) 2024/1689)"
  - "OECD — Recommendation of the Council on Artificial Intelligence"
  - "UNESCO — Recommendation on the Ethics of Artificial Intelligence"
  - "Mitchell et al. — Model Cards for Model Reporting"
  - "Gebru et al. — Datasheets for Datasets"
  - "Government of Canada — Algorithmic Impact Assessment tool"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running an AI ethics impact assessment — from use case to sign-off

**Goal:** before an AI or data-driven system ships (or when it changes materially),
produce a short, evidence-based assessment of who it could harm and how, what was
done about it, and who accepted the remaining risk — in a form engineers can act on.

This is an ethics process, not a compliance certificate. Where the EU AI Act,
GDPR (DPIA), sector rules or anti-discrimination law apply, run those alongside
and involve counsel (jurisdiction-dependent).

## 1. Describe the system (one page)
- **Purpose and decision:** what does the output change for a person? (Ranks a CV,
  flags a transaction, drafts a reply, sets a price.)
- **Users vs affected people** — often different. Who never sees the system but bears its decisions?
- **Data:** sources, consent/legal basis, sensitive attributes, known gaps (datasheet).
- **Model:** type, vendor/foundation model, training data provenance (model card).
- **Human role:** fully automated, human-in-the-loop, or human-on-the-loop?
- **Deployment context:** scale, reversibility of a wrong decision, appeal route.

## 2. Tier the risk
| Tier | Signals | Depth of review |
|---|---|---|
| Low | Internal convenience, easy to override, no individual impact | Checklist + owner sign-off |
| Elevated | Affects individuals' access, price, content they see | Full assessment, fairness tests |
| High | Employment, credit, housing, education, health, policing, migration, essential services; or vulnerable users | Full assessment + external/independent review, ongoing monitoring |
| Prohibited/redline | e.g. practices banned under EU AI Act Art. 5 (social scoring, certain manipulation) or your own policy | Stop |
Map tiers to the regulation that applies to you; the EU AI Act's high-risk list is in Annex III.

## 3. Identify harms — structured brainstorm with the team
Walk each category and record likelihood × severity × who:
- **Allocative** (unfair denial of opportunities/resources)
- **Quality-of-service** (works worse for some groups — accents, skin tones, languages)
- **Representational** (stereotyping, demeaning outputs, erasure)
- **Privacy** (re-identification, inference of sensitive traits, surveillance)
- **Autonomy/manipulation** (dark patterns, undisclosed persuasion)
- **Safety and misuse** (dangerous instructions, dual use; red-team for generative systems)
- **Labour and environmental** (displacement, data-labeller conditions, compute footprint)
Include affected people or their advocates where feasible — not just the build team.

## 4. Choose and run fairness tests
Pick metrics that match the harm, and write down why:
- **Demographic parity** — equal selection rates; screen with the US **four-fifths rule**
  (a group's selection rate below 80% of the highest group's is a red flag, not proof).
- **Equalized odds / equal opportunity** — equal error rates (false negatives where denial harms).
- **Calibration / predictive parity** — a score means the same thing across groups.
These generally **cannot all hold at once** when base rates differ (Kleinberg et al.;
Chouldechova) — choosing is an ethical decision; record it. Report confidence intervals;
small subgroups make metrics noisy.

## 5. Mitigate and decide
For each significant harm: mitigation (data fix, threshold change, human review, scope
restriction, user disclosure, appeal route, kill switch), owner, due date, and
**residual risk**. A named accountable executive signs off on residual risk —
or the answer is "don't deploy this way."

## 6. Monitor
Set triggers for re-assessment: model or data change, new population, drift in subgroup
metrics, incidents/complaints. Schedule periodic review (e.g. quarterly for high tier —
a common practice, not a rule).

## Gotchas
- "We don't collect race, so we can't be biased" — proxies (postcode, name) carry it;
  you may need protected attributes (lawfully) to test.
- Human-in-the-loop that rubber-stamps (automation bias) is not oversight; measure override rates.
- Vendor models: demand documentation; "proprietary" is not an answer for a high-tier use.
- Ethics review timed after launch is a post-mortem. Start at design.
- Principle lists (fairness, transparency, accountability) are not an assessment; evidence is.

## Verify
- [ ] Affected people, not just users, are identified.
- [ ] Risk tier assigned with stated reasons and applicable law listed.
- [ ] Each harm category considered and recorded, even if "not applicable".
- [ ] Fairness metric choice justified; subgroup results with intervals attached.
- [ ] Mitigations have owners; residual risk signed off by a named person.
- [ ] Monitoring triggers and next review date set.
