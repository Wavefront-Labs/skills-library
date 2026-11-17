---
id: creative-arts.game-design.systems-and-mechanics.avoiding-dark-patterns
name: avoiding-dark-patterns
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, dark-patterns, transformational-games, serious-games, ethics, player-wellbeing, monetization-design, manipulation, consumer-protection]
level: practitioner
status: draft
description: "Audit a game for dark patterns (temporal, monetary, social, psychological) using Zagal, Bjork and Lewis's taxonomy, and redesign them into respectful alternatives."
sources:
  - http://www.fdg2013.org/program/papers/paper06_zagal_etal.pdf
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding dark patterns

**Goal:** find design choices that work against players' interests and replace them,
protecting players and the game's long-term reputation.

Zagal, Björk and Lewis ("Dark Patterns in the Design of Games", FDG 2013) define a dark
game design pattern as one used intentionally by a game creator to cause negative
experiences for players against their best interests and likely without their consent.
They group examples into **temporal**, **monetary** and **social capital-based**
patterns. Schell (2nd ed.) ch33 (Designers Have Certain Responsibilities) argues designers are
responsible for what their games do to players.

## Audit checklist
| Category | Pattern (examples) | Respectful alternative |
|---|---|---|
| Temporal | grinding as padding; playing by appointment with punishment | respect time, skip options, no decay |
| Monetary | pay to skip artificial waits; pre-delivered content (dangling locked rewards); obfuscated premium currency | fair prices, real-money equivalents, no manufactured waits |
| Social | social pyramid schemes (invite friends to progress); impersonation (posting as the player) | optional sharing, explicit consent |
| Psychological | FOMO timers; loss aversion via streak resets; near-miss presentation in random rewards; confirmshaming ("No, I don't want to be strong") | calm offers, neutral decline buttons, honest presentation |

## Procedure
1. List every prompt, timer, offer and social mechanic in the game.
2. For each, ask: whose interest does it serve? Would the player choose it with full
   information? Does it exploit a known bias?
3. Mark patterns red/amber/green; redesign reds before launch.
4. Check consumer-protection law in target markets (several regulators have published
   guidance on in-game purchases and manipulative design).
5. Re-audit after each live-ops change; dark patterns creep in via offers and events.

## Gotchas
- Metrics can reward dark patterns short-term (conversion, retention); add sentiment,
  refund and complaint metrics to see the cost.
- Children are a protected audience in many jurisdictions; stricter standards apply.
- Not every time-limited event is a dark pattern; what matters is punishment,
  deception and exploitation.

## Verify
- [ ] Every monetisation and retention mechanic audited.
- [ ] No red-rated pattern remains at launch.
- [ ] Decline buttons use neutral language.
- [ ] Sentiment/refund metrics tracked alongside revenue.
