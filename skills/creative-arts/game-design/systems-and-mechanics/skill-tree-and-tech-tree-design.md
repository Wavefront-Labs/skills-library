---
id: creative-arts.game-design.systems-and-mechanics.skill-tree-and-tech-tree-design
name: skill-tree-and-tech-tree-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, skill-tree, tech-tree, talent-tree, progression-systems, builds, respec, prerequisites, character-progression, 4x-games]
level: practitioner
status: draft
description: "Design skill and tech trees: node types, prerequisites, branching vs web layouts, build diversity, respec rules, and the dead-node and must-pick problems."
sources:
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Skill tree and tech tree design

**Goal:** a progression tree where each point spent is a decision, builds are distinct,
and no node is either mandatory or worthless.

## Node types
| Type | Example | Notes |
|---|---|---|
| Stat increment | +5% damage | filler; boring alone, fine as connective tissue |
| New ability / verb | unlock dash | most exciting; changes play |
| Modifier of an ability | dash leaves fire | creates build identity |
| Keystone (trade-off) | double damage, no healing | strongest build-definers |
| Gate / capstone | tier-5 ultimate | long-term goal |

## Layouts
- **Linear branches** (classic class trees): clear, few builds.
- **Branching with tiers** (choose 1 of 3 per tier): every tier is a decision; easy to
  balance per tier.
- **Web / constellation** (large passive webs): huge build space, hard to read; needs
  search, planners and presets.
- **Tech tree** (strategy games): prerequisites model history or logic; the shape sets
  the pace of unlocks and the eras of the game.

## Procedure
1. Decide the **number of points a player will have** at each stage vs total nodes.
   Choice needs scarcity: if the player can buy 80% of nodes, there are no builds.
2. Group nodes by **build archetype** (3-5) and make sure each archetype has a
   coherent path with its keystone.
3. **Prerequisites:** use them to pace power and teach, not to force tax nodes. Tax
   nodes (mandatory boring nodes before the good one) are the most hated pattern.
4. **Balance per tier:** within a choice set, options should be best in different
   situations (see `creative-arts.game-design.systems-and-mechanics.finding-dominant-strategies`).
5. **Respec rules:** free/cheap respec encourages experimentation; costly respec
   increases commitment. Most modern designs lean toward cheap respec, at least early.
6. **Readability:** show what a node does in concrete numbers and preview the build.

## Gotchas
- **Must-pick nodes** (everyone takes them) are not choices: fold them into baseline.
- **Dead nodes** (no one takes them) are wasted content: buff, merge or cut.
- Pick-rate telemetry per node reveals both problems quickly.
- Tech trees with one obvious rush path collapse strategy; add parallel routes to
  victory.

## Verify
- [ ] Points available vs nodes ratio forces choices.
- [ ] 3+ distinct archetypes each with a coherent path.
- [ ] No mandatory tax nodes without a reason.
- [ ] Node pick rates (playtest or telemetry) have no 95%+ or near-0% nodes.
