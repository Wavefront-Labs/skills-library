---
id: computing-software.game-programming.game-ai-programming.rts-strategic-ai
name: rts-strategic-ai
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, rts-strategic-ai, strategy-ai, build-orders, game-programming]
level: practitioner
status: draft
description: "Structure RTS strategic AI: layered managers for economy, production and military, build orders, scouting, threat assessment and difficulty without cheating."
sources: ["https://github.com/bwapi/bwapi", "https://github.com/Blizzard/s2client-proto"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RTS strategic AI

**Goal:** a computer opponent that expands, builds an army, scouts, attacks and defends coherently.

## Layered architecture
```text
Strategy (seconds-minutes): choose plan (rush, expand, tech), respond to scouting
  -> Economy manager: workers, expansions, resource ratios
  -> Production manager: build queue from build order + reactive needs
  -> Military manager: squads, attack/defend targets, army composition vs enemy
     -> Tactical/squad AI (unit micro, formations, target fire)
```
Managers communicate through requests and a shared world model; each runs at its own rate.

## Build orders
Script openings as timed or supply-triggered lists ("at 14 supply: barracks"), then switch to
reactive production. Validate requirements (tech tree) and handle loss (rebuild).

## Knowledge
- **Scouting:** send scouts early and periodically; remember enemy buildings with timestamps.
- **Threat assessment:** estimate enemy army value by unit counters; compare with own army to decide
  attack, defend or retreat.
- **Terrain analysis:** chokepoints, expansions, regions (BWTA/BWEM-style analysis) inform defence
  positions and attack paths.
- Influence maps for army presence and safety.

## Difficulty without cheating
Tune reaction time, APM caps, build order quality, scouting frequency and micro precision.
Resource bonuses and map vision are acceptable for top difficulties only if disclosed.

## Research platforms
StarCraft II API (`s2client-proto`, python-sc2 and burnysc2) and BWAPI for Brood War provide test
beds and published bot architectures.

## Verify
- Automated matches between AI versions; win rate and timing benchmarks (time to first expansion,
  army supply at 10 minutes).
