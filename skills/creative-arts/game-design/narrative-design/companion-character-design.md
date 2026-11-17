---
id: creative-arts.game-design.narrative-design.companion-character-design
name: companion-character-design
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, companion-design, game-characters, npc-companions, ai-companions, relationship-systems, approval, character-writing]
level: advanced
status: draft
description: "Design companion characters players care about: gameplay usefulness, personality through barks and reactions, relationship systems, avoiding escort frustration."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Companion character design

**Goal:** companions who are helpful, characterful and emotionally meaningful, never a
burden the player wants to leave behind.

Schell (2nd ed.) ch20 (Worlds Contain Characters) discusses making characters players care about:
clear wants and needs, distinctive voice, and reactions to the player.

## Gameplay first
- **Useful, not essential:** companions help (spot enemies, heal, open paths) without
  being required for basic play.
- **Never a liability:** no friendly fire deaths, no blocking doorways, can't trigger
  fail states through dumb AI (or are invulnerable/stealthed in stealth sections).
- **Readable intent:** the companion's actions are visible and explained.

## Character through systems
1. **Reactive barks** to player actions and world events (see
   `creative-arts.game-design.narrative-design.writing-barks`): they notice what you do.
2. **Opinions:** approval/disapproval of choices, shown in dialogue and behaviour.
3. **Personal arc:** a companion quest or arc that resolves over the game.
4. **Downtime conversations** in safe spaces, optional and short.
5. **Physical presence:** idle animations, looking at points of interest, reacting to
   weather.

## Relationship systems (if used)
- Approval values per companion, changed by choices; thresholds unlock content.
- Show feedback when approval changes (subtly or explicitly).
- Avoid "gift spam" optimisation; tie approval to meaningful choices.

## Gotchas
- Escort missions with fragile companions are a well-known frustration; give them
  self-preservation or durability.
- Companions who comment too often become annoying; set cooldowns and quieter modes.
- Writing a reactive companion multiplies content (choices x companions); scope early.

## Verify
- [ ] Companion can't fail the player through AI behaviour.
- [ ] Reactive bark list covers major player actions and events.
- [ ] Personal arc outlined with beats.
- [ ] Playtesters describe the companion's personality in their own words.
