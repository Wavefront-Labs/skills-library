---
id: creative-arts.game-design.narrative-design.narrative-continuity-testing
name: narrative-continuity-testing
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, narrative-continuity, narrative-qa, story-testing, state-tracking, dialogue-testing]
level: practitioner
status: draft
description: "Test narrative continuity: state tables, reachable-line coverage, debug menus to set flags, read-throughs per path, and catching references to events the player skipped."
sources:
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
  - https://www.routledge.com/Procedural-Storytelling-in-Game-Design/Short-Adams/p/book/9781138595309
  - https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Narrative continuity and testing

**Goal:** no line references something the player did not do, no character appears after
dying, and every written line is reachable.

## Common continuity bugs
| Bug | Example |
|---|---|
| Phantom reference | NPC thanks you for a quest you skipped |
| Resurrection | dead character greets you in a later town |
| Wrong state | dialogue assumes day while it is night, or old outfit |
| Order break | sequence-broken quest plays reveals out of order |
| Unreachable line | written, recorded, never triggers |
| Duplicate | same reveal delivered twice by two sources |

## Tools to build
1. **State table**: every narrative flag, who sets it, who reads it, default value.
2. **Debug menu** to set flags, jump to chapters and spawn conversations. Narrative QA is
   impossible without it.
3. **Line coverage report**: log each line id when it plays; diff against the full string
   table to find never-played lines.
4. **Static checks** in the script tool: Ink's compiler warnings, Yarn Spinner's
   validation, custom scripts that check each condition references a known flag.

## Test passes
- **Read-through per path**: a writer plays each major branch start to finish and reads every line in context.
- **Skip-everything pass**: do the critical path only, with no optional content; listen for references to the optional content.
- **Max-optional pass**: do everything; listen for duplicated reveals.
- **Order-break pass**: complete quests in unusual orders; sequence break where possible.
- **Death pass**: kill every killable NPC at the earliest point; check later scenes.

## Fix patterns
- Gate references on the flag, with a neutral fallback line.
- Mark quest-critical NPCs essential or write their death into the plot.
- Prefer "first source wins" for reveals: whichever source plays first sets the flag; others use a short variant.

## Verify
- [ ] State table current; every condition references a known flag.
- [ ] Line coverage report shows no unintended unreachable lines.
- [ ] All five test passes completed before VO lock.
