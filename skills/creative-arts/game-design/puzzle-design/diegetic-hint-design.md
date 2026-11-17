---
id: creative-arts.game-design.puzzle-design.diegetic-hint-design
name: diegetic-hint-design
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, diegetic-hints, hint-systems, in-world-hints, player-guidance]
level: practitioner
status: draft
description: "Design diegetic hints that live in the world: NPC remarks, environmental clues, character barks and in-fiction hint objects, escalated by stuck time without breaking immersion."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://grumpygamer.com/why_adventure_games_suck
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diegetic hints

**Goal:** help stuck players from inside the fiction so the solve still feels earned and
the world stays intact.

## Methods
| Method | Example |
|---|---|
| Character barks | the player-character or companion mutters a thought ("That pipe looks loose") |
| NPC conversation | an NPC whose dialogue changes with stuck time |
| Environmental | a scratch mark, a worn path, a light on the key object |
| In-world documents | a diary page with the cipher key, placed in the next room |
| Hint objects | in-fiction oracles: Professor Layton's hint coins, a crystal ball, a phone call |
| Camera and audio | a camera pan, a sound from the relevant object |

## Escalation design
1. **Detect stuck:** time since last progress, repeated failed attempts, or wandering
   (visiting the same rooms).
2. **Tier the hints:** nudge (attention: "something about the clock"), direction
   (what: "the hands could be moved"), near-answer (how).
3. **Time thresholds** per tier, tuned in tests (e.g. 2, 4, 7 minutes for a mid puzzle).
4. **Reset on progress**, and do not repeat a bark the player just heard.
5. **Player control:** companion hint barks should be toggleable; some players hate them.

## Writing tips
- Barks phrased as the character's observation, not instructions ("I bet that lever
  isn't just decoration" beats "Pull the lever").
- Hints must be accurate for the current state; stale hints are worse than none.
- Environmental hints need to be noticed: contrast, light, motion.

## Gotchas
- Too-frequent barks (God of War Ragnarok's companion hints drew criticism) patronise
  players; lengthen thresholds and add a setting.
- Hints keyed only to time punish slow, careful players; combine with failed-attempt counts.
- Hints in documents work only if players read them; repeat key clues elsewhere.

## Verify
- [ ] Each puzzle has at least two hint tiers with thresholds.
- [ ] Hints reset or advance correctly after progress.
- [ ] Hint barks can be disabled.
