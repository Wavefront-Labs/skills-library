---
id: creative-arts.design-for-form-and-experience.interaction-design.building-multi-step-forms
name: building-multi-step-forms
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [multi-step-form, wizard, form-wizard, stepper, progress-indicator, form-design, checkout-flow]
level: practitioner
status: draft
description: "Build multi-step forms and wizards: split by topic, show progress and step names, save state, allow back and edit, validate per step and end with a review step."
sources:
  - "Nielsen Norman Group - Wizards: Definition and Design Recommendations (nngroup.com/articles/wizards)"
  - "GOV.UK Design System - Question pages and Check answers pattern (design-system.service.gov.uk/patterns/check-answers)"
  - "Baymard Institute - Checkout flow and multi-step usability (baymard.com/blog)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-step forms and wizards

**Goal:** long or complex data entry feels manageable and recoverable.

## When to split
Use steps when the form has more than about 8-10 fields, distinct topics, conditional branches or needs saved progress. Do not split short forms; extra clicks hurt.

## Design
1. **Chunk by topic** (about 3-7 steps); one clear task or question per step. Order low-effort, low-risk questions first (momentum), sensitive ones later.
2. **Show progress:** a stepper with step names ("Details, Delivery, Payment, Review") or "Step 2 of 5"; avoid false progress (percent bars that jump). Allow clicking completed steps.
3. **Navigation:** Back and Next/Continue buttons in consistent places; the Back button preserves entries; browser Back works (each step has a URL or history state).
4. **Validate per step** before moving on, with errors specific to the step; allow skipping optional steps.
5. **Save state:** autosave to local storage or server; let people leave and resume ("Save and continue later" with email link) for long applications.
6. **Conditional logic:** hide irrelevant steps and keep the step count honest (recompute).
7. **Review step:** summarise all answers with Change links back to the right step; the final button states the outcome ("Place order", "Submit application").
8. **Confirmation:** explain what happens next and give a reference.

## Gotchas
- A single page with progressive disclosure often beats a wizard for short forms.
- Do not lose input on error or refresh.
- Announce step changes to screen readers (focus to the new heading, `aria-current="step"`).

## Verify
- [ ] Each step has one topic and clear progress; Back preserves data.
- [ ] Review and edit step before final submission.
- [ ] Progress is saved or recoverable; URLs per step.
