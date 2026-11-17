---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-empty-states
name: designing-empty-states
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [empty-state-design, empty-states, ui-states, interaction-states, first-use, zero-data, onboarding]
level: practitioner
status: draft
description: "Design empty states: tell users why it is empty, what value comes next, and one clear action, for first-use, no-results, cleared and error-caused empties."
sources:
  - "Nielsen Norman Group - Designing Empty States in Complex Applications (nngroup.com/articles/empty-state-interface-design)"
  - "Material Design 3 - Empty states guidance (m3.material.io)"
  - "Carbon Design System - Empty states pattern (carbondesignsystem.com/patterns/empty-states-pattern)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Empty states

**Goal:** turn a blank screen into guidance.

## Types (design each)
1. **First use / nothing created yet:** explain the value and offer the first action ("No projects yet. Create a project to organise your tasks." with a primary "Create project" button). Pair with sample data or templates.
2. **User cleared / completed:** celebrate or confirm ("Inbox zero"); optional light illustration; offer next action.
3. **No results (search/filter):** say what was searched, how to broaden (clear filters button), suggestions; see `creative-arts.design-for-form-and-experience.interaction-design.designing-search-and-autocomplete`.
4. **Nothing to show because of an error or permission:** state the cause and a recovery (`creative-arts.design-for-form-and-experience.interaction-design.designing-error-recovery-states`).
5. **Not yet available** (data still arriving): say when and why.

## Anatomy
Illustration or icon (optional, small), **headline** stating the status, **supporting line** with the benefit or reason, **primary action** (one), optional secondary link (learn more). Left-align for dense app panels; centre for full-page views.

## Tips
- Use the empty space to teach: show what the filled state looks like (a ghosted preview).
- Keep the layout stable: place the empty state where the content will appear.
- Do not just show "No data" or an empty table with headers.
- Localise copy and keep illustrations optional for performance and accessibility (decorative alt).
- Track whether users take the empty-state action.

## Verify
- [ ] Each empty type has a cause, a benefit statement and an action.
- [ ] No dead ends; clear filter and create buttons work.
