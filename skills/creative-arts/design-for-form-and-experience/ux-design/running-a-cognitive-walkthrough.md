---
id: creative-arts.design-for-form-and-experience.ux-design.running-a-cognitive-walkthrough
name: running-a-cognitive-walkthrough
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [cognitive-walkthrough, usability-inspection, learnability, task-analysis, ux-research]
level: practitioner
status: docs-checked
description: "Run a cognitive walkthrough: step through a task as a first-time user and answer the four walkthrough questions at every action to find learnability failures."
sources:
  - https://www.nngroup.com/articles/cognitive-walkthroughs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cognitive walkthrough

**Goal:** judge how easily a **new user** can work out the correct action sequence for a task, one step at a time. It evaluates learnability, not efficiency.

## Setup
- Choose the user tasks in advance, for example from a list of top tasks.
- Roles: a facilitator, evaluators (a cross-functional team: UX, product owners, engineers, domain experts) and a recorder.
- Write the ideal path as numbered steps; the facilitator sets the step granularity beforehand. Early prototypes work.

## Steps
1. The facilitator performs the task and stops at each new screen or discrete step.
2. The group answers the four questions for that step.
3. If any answer is "No", the recorder marks the whole step as Fail.
4. Repeat until the task is complete, then summarise the fail points and discuss next steps.

## The four questions, asked at every step
1. Will users try to achieve the right result?
2. Will users notice that the correct action is available?
3. Will users associate the correct action with the result they are trying to achieve?
4. After the action is performed, will users see that progress is made toward the goal?

## Recording
The recorder documents the answer to each question and whether the task will likely succeed or fail. Give each "No" a short failure story (why this user would miss it) so the debrief is not opinion.

## When to use
Best for complex, new or unfamiliar workflows on early prototypes, and when access to users is limited. Poorly suited to standard patterns such as a basic ecommerce checkout. Combine with other methods.

## Verify
- [ ] Tasks and user profile written down before the session.
- [ ] Every step has four answers and a Pass or Fail.

## Checked
2026-11-01. Confirmed against NN/g "Cognitive Walkthroughs": steps, four questions, pass/fail rule, roles, suitability. Removed: team size of 2-4, the two-question streamlined variant attributed to Spencer, "fix by earliest failure" advice, and the book, IxDF and CHI sources (not read).
Method: documentation only; no commands were run.
