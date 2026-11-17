---
id: creative-arts.design-for-form-and-experience.prototyping.running-a-prototype-walkthrough-test
name: running-a-prototype-walkthrough-test
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [prototyping, design-prototyping, prototype-testing, usability-testing, moderated-testing, unmoderated-testing, think-aloud, task-scenarios, clickable-prototype, high-fidelity-prototype, low-fidelity-prototype, paper-prototype, wizard-of-oz, figma-prototype, protopie, maze, lookback, five-users, test-script, observation, note-taking, rainbow-spreadsheet, severity-rating, synthesis, concept-validation, iteration]
level: practitioner
status: draft
description: "Test a design prototype with real users: set the question, pick fidelity, write realistic task scenarios, run think-aloud sessions without leading, log observations, and rate issues by severity."
sources:
  - "Nielsen Norman Group, articles on usability testing, think-aloud and 'Why you only need to test with 5 users'"
  - "Krug, Rocket Surgery Made Easy (New Riders)"
  - "Rubin & Chisnell, Handbook of Usability Testing (Wiley)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a prototype walkthrough test

**Goal:** find out whether a design works for the people it's for — before it's built —
by watching a handful of them try to complete real tasks on a prototype, then turning
what you saw into a ranked list of fixes.

> **Status: draft.** Method follows standard usability-testing practice (NN/g, Krug,
> Rubin & Chisnell). The "five users" guidance applies to finding usability problems in
> one round with a fairly homogeneous audience, not to measuring metrics.

## 1. Decide what you're testing
Write **1–3 questions**: "Can first-time users book a slot without help?" "Do people
understand the difference between Save and Publish?" A test without a question becomes
a demo.

## 2. Pick the fidelity to match the question
| Question type | Prototype |
|---|---|
| Flow, structure, labels | paper or grey clickable wireframes |
| Visual hierarchy, trust, comprehension | high-fidelity clickable (Figma, ProtoPie) |
| Feel of gestures, animation, physical form | coded or device prototype, or physical mockup |
| Concept/value ("would you use this?") | storyboard, landing page, Wizard-of-Oz (a human fakes the system) |

Build **only the paths the tasks need**, but make dead ends safe (a "not built in this
prototype" screen rather than nothing happening).

## 3. Recruit
- **5 participants per distinct user group** typically surface most major issues in one
  round; test again after fixing, rather than testing 15 once.
- Recruit people matching the audience (screen with a few questions); colleagues are a
  last resort and miss domain confusion.
- Get consent for recording; offer an incentive.

## 4. Write the script
- **Intro:** "We're testing the design, not you. Please think aloud. There are no wrong answers."
- **Warm-up questions** about their context.
- **Task scenarios** — realistic goals, not instructions:
  - Good: "You're going on holiday next week and want your plants watered. Find someone
    who can do it on Tuesday."
  - Bad: "Click Services, then Book." (tells them the path and the labels)
- 3–6 tasks, ~30–60 min total. Define what counts as success for each.
- **Wrap-up:** overall impressions, what was confusing, one thing they'd change.

## 5. Run the session
- Moderator and a separate **note-taker**; observers silent (ideally in another room or on a call).
- **Don't lead or rescue.** When asked "Should I click this?", reply "What would you
  expect it to do?" Let silence work. Rescue only if they're stuck for minutes, and log it as a failure.
- Prompt thinking aloud gently: "What are you looking for?"
- Note **behaviour over opinion**: where they hesitated, what they clicked first, what they
  said they expected. Quotes are useful; preferences ("I like blue") are weak evidence.
- Remote unmoderated tools (Maze, Lookback, UserTesting-style platforms) scale, but you lose
  follow-up questions — use them for simpler tasks.

## 6. Synthesise
- After each session, a 10-minute debrief: top observations.
- Put observations in a grid (participants × issues — a "rainbow spreadsheet"), so you see
  how many people hit each problem.
- Rate **severity**: critical (blocks task), serious (big delay/error), minor (annoyance),
  plus frequency.
- Recommend fixes for the top issues; share short clips — they persuade more than reports.
- Fix, then test again.

## Gotchas
- Leading tasks that use the interface's own words.
- Testing too polished, too late — nobody wants to change it then.
- Explaining the design during the session.
- Counting opinions instead of observing behaviour.
- Mixed audiences in one round of five — findings scatter.

## Verify
- [ ] Written test questions and success criteria for each task.
- [ ] Prototype fidelity matches the questions; task paths built, dead ends safe.
- [ ] ~5 participants per user group, recruited from the real audience.
- [ ] Tasks written as goals, not instructions; moderator didn't lead.
- [ ] Issues logged by participant, rated by severity, with fixes and a retest planned.
