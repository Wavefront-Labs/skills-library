---
id: creative-arts.design-for-form-and-experience.ux-design.analysing-tasks-with-hierarchical-task-analysis
name: analysing-tasks-with-hierarchical-task-analysis
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [hierarchical-task-analysis, hta, task-analysis, task-decomposition, ux-requirements]
level: practitioner
status: docs-checked
description: "Break a user goal into a hierarchy of tasks and subtasks with plans, using hierarchical task analysis to find steps, errors and design opportunities."
sources:
  - https://www.nngroup.com/articles/task-analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hierarchical task analysis

Hierarchical task analysis (HTA) is the task-analysis diagram NN/g calls the most commonly used. It describes a goal as a hierarchy of tasks, each decomposed into subtasks, with **plans** that say in what order or under what conditions the subtasks are done.

## Steps
1. **State the goal** in a short verb phrase ("Send a parcel").
2. **Break into the major tasks** (human factors calls them operations); number them 1, 2, 3 and so on.
3. **Redescribe each subgoal** into subtasks (1.1, 1.2); the number of levels depends on the complexity of the process and how granular you want the analysis.
4. **Write a plan** for each level: the order of the steps and which are undertaken when or by whom, so novice and expert routes are both captured (for example the password-reset steps apply only if the user cannot remember it).
5. **Collect data** by observing and speaking with users and subject-matter experts (contextual inquiry, critical-incident interviews, record keeping, activity sampling, simulations); do not rely only on self-report or simulation.
6. **Draw it** as an HTA diagram that starts from the goal and scenario.
7. **Analyse:** NN/g lists the number of tasks, their frequency, cognitive complexity, physical requirements and time taken (activity sampling or GOMS modelling); look for steps to remove and error-prone steps; check against screens and flows; use as input for task flows (see `...ux-design.user-flows-and-low-fidelity-wireframes`) and for test tasks.

## Gotchas
- Describing how a system works rather than what the user does.
- Going too deep; stop at the level where design decisions occur.

## Verify
- [ ] Every non-trivial node has a plan.
- [ ] Users or experts confirmed the hierarchy.
- [ ] Improvement opportunities from the analysis are listed.

## Checked
2026-11-01. Confirmed against NN/g, Task Analysis: Study How Users Complete Tasks: two stages, data-gathering methods, HTA diagram structure (goal, tasks as operations, subtasks, plans by order and who or when), analysis attributes, the point not to rely only on self-report. Removed (not stated there): Annett and Duncan origin, 4-8 and 7 subgoal rules, stopping rule, loop and timing plan types, indented-outline form, three-opportunity check, the Annett/Duncan and Stanton sources.
Method: documentation only; no commands were run.
