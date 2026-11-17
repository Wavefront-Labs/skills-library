---
id: creative-arts.game-design.systems-and-mechanics.bartle-taxonomy-and-its-limits
name: bartle-taxonomy-and-its-limits
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, bartle-taxonomy, player-types, player-motivation, achievers, explorers, socialisers, killers, mud, mmo-design]
level: intro
status: draft
description: "Use Bartle's player types (achievers, explorers, socialisers, killers) as a design checklist for multiplayer worlds, and know where the model does not apply."
sources:
  - https://mud.co.uk/richard/hcds.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bartle taxonomy and its limits

**Goal:** use Bartle's four player types to check that a shared virtual world offers
something to each kind of player and that the populations stay in a healthy balance,
without misusing it as a universal personality test.

## The model (Bartle 1996, "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs")
Two axes: **acting vs interacting**, and **players vs world**.
| | World | Players |
|---|---|---|
| **Acting on** | Achievers (diamonds): points, levels, goals | Killers (clubs): imposing on others |
| **Interacting with** | Explorers (spades): learning how the world works | Socialisers (hearts): relationships, conversation |
Bartle's key insight is about **dynamics between populations**: e.g. killers prey on
achievers; too many killers drive out achievers and socialisers; socialisers keep
others around. He discusses how changes to one group's numbers affect the others.

## Using it in design
1. For each type, list what the world offers them (achievers: progression, rankings;
   explorers: hidden areas, systems depth; socialisers: chat, guilds, shared spaces;
   killers: PvP, competition with consent).
2. Check the **interactions**: does open PvP let killers grief achievers? Add consent
   zones or penalties (see `creative-arts.game-design.systems-and-mechanics.griefing-and-toxicity-mitigation`).
3. Monitor population health with behaviour data, not surveys alone.

## Limits (know these)
- It was derived from **MUD players** (text multiplayer worlds) in the 1990s. Bartle
  himself has said it was never meant for single-player games.
- The popular online "Bartle test" is not Bartle's own work and is not validated.
- People mix motivations and change over time; types are tendencies, not boxes.
- For broader audiences, use empirically derived models (Quantic Foundry, SDT; see
  `creative-arts.game-design.systems-and-mechanics.player-motivation-models` and
  `creative-arts.game-design.systems-and-mechanics.self-determination-theory-in-games`).
- Bartle later extended it to an 8-type model (implicit/explicit axis) in *Designing
  Virtual Worlds*.

## Verify
- [ ] Each type has listed offerings in the design (for multiplayer worlds).
- [ ] Type interactions (especially killer vs others) have explicit rules.
- [ ] Model not applied to single-player design decisions without other evidence.
