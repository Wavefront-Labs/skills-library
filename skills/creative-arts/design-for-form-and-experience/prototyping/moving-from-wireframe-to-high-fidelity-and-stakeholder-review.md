---
id: creative-arts.design-for-form-and-experience.prototyping.moving-from-wireframe-to-high-fidelity-and-stakeholder-review
name: moving-from-wireframe-to-high-fidelity-and-stakeholder-review
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [wireframe-to-hifi, stakeholder-review, design-review, visual-design-process, design-approval, hi-fi-handoff, design-sign-off]
level: practitioner
status: draft
description: "Move wireframes to high fidelity: apply the style, components and states in layers, and run stakeholder design reviews that frame the feedback and record sign-off."
sources:
  - "Nielsen Norman Group - articles on design critiques and presenting design to stakeholders (nngroup.com)"
  - "Aaron Irizarry and Adam Connor, Discussing Design (O'Reilly, 2015)"
  - "Figma - Design review workflows and comments (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# From wireframe to high fidelity, and stakeholder review

## Layered conversion
1. **Lock the structure** from wireframes: flows, layout, hierarchy and content priorities approved (`creative-arts.design-for-form-and-experience.ux-design.user-flows-and-low-fidelity-wireframes`).
2. **Apply foundations:** grid, colour roles, type styles, spacing tokens, then components from the library (`creative-arts.design-for-form-and-experience.figma.auto-layout-components-and-variants`).
3. **Pass one:** visual hierarchy and branding on key screens (home, core task); resolve spacing and alignment.
4. **Pass two:** all states (empty, loading, error, success, disabled), breakpoints, dark mode if needed, accessibility annotations.
5. **Pass three:** real content, imagery and microcopy (`creative-arts.design-for-form-and-experience.prototyping.building-realistic-high-fidelity-mockups`); motion specs and prototype.
6. **QA** against the system: layer names, auto layout, contrast, text styles, tokens used, nothing detached.

## Stakeholder review
- **Before:** share the brief, goals, constraints and what decisions you need; send an overview 24 h ahead if possible; separate **review** (feedback) from **approval** (decision).
- **Run:** present the **user's journey first**, not screens in isolation; explain decisions in terms of goals and research; show alternatives where meaningful (A/B options with rationale); take questions, then structured feedback (`creative-arts.design-for-form-and-experience.ux-design.facilitating-a-design-critique`).
- **Handle feedback:** write it down verbatim, ask for the **problem** behind a solution ("make the logo bigger" to "the brand isn't recognisable"), classify (must fix, consider, out of scope), reply with decisions and reasons, and avoid design by committee.
- **Sign-off:** record who approved what, version, date and open items (a decision log); freeze the approved version (Figma branch or version label) before handoff.

## Verify
- [ ] Structure frozen before visual design; states and breakpoints covered.
- [ ] Review framed around goals; feedback classified and answered.
- [ ] Approval recorded for a versioned design.
