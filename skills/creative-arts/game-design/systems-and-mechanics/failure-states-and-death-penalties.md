---
id: creative-arts.game-design.systems-and-mechanics.failure-states-and-death-penalties
name: failure-states-and-death-penalties
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, death-penalty, failure-states, punishment, checkpoints, permadeath, respawn, reward-design, frustration, retry-loop]
level: practitioner
status: draft
description: "Choose what failure costs the player (time, progress, resources, permanence), place checkpoints, and keep the retry loop fast so failure teaches instead of punishing."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://mitpress.mit.edu/9780262019057/the-art-of-failure/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failure states and death penalties

**Goal:** failure that matters enough to create tension but costs little enough that
players learn and retry instead of quitting.

Schell (2nd ed.) ch13 lists punishment types (shame, loss of points, shortened play, terminated
play, setback, removal of powers, resource depletion) and notes punishment makes
success meaningful. Juul (*The Art of Failure*) argues failure is central to why games
feel meaningful, provided the player attributes it to their own play.

## Penalty dial
| Penalty | Example | Use |
|---|---|---|
| None / instant retry | Celeste-style instant respawn | precision challenge, learning by repetition |
| Time setback | back to checkpoint | most action games |
| Resource loss | drop currency, recover on corpse run | tension on the return trip |
| Progress loss | lose level/run | roguelikes, survival |
| Permadeath | character gone | high stakes; needs short runs or meta-progression |
| Narrative consequence | story branches on failure | failure as content |

## Design rules
1. **Retry latency:** time from failure to being back in control. Short for challenge
   games (seconds); a long load + cutscene + walk back is the classic frustration.
2. **Checkpoint placement:** before every hard section, after every unskippable
   sequence; never put a long easy stretch between checkpoint and a hard bit.
3. **Make failure legible:** the player must see why they failed (telegraphed attack,
   clear hazard). Unclear causes feel unfair.
4. **Scale penalty with session length:** permadeath in a 30-minute run is exciting; in
   a 40-hour game it is devastating.
5. **Give partial credit:** keep something (XP, unlocks, knowledge) after failure.
6. **Consider difficulty options** for the penalty itself (assist settings that
   reduce it).

## Gotchas
- Lose-all-resources penalties cause "save scumming" or quitting; recoverable losses
  (corpse runs) keep tension without despair.
- Failure from randomness the player could not influence feels like punishment from
  the game, not a lesson.
- Multiplayer penalties affect others (team wipes); avoid one player's failure
  costing the whole team disproportionately.

## Verify
- [ ] Penalty type chosen per failure state with a reason.
- [ ] Retry latency measured (seconds) and within target.
- [ ] Testers can say why they failed in 4 of 5 deaths.
- [ ] No checkpoint gap that repeats long easy content before a hard section.
