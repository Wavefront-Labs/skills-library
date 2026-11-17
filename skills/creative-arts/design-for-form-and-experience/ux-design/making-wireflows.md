---
id: creative-arts.design-for-form-and-experience.ux-design.making-wireflows
name: making-wireflows
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [wireflow, wireflows, wireframe-flow, screen-flow, ux-deliverable]
level: practitioner
status: draft
description: "Make a wireflow: combine low-fidelity screens with flow arrows to show how a task moves between states, with triggers, conditions and annotations."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Wireflows

A wireflow places simplified wireframes in sequence with arrows showing the interaction that moves from one screen or state to the next. It joins the content detail of wireframes with the logic of flow diagrams (see `...ux-design.drawing-user-flow-diagrams`).

## Build
1. **Start from the user flow** for one task.
2. **Sketch minimal wireframes** for each key screen or state: layout blocks, key content and controls; no visual styling (see `...ux-design.user-flows-and-low-fidelity-wireframes`).
3. **Arrange left to right** (or top to bottom) in order; connect screens with arrows from the specific control that triggers the transition (draw the arrow from the button, not the screen edge).
4. **Add decision points** as diamonds or branching arrows labelled with the condition.
5. **Show states** (loading, error, empty, success) as separate frames where they change what the user does.
6. **Annotate** notes for behaviour, validation, data and rules; number the callouts.
7. **Share** in FigJam, Figma or on a wall; walk stakeholders through the task step by step.

## When to use
When you must show behaviour across screens to engineers and stakeholders, for example onboarding, checkout, multi-step setup.

## Gotchas
- Too much detail makes the wireflow unreadable; one task per diagram.
- Arrows that start from the screen and not the trigger hide interaction.

## Verify
- [ ] Every arrow starts from a labelled control or event.
- [ ] Error and empty states appear where they alter the path.
- [ ] A new reader can narrate the task from the diagram.
