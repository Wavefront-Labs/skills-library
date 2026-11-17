---
id: computing-software.qa-testing-engineering.test-case-design.perspective-and-checklist-based-reading
name: perspective-and-checklist-based-reading
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [perspective-based-reading, checklist-based-review, review-techniques, static-testing, scenario-based-review]
level: practitioner
status: draft
description: "Apply review reading techniques: checklist-based, scenario-based, role-based and perspective-based reading, assigning perspectives so reviewers do not overlap."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.iso.org/standard/67407.html
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Perspective-based and checklist-based reading

**Goal:** make each reviewer look for different defects, systematically. Techniques per ISO/IEC 20246 and the ISTQB syllabi; PBR from Basili et al.

## Techniques
| Technique | How | Best for |
|---|---|---|
| Ad hoc | read and note issues | quick checks; low yield, much duplication |
| Checklist-based | questions derived from past defects | consistent coverage of known defect types |
| Scenario-based | walk through usage scenarios / dry runs | finding missing behaviour |
| Role-based | read as a specific stakeholder (end user, admin, operator) | usability, operability |
| Perspective-based | read as a stakeholder *and produce a derived artefact* | deepest: forces understanding |

## Perspective-based reading (PBR)
Assign each reviewer one perspective with a concrete task:
- **Tester:** write acceptance test cases from the requirement; note anything you cannot write an expected result for.
- **Designer/developer:** sketch the design or data model; note missing information.
- **User:** write the user manual steps for a scenario; note gaps and confusing flows.
- **Operations/security:** describe how to deploy, monitor and attack it.
Studies show PBR teams find more distinct defects with less overlap than ad hoc teams.

## Building a checklist
- 10-20 questions, each answerable yes/no, specific to the work product type ("Does every error message say how to recover?" not "Is it clear?").
- Source questions from defect data and root cause analyses; prune items that never find anything.
- Include questions about what is *missing*, not only what is wrong.

## Gotchas
- Long checklists get skimmed; split them by perspective.
- Checklist-only reviews miss novel defect types; combine with a scenario or perspective.
- Note the technique used in the review record so effectiveness can be compared.

## Verify
Review records show each reviewer's perspective and derived artefact, and duplicate findings across reviewers are low.
