---
id: creative-arts.design-for-form-and-experience.prototyping.paper-prototype-testing
name: paper-prototype-testing
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [paper-prototype-testing, paper-prototype, prototype-fidelity, low-fidelity-prototype, sketch-prototype, usability-testing]
level: practitioner
status: draft
description: "Test paper prototypes: sketch screens and states, run sessions with a human computer, a facilitator and observers, and iterate between participants."
sources:
  - "Carolyn Snyder, Paper Prototyping (Morgan Kaufmann, 2003)"
  - "Nielsen Norman Group - Paper Prototyping: Getting User Data Before You Code (nngroup.com/articles/paper-prototyping)"
  - "Jake Knapp et al., Sprint (2016) - fidelity trade-offs"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Paper prototype testing

**Goal:** learn whether the structure and flow work before investing in screens or code.

## Prepare
1. Define 3-5 **tasks** to test and the screens, states and messages those tasks need (default, error, empty, confirmation, menus).
2. Sketch **each screen on a card or sheet** at actual device size (a phone outline template), with separate pieces for dropdowns, dialogs, keyboards and focus states; use Post-it notes as repositionable fields and tape/white-out for changes. Neat is unnecessary; legibility matters.
3. Assemble a **screen set and a "stack" of states** in a tidy order so the Computer can find them quickly; write task cards and a script.

## Roles
- **Facilitator:** gives tasks, asks users to think aloud, probes ("What do you expect to happen?"), does not explain the interface.
- **Computer:** silently swaps screens in response to touch or finger taps, never helps; knows the system rules.
- **Observers:** note issues, quotes and severity.
- **User:** taps with a finger or a pencil, writes in fields.

## Run (30-45 min)
Brief the user (testing the design, not them), practice with a simple task, run the tasks, then debrief with open questions. Record with a camera pointing at the sheet if consent is given.

## Iterate
Fix obvious problems **between sessions** (re-sketch a label, add a missing state), because paper is cheap; stop when new users stop finding new issues (typically 5-8 participants).

## Gotchas
- Paper tests structure, labelling and flow, not visual design, performance or small interaction details; follow up with a higher-fidelity test (`creative-arts.design-for-form-and-experience.prototyping.choosing-prototype-fidelity`).
- Do not draw the whole app; prototype only the tasks to test.

## Verify
- [ ] Tasks map to the screens and states built.
- [ ] Computer and facilitator roles kept distinct and silent about answers.
- [ ] Changes made between sessions and logged.
