---
id: creative-arts.design-for-form-and-experience.prototyping.building-looks-like-and-works-like-prototypes
name: building-looks-like-and-works-like-prototypes
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [looks-like-works-like, looks-like-prototype, works-like-prototype, integrated-prototype, product-prototyping, prototype-strategy]
level: practitioner
status: draft
description: "Split product prototyping into looks-like and works-like models, test form and function separately, then integrate when risks are retired."
sources:
  - "IDSA (idsa.org) education resources"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Looks-like and works-like prototypes

Product teams commonly separate prototypes by the question they answer: a **looks-like** prototype shows form, finish, size and feel; a **works-like** prototype proves the function (mechanism, electronics, performance). An **integrated** prototype combines both later.

## Looks-like
- Purpose: judge appearance, ergonomics, CMF and user reaction.
- Build: foam, clay, 3D prints, painted appearance models (see `...concept-design.making-3d-printed-and-painted-appearance-models`), ergonomic bucks (see `...concept-design.building-ergonomic-bucks-and-sizing-mockups`).
- Does not need working internals; fix the weight and balance with ballast.

## Works-like
- Purpose: test whether the mechanism, circuits, sensors, software and battery do the job.
- Build: breadboards or development boards, ugly mechanical rigs, off-the-shelf parts in a box; size is irrelevant.
- Define the **function tests and pass criteria** (force, cycle count, battery life, accuracy).

## Plan
1. List the **riskiest assumptions** for desirability, usability, feasibility and viability.
2. Choose the cheapest prototype that tests each risk; do not build a full integrated one to learn something a rough one would reveal.
3. Run the looks-like and works-like tracks in parallel; converge in an **integrated prototype** when packaging and electronics must fit (see `...concept-design.designing-wall-thickness-ribs-and-sink-mark-control`).
4. Record test results and decisions.

## Verify
- [ ] Each prototype maps to a stated question.
- [ ] Function tests have pass criteria.
- [ ] The integration step lists fit and tolerance checks.
