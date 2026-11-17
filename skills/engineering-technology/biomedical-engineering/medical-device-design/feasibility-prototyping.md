---
id: engineering-technology.biomedical-engineering.medical-device-design.feasibility-prototyping
name: feasibility-prototyping
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [feasibility-prototype, prototyping, learning-plan, proof-of-concept, biodesign]
level: practitioner
status: draft
description: "Plan feasibility prototypes around the riskiest assumptions: staged fidelity, explicit learning questions and exit criteria before design controls begin."
sources: ["Zenios et al., Biodesign: The Process of Innovating Medical Technologies (prototyping and concept selection chapters)", "ISO 13485 design and development planning (confirm edition)", "https://www.fda.gov"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Feasibility prototyping and learning plans

**Goal:** buy down technical and clinical risk cheaply before committing to controlled design and verification.

## Method
1. List assumptions the concept depends on (the shaft can be pushed through a 90 degree bend, tissue will not adhere). Rank by consequence of being wrong and uncertainty.
2. For each, write a learning question and a measurable exit criterion (pushes through the fixture at under a stated force is an example form).
3. Match fidelity to the question: sketch or foam model (ergonomics), looks-like (form), works-like (function on bench), then animal or cadaver model when bench cannot answer.
4. Run cheapest first; record results and decisions, including failures.
5. Keep a feasibility log; it is not a design history file but it justifies later requirements. Mark prototypes as not for human use.
6. Transition: when feasibility questions are answered, freeze concept and start design controls; do not reuse unverified prototype data as verification evidence.

## Traps
- Building a full prototype before testing the single risky function.
- Testing in an idealised bench model that hides the clinical failure mode.
- Using prototypes on people or animals without ethics approval and applicable controls.

## Verify
- [ ] Each prototype has a learning question and exit criterion.
- [ ] Results and decisions logged.
- [ ] Handover to design controls is explicit.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
