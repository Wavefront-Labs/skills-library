---
id: creative-arts.game-design.systems-and-mechanics.paper-prototyping-a-digital-game
name: paper-prototyping-a-digital-game
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, digital-paper-prototype, game-prototyping, prototype-iteration, paper-prototyping, low-fidelity, fullerton, rapid-iteration, video-games]
level: practitioner
status: draft
description: "Paper-prototype a digital game's systems: map real-time rules to turns, a human 'computer' runs the rules, test decisions and economy in an hour before writing code."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Paper prototyping a digital game

**Goal:** test a digital game's rules, decisions and economy with paper, cards and a
human playing the computer, so you find broken systems in hours instead of sprints.

Fullerton (Game Design Workshop ch7) and Schell (2nd ed.) ch8 both recommend physical prototypes
for digital games: they are fast to change mid-session and expose the rules because
someone has to execute them by hand.

## What paper can and cannot test
| Good for | Bad for |
|---|---|
| economy, progression, card/ability balance | twitch feel, timing, aiming |
| turn structure, information flow | physics, camera |
| level layout and routes (top-down map) | moment-to-moment game feel |
| UI information hierarchy (paper screens) | animation readability |
Real-time games: convert to turns ("each turn = 1 second") or use a sand-timer so
the *decisions* are tested even if the *feel* is not.

## Procedure
1. **Pick the question** the prototype answers (see
   `creative-arts.game-design.systems-and-mechanics.risk-driven-prototypes`).
2. **Model state physically:** index cards for entities with stats, tokens for
   resources, a grid or map, a whiteboard for global variables.
3. **Assign a "computer"** (a person) who applies enemy AI rules, spawns, random rolls,
   and hidden information. Give them a written rule sheet; their confusion reveals
   ambiguous rules.
4. **Use dice or a card deck for randomness** that mirrors the planned distribution.
5. **Play, and change rules mid-session** when something breaks; note each change.
6. **Record** decisions players agonised over (good) and decisions they never thought
   about (no real choice).

## Paper UI prototypes
Sketch screens on paper; the facilitator swaps sheets as the tester "taps". Tests
whether the player can find and understand information before UI art exists.

## Gotchas
- Do not simulate everything; abstract what is not under test.
- Paper hides computation cost: a rule the computer applies easily might be expensive or
  unreadable in-game. Flag rules the human struggled with.
- People are kinder to paper; expect harsher reactions when it is digital.

## Verify
- [ ] Prototype answers a stated question.
- [ ] A complete session played with written rule changes logged.
- [ ] Decision for the digital build recorded (keep, change, drop).
