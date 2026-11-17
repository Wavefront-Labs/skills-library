---
id: creative-arts.design-for-form-and-experience.ux-design.user-flows-and-low-fidelity-wireframes
name: user-flows-and-low-fidelity-wireframes
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [ux-design, user-experience, ux, user-flows, task-flows, flowcharts, happy-path, edge-cases, error-states, empty-states, wireframes, wireframing, low-fidelity, lo-fi, sketching, paper-prototyping, information-architecture, content-hierarchy, jobs-to-be-done, user-goals, entry-points, figma, figjam, balsamiq, whimsical, miro, usability, heuristics, nielsen-heuristics, design-critique]
level: practitioner
status: draft
description: "Map a user task as a flow (entry points, decisions, happy path, errors, empty states), then wireframe each screen in grey boxes to settle hierarchy and content before any visual design."
sources:
  - "Nielsen Norman Group articles on user flows, wireframes and the 10 usability heuristics"
  - "Garrett, The Elements of User Experience (New Riders)"
  - "Krug, Don't Make Me Think, Revisited (New Riders)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# User flows and low-fidelity wireframes

**Goal:** decide *what happens and in what order* before deciding what it looks like.
A user flow maps the steps for one goal; low-fidelity wireframes give each step a screen
layout of content and controls. Mistakes caught here cost minutes; in visual design or
code they cost days.

> **Status: draft.** Standard UX practice (NN/g, Garrett's planes). Tool names are
> examples; the method works on paper.

## 1. Frame one task
Write: **user + goal + context.** "A returning customer wants to reorder last month's
groceries on their phone during a commute." One flow per goal. Note what they know, what
data the system already has, and the success state ("order confirmed, delivery slot booked").

## 2. Draw the user flow
Use simple notation (FigJam, Miro, Whimsical, paper):
- **Rectangles** = screens/pages, **diamonds** = decisions, **rounded** = start/end, arrows = actions.
- **Entry points:** where do users arrive from — home screen, push notification, email
  link, search result? Flows rarely start at the home screen.
- **Happy path** first, start to success, fewest steps.
- Then add branches: **errors** (payment declined, item out of stock), **edge cases**
  (no previous order, logged out, offline), **empty states**, and **exits** (where they
  might abandon).
- Count steps and decisions on the happy path. Each removed step usually raises completion.

Check the flow against the site/app structure (information architecture). If labels and
grouping are uncertain, test them first — see
`media-communication.library-and-archive-science.information-architecture.card-sorting-and-tree-testing`.

## 3. Wireframe each screen in the flow
- **Low fidelity:** greyscale boxes, real-ish text (not lorem ipsum for headings and
  buttons — words are part of the design), no colour, no imagery beyond an X box, one
  system font. Balsamiq-style or plain grey frames in Figma; or pen on paper.
- **Start mobile or with the most constrained viewport** — forces priority.
- For each screen ask:
  1. What is the **one primary action**? Make it the most prominent element.
  2. What information does the user **need to decide**? Order content by that.
  3. What is the **back/escape** route?
  4. What does it look like **empty, loading, and in error**?
- Annotate: behaviours ("tap reorders whole basket"), rules ("hide if no past orders"),
  data source. Annotations make wireframes a spec.

## 4. Review cheaply
- Walk the flow screen by screen with a teammate playing the user, out loud.
- Run a **heuristic check** (Nielsen's 10: visibility of status, match with real world,
  user control, consistency, error prevention, recognition over recall, etc.).
- If possible, put paper or clickable wireframes in front of 3–5 target users with a task;
  watch, don't help. (See `creative-arts.design-for-form-and-experience.prototyping.running-a-prototype-walkthrough-test`.)
- Iterate the flow before increasing fidelity.

## Gotchas
- **Designing only the happy path:** errors and empty states end up designed by
  developers at the last minute.
- **Wireframes too polished:** stakeholders critique colours and miss structure. Keep it grey.
- **Lorem ipsum** hides real content length issues (long product names, translations).
- **One flow for many goals:** separate "reorder" from "browse new products".
- Ignoring entry from deep links and notifications.

## Verify
- [ ] Task stated as user + goal + context + success state.
- [ ] Flow shows entry points, happy path, errors, edge cases, empty states.
- [ ] Every screen has one clear primary action and annotated behaviours.
- [ ] Empty, loading and error variants wireframed for key screens.
- [ ] Walked through by someone else and heuristics-checked before visual design.
