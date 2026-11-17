---
id: creative-arts.game-design.narrative-design.choice-consequence-design
name: choice-consequence-design
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, choice-consequence, branching-narrative, meaningful-choice, player-agency, dialogue-choices, reactivity]
level: practitioner
status: draft
description: "Design choices whose consequences players feel: immediate acknowledgement, delayed payoff, state tracking, telegraphing stakes and keeping branch cost under control."
sources:
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
  - https://www.routledge.com/Procedural-Storytelling-in-Game-Design/Short-Adams/p/book/9781138595309
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choice consequence design

**Goal:** choices that feel meaningful because the game visibly remembers them, at a
production cost the team can afford.

## The consequence ladder (cheapest first)
| Level | What changes | Cost |
|---|---|---|
| Acknowledge | next line reacts ("You chose to spare him.") | 1 line |
| Flavour | later barks, journal text, NPC greeting reference it | a few lines per mention |
| State | a variable shifts a meter, unlocks or closes an option | logic plus a few lines |
| Branch | different scene or quest step | full scene per branch |
| Outcome | different ending or world state | very high |

Most choices should live on the first three rungs; reserve branches for a handful of
signature decisions.

## Procedure
1. **List the signature choices** (3-6 per game) in the narrative design doc; for each,
   write what the player believes they are choosing and what the game will remember.
2. **Telegraph stakes** before the choice: who is affected, roughly what is at risk.
   Hidden stakes read as arbitrary punishment, not consequence.
3. **Acknowledge immediately** (within the same scene) so the player knows it registered.
4. **Plan at least one delayed callback** per signature choice, ideally where the player
   does not expect it. Delay is what makes the world feel persistent.
5. **Track with few, named variables** (`spared_captain`, `town_trust`) and log them in a
   state table: variable, set where, read where.
6. **Fold back** (branch and bottleneck) so the main line stays one script: branches
   diverge for a scene and reconverge, carrying flags forward.
7. **Show the record** where the genre supports it: journal entries, codex, end-of-chapter
   summary (Telltale's "X will remember that" is the extreme form).

## Good choices are dilemmas
- Two goods or two evils with different victims beat a clear good-vs-evil pair.
- Avoid choices where one option is plainly optimal on the stats; players will min-max
  and the moral weight disappears.
- Never punish a choice the player could not reasonably foresee unless the theme is
  exactly that, and say so in the doc.

## Gotchas
- Consequence that only appears in an ending players see once is invisible to most of them.
- Meters (paragon/renegade) push players to pick one lane early; consider decay or
  separate axes.
- Each persistent flag multiplies QA; keep the state table current and test combinations.

## Verify
- [ ] Every signature choice has an immediate acknowledgement and a delayed callback.
- [ ] State table lists each flag with its writers and readers.
- [ ] Playtest: players can name what a choice changed when asked afterwards.
