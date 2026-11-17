---
id: creative-arts.game-design.systems-and-mechanics.writing-a-feature-spec
name: writing-a-feature-spec
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-and-mechanics, feature-spec, game-design-document, design-documentation, acceptance-criteria]
level: practitioner
status: draft
description: "Write a one-feature design spec engineers and artists can build from: player goal, rules, states, tuning values, edge cases, dependencies and acceptance criteria."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.routledge.com/Game-Design-Workshop-A-Playcentric-Approach-to-Creating-Innovative-Games/Fullerton/p/book/9781032611631
  - https://www.atlassian.com/agile/project-management/user-stories
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a feature spec

**Goal:** a short document per feature that answers every question a builder would otherwise ask you.

## Template
1. **Summary** - one paragraph: what the feature is and why players want it.
2. **Player experience** - the intended feeling, tied to a design pillar.
3. **User stories** - "As a player, I can ... so that ...".
4. **Rules** - numbered, testable statements. Numbers live in the tuning table, not in prose.
5. **States and flow** - state diagram or flowchart (idle, active, cooldown, failed).
6. **UI/UX** - wireframe, feedback for each state, input mapping.
7. **Tuning table** - every variable, default, range, and whether designers can edit it.
8. **Edge cases** - disconnect, pause, death mid-action, inventory full, multiplayer
   authority, save/load mid-state.
9. **Dependencies** - systems touched, assets needed (art, audio, VFX, text), telemetry events.
10. **Acceptance criteria** - checkable conditions for "done".
11. **Open questions** - with owner and due date.
12. **Change log**.

## Practice
- Keep it to 2-5 pages; link out to the data sheet instead of pasting numbers.
- Review with engineering, art, audio and QA before build; QA writes test cases from
  sections 8 and 10.
- Use "must / should / may" consistently.
- Mark speculative sections; do not spec in detail what has not been prototyped.

## Gotchas
- Prose numbers drift from the data; keep one source of truth in the tuning sheet.
- Specs written after implementation become fiction; update them or delete them.
- Missing failure feedback is the most common gap: specify what the player sees when it does not work.

## Verify
- [ ] Every rule testable.
- [ ] Tuning table with ranges.
- [ ] Edge-case list reviewed by an engineer.
- [ ] Acceptance criteria used by QA.
