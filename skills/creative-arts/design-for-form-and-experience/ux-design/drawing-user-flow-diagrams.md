---
id: creative-arts.design-for-form-and-experience.ux-design.drawing-user-flow-diagrams
name: drawing-user-flow-diagrams
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [user-flow-diagram, user-flow, flowchart-notation, task-flow, user-flows]
level: practitioner
status: docs-checked
description: "Draw user flow diagrams: choose entry points, use consistent flowchart shapes, show decisions, system responses and exits, and keep one goal per flow."
sources:
  - https://www.nngroup.com/articles/user-journeys-vs-user-flows/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# User flow diagrams

A user flow shows the path a person takes to reach a goal, including decisions and system responses. NN/g defines it as the typical or ideal set of steps to accomplish a common task with one product; it captures key user steps and system responses, not emotions or thoughts (that is a journey map). Flow charts, wireflows and task diagrams are the usual forms. Usability testing is the best research source, with analytics such as click heatmaps as a secondary one.

## Build
1. **Define one goal** that users can reach in minutes or hours (for example "new user subscribes"). Split different goals into separate flows.
2. **Set the entry points** (search, email link, home) and the **success end state**.
3. **Draw with a small, consistent shape set** for start and end, steps or screens, decisions with labelled branches, and system responses. Add a legend.
4. **Show the happy path first,** then branches: validation errors, cancellations, back steps, timeouts and permission denials (see `...ux-design.designing-error-and-edge-case-flows`).
5. **Annotate** each step with the system response.
6. **Link to wireframes** or screens by ID.
7. **Review** with engineering and support for missing cases.

## Gotchas
- Mixing goals in one chart creates spaghetti.
- Skipping the "unhappy" paths hides most real work.

## Verify
- [ ] Each decision has labelled exits.
- [ ] Every flow has a defined start and end.
- [ ] Error and cancel branches are covered or listed as open.

## Checked
2026-11-01. Confirmed against NN/g, User Journeys vs. User Flows: definition, goal granularity (minutes or hours, one product), artifact types, what a flow captures and omits, usability testing and analytics as sources. Removed (not stated there): specific shape-to-meaning mapping, persona requirement, drop-off metric annotation, named diagram tools, the Topics-page source.
Method: documentation only; no commands were run.
