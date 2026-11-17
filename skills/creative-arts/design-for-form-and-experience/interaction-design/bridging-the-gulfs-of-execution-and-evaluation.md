---
id: creative-arts.design-for-form-and-experience.interaction-design.bridging-the-gulfs-of-execution-and-evaluation
name: bridging-the-gulfs-of-execution-and-evaluation
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [gulf-of-execution, gulf-of-evaluation, seven-stages-of-action, action-cycle, design-of-everyday-things, norman-principles, interaction-design]
level: practitioner
status: draft
description: "Use Norman's seven stages of action to find where a task breaks: bridge the gulf of execution (what can I do) and gulf of evaluation (what happened)."
sources:
  - "Don Norman, The Design of Everyday Things, revised ed. (Basic Books, 2013), chapter 2 The Psychology of Everyday Actions"
  - "Hutchins, Hollan and Norman, Direct Manipulation Interfaces (1985)"
  - "Interaction Design Foundation - Gulf of Execution and Gulf of Evaluation (interaction-design.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gulfs of execution and evaluation

**Goal:** locate which stage of an interaction fails and apply the matching design fix.

## The seven stages
Goal, then **execution**: 1 plan, 2 specify, 3 perform; then **evaluation**: 4 perceive, 5 interpret, 6 compare with the goal.
- **Gulf of execution:** the gap between what the user wants to do and what the system lets them do or shows how to do. Questions: Can I tell what actions are possible (discoverability)? Can I tell how to do them (mapping, signifiers)? Can I perform them (constraints, effort)?
- **Gulf of evaluation:** the gap between the system's state and the user's ability to perceive and interpret it. Questions: Can I tell what state it is in? Did my action work? Is the outcome what I wanted?

## Using it in review
1. Pick a task and list the user's goal.
2. Walk the seven stages and mark where users hesitate, err or ask for help (use test video or a cognitive walkthrough).
3. Execution gulf signs: users scan, hunt in menus, try wrong controls. Fixes: signifiers, natural mapping, visible options, fewer steps, defaults.
4. Evaluation gulf signs: users re-click, ask "did it save?", misread state. Fixes: immediate informative feedback, visible state, undo, progress, confirmation of results.
5. Record the gap, the stage and the fix per task in a table.

## Verify
- [ ] Each observed failure is assigned to a stage and a gulf.
- [ ] The fix targets the gulf (visibility or feedback), not just copy tweaks.
