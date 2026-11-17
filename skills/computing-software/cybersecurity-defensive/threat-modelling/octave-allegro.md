---
id: computing-software.cybersecurity-defensive.threat-modelling.octave-allegro
name: octave-allegro
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [octave-allegro, octave, information-asset-risk, risk-assessment, sei-cert, threat-modelling]
level: practitioner
status: docs-checked
description: "Run an OCTAVE Allegro assessment: risk measurement criteria, information asset profiles, containers, areas of concern, threat scenarios and relative risk scores."
sources: ["https://insights.sei.cmu.edu/library/introducing-octave-allegro-improving-the-information-security-risk-assessment-process/", "https://resources.sei.cmu.edu/asset_files/TechnicalReport/2007_005_001_14885.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCTAVE Allegro

OCTAVE Allegro (SEI report CMU/SEI-2007-TR-012, 2007) streamlines information security
risk assessment so an organisation gets sufficient results with a small investment of time,
people and other resources. It considers people, technology and facilities in relation to
the information they handle, and centres on information assets and the containers where
they live.

## The eight steps (outputs are captured on worksheets)
1. **Establish risk measurement criteria**: qualitative measures of the effect of a realised
   risk, using standard worksheets for reputation/customer confidence, financial,
   productivity, safety and health, and fines/legal penalties (high, medium and low
   definitions), plus a user-defined area. Then prioritise the impact areas from most to
   least important. Consistent criteria keep mitigation decisions consistent across assets
   and units.
2. **Develop an information asset profile**: describes the asset's features, value and
   boundaries and defines its security requirements (confidentiality, integrity,
   availability, and the most important one). One worksheet per asset.
3. **Identify information asset containers**: everywhere the asset is stored, transported or
   processed, internal or external. Risks to a container are inherited by the asset, so
   include service providers and their subcontractors.
4. **Identify areas of concern**: brainstorm real-world conditions that threaten the asset.
   The aim is to capture quickly what comes to mind, not a complete list.
5. **Identify threat scenarios**: expand each area of concern into a scenario of actor,
   means (access), motive and outcome (disclosure, modification, destruction, loss,
   interruption). Then work through the threat trees (human actors using technical means,
   human actors using physical access, technical problems, other problems) using the report's
   questionnaires. Probability, if used, is expressed qualitatively as high, medium or low.
6. **Identify risks**: capture the consequences of each threat in the impact areas.
7. **Analyse risks**: multiply each impact area's rank by its impact value (high 3, medium 2,
   low 1) and total the results as the relative risk score. Including probability is up to the
   organisation.
8. **Select mitigation approach**: prioritise by relative risk score, group into pools
   (pool 1 mitigate; pool 2 mitigate or defer; pool 3 defer or accept; pool 4 accept), and
   develop mitigation strategies considering the asset's value and security requirements, its
   containers and the operating environment. Approaches are accept, defer, mitigate and
   transfer.

## Tips
- Agreeing the impact-area definitions and ranking in step 1 is what makes later scores
  reflect the organisation's own priorities.
- Complete the asset profile before brainstorming threats; the profile is the basis for
  threats and risks in later steps.

## Verify
- [ ] Each high-score risk has a chosen approach and a mitigation strategy.
- [ ] The step 1 criteria were agreed by the business before scoring.

## Checked
Confirmed 2026-11-09 against the SEI report landing page and the full report PDF (CMU/SEI-2007-TR-012), the section 3 step descriptions, the worksheet list, the step 5 threat tree table, the step 7 scoring activity and the step 8 pool table.
Removed as unconfirmed: the "lightweight, small team in workshops without deep risk expertise" framing, the examples of containers by type (people, paper, laptops), the specific contractor example, the claim that people containers surface insider scenarios, the advice to keep assets coarse, and the gotcha that scores must never be compared across organisations.
Method: docs-checked 2026-11-09 against the SEI Allegro report landing page and the full PDF (steps, worksheets, scoring, pool sections read)
