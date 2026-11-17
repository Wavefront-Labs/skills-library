---
id: creative-arts.game-design.narrative-design.three-act-structure-for-games
name: three-act-structure-for-games
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, three-act-structure, heros-journey, story-structure, narrative-pacing, plot-structure]
level: practitioner
status: draft
description: "Adapt three-act structure and the hero's journey to games: mapping acts to chapters and difficulty, where play replaces scenes, and where the classical model breaks down."
sources:
  - https://en.wikipedia.org/wiki/Three-act_structure
  - https://en.wikipedia.org/wiki/Hero%27s_journey
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three-act structure and the hero's journey for games

**Goal:** a macro-structure that paces story and play together across a 10-60 hour game.

## Three acts mapped to a game
| Act | Share of playtime | Story job | Play job |
|---|---|---|---|
| Act 1 | ~20-25% | ordinary world, inciting incident, commitment | tutorial, core verbs taught |
| Act 2a | ~25% | new world, allies, rising stakes | mechanics combined, map opens |
| Midpoint | | revelation or reversal | new ability or region; difficulty spike |
| Act 2b | ~25% | complications, dark moment | hardest optional content available |
| Act 3 | ~20% | climax, resolution | mastery test, final boss, epilogue |

Schell's interest curve (hook, rising peaks, climax, short resolution) is the same shape
at session and level scale.

## Hero's journey (Campbell / Vogler) checkpoints
Ordinary world, call to adventure, refusal, mentor, crossing the threshold, tests/allies/
enemies, approach to the inmost cave, ordeal, reward, the road back, resurrection, return
with the elixir. Use it as a checklist for missing beats, not a template; many games skip
"refusal" because a refusing player-character fights the player's intent.

## Adapting
1. **Write the beat list first**, then assign each beat to a chapter and a level.
2. **Let play carry the middle:** act 2 is mostly player-driven; place story beats at
   region transitions so open-world freedom does not shred pacing.
3. **Climax = mechanical mastery test.** The final boss should demand the full verb set.
4. **Keep the resolution short**; players stop playing after the credits, so put
   post-game hooks before them if you need them.
5. **Open worlds:** use act structure per main quest line and let side content sit
   between beats; gate the act-3 trigger behind player readiness (a point of no return warning).

## Where it breaks
- Roguelikes and live games are cyclical; use loop structures (run, meta-progress) and
  seasonal arcs instead.
- Emergent / sandbox games use the player's story; supply prompts, not acts.

## Verify
- [ ] Beat list mapped to chapters with approximate playtime share.
- [ ] Midpoint has both a story reversal and a mechanical change.
- [ ] Final act tests the full verb set.
