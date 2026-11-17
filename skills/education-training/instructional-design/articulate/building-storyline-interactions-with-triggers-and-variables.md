---
id: education-training.instructional-design.articulate.building-storyline-interactions-with-triggers-and-variables
name: building-storyline-interactions-with-triggers-and-variables
category: education-training
field: instructional-design
product: articulate
tags: [articulate, articulate-360, storyline, storyline-360, rise, rise-360, triggers, variables, true-false-variable, number-variable, text-variable, conditions, states, layers, slide-layers, hotspots, sliders, question-banks, result-slide, quiz, branching, publish, scorm, xapi, review-360, lms-publishing, elearning-authoring, authoring-tool, captivate, instructional-design]
level: practitioner
status: draft
description: "Build Storyline 360 interactions with states, layers, triggers and variables; know when to use Rise blocks instead; set up quiz result slides and publish to an LMS without tracking surprises."
sources:
  - "Articulate 360 support documentation and E-Learning Heroes community (articulate.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building Storyline interactions with triggers and variables

**Goal:** build interactive e-learning in Articulate Storyline 360 that behaves reliably,
is maintainable by the next developer, and tracks correctly in the LMS — and know when Rise
360 is the faster choice.

*Feature names reflect Storyline 360 / Rise 360 as generally documented; Articulate updates
360 frequently, so confirm exact menu paths in the current version.*

## 1. Storyline or Rise?
| Use **Rise 360** when | Use **Storyline 360** when |
|---|---|
| Content is mostly text, media and simple checks | You need custom interactions, simulations or scenarios with state |
| Responsive mobile layout matters most | You need precise slide-based layout and animation |
| Fast turnaround, many SMEs editing | You need variables, conditional logic, custom scoring |
You can embed a Storyline block inside Rise for one complex interaction.

## 2. The four building blocks
- **States** — how an object looks: Normal, Hover, Down, Selected, Visited, Disabled, plus custom
  states (e.g. "Correct"). Built-in states like Visited and Selected change automatically.
- **Layers** — overlays on a slide (feedback pop-ups, reveal panels). Layer properties control
  whether the base layer is hidden or clickable while the layer is open.
- **Triggers** — *action + when + object + conditions*. E.g. "Show layer **Feedback** when the user
  clicks **Submit** if **Answer1** = True."
- **Variables** — True/False, Number, Text; project-wide. Name them meaningfully (`visitedTab3`,
  `scoreScenario`), not `Variable1`.

## 3. Pattern: "click all tabs, then Next unlocks"
1. Create three buttons; each has a **Visited** state (Storyline applies it on click).
2. Set the Next button's initial state to **Disabled**.
3. Add a trigger on Next: *Change state of Next to Normal when the state of all of Tab1, Tab2,
   Tab3 is Visited.*
Simpler than a variable per tab, and it works because state-based conditions are evaluated when
states change.

## 4. Pattern: scenario with a score variable
1. Create Number variable `trust` (default 5).
2. On each choice, trigger *Add 2 to trust* or *Subtract 2 from trust*, then *Jump to* the next
   scene slide.
3. On the final slide, triggers: *Show layer Good ending when timeline starts if trust ≥ 7*;
   *… Mixed ending if trust ≥ 4 and < 7*; *… Poor ending if trust < 4*.
4. Display the value on screen while testing by inserting `%trust%` in a text box; delete it before publishing.

## 5. Quizzes and result slides
- Build question slides via **Insert › New Slide › Quizzing** (graded/survey/freeform).
  Freeform turns your own drag-drop or hotspot into a graded question.
- Use a **question bank** to draw random questions for retakes.
- Add a **Results slide**: choose which questions it tracks and the pass score.
- Tracking: in **Publish › LMS › Reporting and Tracking**, choose to track using the *results
  slide* or *slides viewed* (or, in newer versions, multiple completion criteria). This choice is
  the main cause of "course won't complete" tickets.

## 6. Publish and test
- **Review 360** for SME comments on a hosted preview.
- **LMS publish**: choose the standard your LMS supports (SCORM 1.2, SCORM 2004, xAPI, cmi5,
  AICC); match LMS reporting status (e.g. Passed/Incomplete vs Completed/Incomplete) to what your
  LMS expects.
- Test the published package in **SCORM Cloud** and then the real LMS before release — see
  education-training.instructional-design.scorm-and-xapi.packaging-and-debugging-lms-tracking.

## Gotchas
- **Trigger order matters:** triggers on the same event run top to bottom. Put variable
  adjustments *before* the jump or layer-show that depends on them.
- **Jump triggers end execution** on that slide — triggers below a "Jump to slide" may never run.
- **Slide properties "When revisiting"** (reset to initial state vs resume saved state) changes
  behaviour on Back navigation; set it deliberately.
- **Player features** (menu, seekbar) can let learners skip locked content; check player settings.
- Keep a **variable list** in the storyboard so the logic is documented.
- Accessibility: set focus order and alt text; custom drag-and-drop often fails keyboard users —
  provide an alternative.

## Verify
- [ ] Every variable has a meaningful name and is listed in the storyboard.
- [ ] Each trigger's order was checked; nothing important sits below a jump.
- [ ] Revisit behaviour and player navigation can't bypass required content.
- [ ] Quiz result slide and LMS tracking option match the agreed completion rule.
- [ ] The published package completed and reported a score correctly in SCORM Cloud and the target LMS.
