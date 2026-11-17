---
id: creative-arts.design-for-form-and-experience.ux-design.annotating-wireframes
name: annotating-wireframes
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [wireframe-annotation, wireframe-notes, annotated-wireframes, wireframing, design-notes]
level: practitioner
status: draft
description: "Annotate wireframes so developers and stakeholders understand behaviour: numbered callouts, rules, content sources, states and open questions, kept separate from the layout."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Wireframe annotation

Annotations explain what the wireframe cannot show: behaviour, rules, data and reasons.

## What to annotate
- **Purpose** of the screen and priority content.
- **Behaviour:** what each control does, what happens on hover, focus, error and success; validation rules and limits.
- **Data and content:** source, who maintains it, character limits, empty states, dynamic vs static.
- **Conditions:** shown only to certain roles or states, feature flags.
- **Rationale:** a short line saying why, linked to research or requirements.
- **Open questions** and assumptions to confirm.
- **Accessibility notes:** heading structure, reading and focus order, alt text (see `...interaction-design.annotating-designs-for-accessibility`).

## How
1. Number callouts on the wireframe (1, 2, 3) and list the notes beside or below in the same order.
2. Keep each note to one or two sentences; one rule per note.
3. Use a consistent colour or style for annotations so they are not mistaken for UI; keep them outside the artboard or on a separate layer so they can be hidden.
4. Use a standard set of icons or labels: Behaviour, Content, Rule, Question.
5. Version and date the annotated file; track resolved questions.

## Gotchas
- Annotations that restate the visible (a "button" label).
- Contradictions between notes and the visuals; engineers will follow the note.

## Verify
- [ ] Every interactive element is explained.
- [ ] Open questions have owners.
- [ ] Annotations can be toggled off without changing the layout.
