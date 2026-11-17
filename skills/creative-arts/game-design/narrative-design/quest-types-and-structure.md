---
id: creative-arts.game-design.narrative-design.quest-types-and-structure
name: quest-types-and-structure
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, quest-design, quest-types, quest-structure, fetch-quest, objectives, rpg, side-quests, quest-beats]
level: practitioner
status: draft
description: "Structure quests from a taxonomy of quest types (kill, fetch, escort, deliver, investigate, defend), with hook, complication, choice and payoff, and avoid filler fetch quests."
sources:
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quest types and structure

**Goal:** quests with clear objectives, a story worth following, and at least one
complication or choice, built from known quest types without feeling like chores.

## Quest types (mechanical core)
| Type | Core activity | Make it interesting by |
|---|---|---|
| Kill / defeat | combat | unique encounter, moral context |
| Fetch / gather | travel, collection | a complication on the way, interesting location |
| Deliver | travel with item | time pressure, temptation to open/keep |
| Escort | protect NPC | competent NPC, conversation en route |
| Investigate | gather clues, deduce | real deduction, wrong conclusions possible |
| Defend / survive | hold position | prep phase, choices of defences |
| Talk / persuade | dialogue | skill checks, information as leverage |
| Explore / discover | reach a place | the place is the reward |
| Puzzle | solve | ties to quest story |

## Structure template
1. **Hook:** why the player cares (personal stake, curiosity, reward).
2. **Objective:** concrete and trackable (see quest-log practices).
3. **Complication / twist:** something changes (the client lied, the target is
   sympathetic, the route is blocked).
4. **Choice:** at least one meaningful decision where possible.
5. **Payoff:** reward plus a consequence the player can see (world reacts).
6. **Echo:** later reference to the quest (an NPC mentions it).

## Procedure
1. Write the quest on one card: giver, hook, objective, complication, choice, payoff,
   echo, location, estimated minutes.
2. Check variety across the quest set (not five fetch quests in a row in one area).
3. Check objectives are trackable in the UI and don't break if done out of order.
4. Playtest for clarity: can players say what to do and why?

## Gotchas
- "Kill 10 rats" with no story or complication is filler; even small quests need a hook
  or twist.
- Quest state bugs (doing steps out of order, killing the quest giver) are common;
  design fallback states.
- Long chains of travel with nothing happening pad play time.

## Verify
- [ ] Each quest card has hook, complication and payoff.
- [ ] Quest type mix varied per region.
- [ ] Out-of-order and NPC-death states handled.
