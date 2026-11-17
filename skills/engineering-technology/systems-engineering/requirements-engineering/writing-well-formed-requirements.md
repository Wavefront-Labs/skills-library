---
id: engineering-technology.systems-engineering.requirements-engineering.writing-well-formed-requirements
name: writing-well-formed-requirements
category: engineering-technology
field: systems-engineering
product: requirements-engineering
tags: [requirements-engineering, requirement-writing, well-formed-requirements, ears, easy-approach-to-requirements-syntax, shall-should-will, verifiability, rationale, ambiguity, tbd-tbr, requirement-quality, singular-requirement, needs-vs-requirements, specification-review, system-requirements, nasa-se-handbook]
level: practitioner
status: docs-checked
description: "Write singular, verifiable requirements: shall/will/should usage, EARS sentence patterns, NASA handbook writing checklist, rationale, and an unverifiable-word list."
sources:
  - "https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf"
  - "https://alistairmavin.com/ears/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing well-formed requirements — one testable obligation per statement

**Goal:** turn stakeholder needs into requirement statements that a designer can build to and a tester can pass/fail, without arguing about what they mean.

## 1. Terms
- **shall** = requirement. **will** = fact or declaration of purpose. **should** = goal (NASA SE Handbook, Appendix C).
- Product requirement form: "The product shall ...". Use consistent terminology for the product and its lower-level entities.
- Keep stakeholder needs in a separate set and trace requirements to them. Distinguish needs from wants: if it is not necessary to meet the parent requirement, it is not a requirement.

## 2. EARS patterns (Mavin)
| Pattern | Template |
|---|---|
| Ubiquitous | The `<system>` shall `<response>`. |
| Event-driven | **When** `<trigger>`, the `<system>` shall `<response>`. |
| State-driven | **While** `<precondition>`, the `<system>` shall `<response>`. |
| Unwanted behaviour | **If** `<trigger>`, **then** the `<system>` shall `<response>`. |
| Optional feature | **Where** `<feature is included>`, the `<system>` shall `<response>`. |
| Complex | Combine keywords, e.g. **While** `<state>`, **when** `<trigger>`, the `<system>` shall `<response>`. |

## 3. Writing checklist (NASA SE Handbook, Appendix C)
- Say who or what shall act; sentences like "The operator shall ..." are usually operational statements, not product requirements. Put operations in the ConOps and task assignments in the SOW/task order.
- State what is needed, not how to provide it. Ask "why do you need it?" to find the real requirement.
- One thought per statement: one subject and one predicate, no requirement-plus-rationale paragraphs.
- Give tolerances for performance values (less than, greater than or equal to, plus or minus).
- State positively rather than "shall not".
- No indefinite pronouns (this, these) or ambiguous terms such as "as appropriate", "etc.", "and/or", "but not limited to".
- Unverifiable words to avoid (the handbook's list): flexible, easy, sufficient, safe, ad hoc, adequate, accommodate, user-friendly, usable, when required, if required, appropriate, fast, portable, light-weight, small, large, maximize, minimize, robust, quickly, easily, clearly, other "ly" and "ize" words.
- Each requirement is uniquely numbered and bidirectionally traceable to higher-level requirements, needs, goals or ConOps.
- Include an intelligible rationale with assumptions; confirm assumptions before baselining.
- Minimise TBD values: use a best estimate marked TBR with rationale, what will remove it, who is responsible and by when.

## 4. Attributes that travel with the text
Unique ID, rationale, parent trace, verification method (analysis, inspection, demonstration or test), owner, status, and TBD/TBR with owner and close date.

## Gotchas
- A verifiable-looking requirement with no stated condition still fails test day: state the conditions the value applies under.
- Rewriting to pass a checklist can lose intent: reread against the parent need.
- Performance allocated to children must add up (latency, mass, power): check the roll-up.
- Interface requirements belong in the interface requirements document / ICD: see engineering-technology.systems-engineering.interface-management.n2-diagrams-and-icd-authoring.
- "Shall comply with standard X" pulls in every clause: cite the paragraph and edition you mean.

## Verify
- [ ] Each statement has an explicit subject, one "shall", and passes an unverifiable-word scan.
- [ ] Each performance value has a unit, tolerance and applicable condition.
- [ ] Each requirement has rationale, a parent trace and a proposed verification method (feeds engineering-technology.systems-engineering.verification-validation.verification-cross-reference-matrix).
- [ ] Every TBD/TBR has an owner and a closure date.
- [ ] Set check done: no conflicts, no duplicates, all parent needs covered.

## Checked
2026-11-01. Confirmed in the NASA Systems Engineering Handbook (SP-2016-6105 Rev 2) Appendix C: shall/will/should meanings, product requirement form, active voice, WHAT-not-HOW, one thought per statement, tolerances, positive statements, ambiguous terms, unverifiable-word list, TBD/TBR guidance, rationale and assumptions, bidirectional traceability, unique numbering. Confirmed on alistairmavin.com/ears: the six EARS patterns and keywords. Removed (not confirmed in readable sources; INCOSE GtWR and ISO/IEC/IEEE 29148 are paywalled): GtWR characteristic lists and version numbering, ISO 29148 claims, "must" guidance, "each" versus "all", the extended banned word list beyond NASA's, a zero-TBD-at-CDR target, the paraphrase-test count.
Method: documentation only; no commands were run.
