---
id: creative-arts.game-design.systems-and-mechanics.difficulty-settings-and-assist-modes
name: difficulty-settings-and-assist-modes
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, assist-mode, difficulty-settings, difficulty-design, accessibility, game-speed, invincibility, granular-difficulty, celeste-assist-mode]
level: practitioner
status: draft
description: "Design difficulty modes and granular assist options (game speed, damage taken, aim assist, skip): naming, defaults, changing mid-game, and avoiding shame."
sources:
  - https://gameaccessibilityguidelines.com/
  - https://learn.microsoft.com/en-us/gaming/accessibility/guidelines
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Difficulty settings and assist modes

**Goal:** let a wide range of players experience the game at a challenge level that
suits them, without shaming them and without ruining the intended experience for those
who want it hard.

## Two approaches
- **Preset modes** (Story / Normal / Hard): simple, but bundle many variables.
- **Granular assists** (independent toggles/sliders): e.g. Celeste's Assist Mode offers
  game speed (down to 50%), infinite stamina, extra/infinite dashes and invincibility,
  presented with a respectful note about the intended experience.
Many modern games offer both: presets as starting points, granular options to tune.

## Common levers
| Lever | Helps with |
|---|---|
| Game speed / slow motion | reaction time, motor impairments |
| Damage taken / dealt multipliers | general challenge |
| Aim assist strength, auto-aim | motor precision |
| Timing windows (parry, QTE) | reaction time |
| Puzzle hints / skip | cognitive load, stuck points |
| Skip combat / encounters | story-focused players |
| Navigation aids | orientation, cognitive |

## Procedure
1. List the **skill demands** of the game (reaction, precision, memory, puzzle-solving,
   endurance). Each needs at least one lever.
2. **Naming:** describe what a mode does, not who it is for ("Fewer enemies, more
   healing" rather than "Baby mode"). Avoid mocking text.
3. **Default and first-run choice:** ask at start with clear descriptions; let players
   change any time without restarting, unless there is a strong design reason.
4. **Achievement policy:** decide whether assists affect achievements and say so up front.
5. **Accessibility guidelines:** Game Accessibility Guidelines and Xbox Accessibility
   Guidelines both include difficulty-related items (e.g. allowing difficulty to be
   adjusted during play); review them.

## Gotchas
- A "Hard" mode that only inflates enemy HP is tedium, not challenge; change behaviour.
- Locking difficulty after selection punishes players who misjudged at the start.
- Assist options buried in menus are unused; surface them after repeated failure, with
  a dismissable prompt.

## Verify
- [ ] Each skill demand has a lever.
- [ ] Mode names describe effects; no shaming copy.
- [ ] Difficulty changeable mid-game (or reason documented).
- [ ] Achievement interaction stated in the menu.
