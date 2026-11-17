---
id: creative-arts.game-design.level-design.secrets-and-optional-content
name: secrets-and-optional-content
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, secret-design, optional-content, exploration, collectibles]
level: practitioner
status: draft
description: "Design secrets and optional content that reward curiosity: hint grammar, placement off the critical path, reward value, discovery rates and completionist support."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.gamedeveloper.com/design/the-art-of-the-secret
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secrets and optional content

**Goal:** the curious player feels clever and rewarded; the player on the critical path
never feels punished for missing it.

## Hint grammar
Teach a consistent vocabulary of "something is here": cracked walls, an odd texture,
an unreachable ledge visible from the path, a draft or sound, a gap in the minimap.
Use the same tells everywhere.

## Placement
1. Off the critical path but **visible from it** (the "see it, work out how to reach it" secret).
2. Behind a mechanic learned earlier (backtracking with new abilities).
3. Layered: easy (a side room), medium (a puzzle), hard (a hidden route).
4. Map them on the level plan with their tell and reward.

## Rewards
- Value proportional to effort; never mandatory for completion.
- Types: resources, cosmetics, lore, upgrades (small), shortcuts, Easter eggs.
- Avoid locking key story beats behind secrets.

## Measure
Telemetry or playtests for discovery rate per secret. Aim for a spread (some found by
most players, a few by very few). Zero-discovery secrets need a better tell.

## Completionist support
Counters per area, collectible maps after completion, items that reveal secrets.

## Gotchas
- Invisible walls that break the hint grammar teach players to wall-hump everything.
- Secrets that require exploiting physics often get patched or feel unintended.
- Mandatory "optional" upgrades make the game harder for those who missed them.

## Verify
- [ ] Each secret has a tell and a reward logged.
- [ ] Discovery rates measured.
- [ ] No critical progression behind a secret.
