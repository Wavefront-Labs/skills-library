---
id: engineering-technology.biomedical-engineering.biomechanics.fea-credibility-asme-vv40
name: fea-credibility-asme-vv40
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [fea-credibility, asme-v-and-v-40, model-credibility, verification-validation, context-of-use]
level: advanced
status: gated
description: "Plan model credibility for medical device FEA using the ASME V and V 40 risk-informed framework: question of interest, context of use, model risk, credibility goals and evidence."
sources: ["ASME V&V 40-2018 Assessing Credibility of Computational Modeling through Verification and Validation: Application to Medical Devices (confirm edition)", "FDA, Assessing the Credibility of Computational Modeling and Simulation in Medical Device Submissions, final guidance November 2023 (https://www.fda.gov/regulatory-information/search-fda-guidance-documents/assessing-credibility-computational-modeling-and-simulation-medical-device-submissions)", "https://www.asme.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Model credibility with ASME V and V 40

**Goal:** show that a model is credible enough for its decision, in proportion to the risk of a wrong answer.

## Framework steps
1. **Question of interest:** the decision the model informs (for example fatigue life of a stent).
2. **Context of use (COU):** the specific role of the model (replaces a bench test, supplements it) and the conditions it covers.
3. **Model risk:** the combination of model influence (how much the decision relies on the model versus other evidence) and decision consequence (patient harm if wrong).
4. **Credibility goals:** higher risk needs more rigorous evidence in each credibility factor.
5. **Credibility factors** (as defined in ASME V&V 40 (gated: unconfirmed, source is paywalled or blocked)): code verification, calculation verification (mesh and step convergence), model form and inputs, test samples and conditions for validation, comparator quality, agreement and applicability of validation to the COU, and uncertainty quantification.
6. **Evidence and assessment:** perform and document verification, validation and uncertainty analysis; compare with goals; state residual gaps and whether the COU needs to be narrowed.

## Practice
- Plan before building the model; define validation experiments to be sensitive to the quantities of interest.
- Keep traceable records (inputs, versions, mesh studies) for regulatory review.
- The framework is guidance; regulators describe expectations in their own documents. FDA's final guidance "Assessing the Credibility of Computational Modeling and Simulation in Medical Device Submissions" (November 2023) is the US reference; confirm current text.

## Verify
- [ ] COU and model risk written down and agreed.
- [ ] Validation comparator matches the COU, with uncertainties.
- [ ] Mesh convergence and input sensitivity documented.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
