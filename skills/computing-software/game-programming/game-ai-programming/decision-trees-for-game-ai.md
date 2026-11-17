---
id: computing-software.game-programming.game-ai-programming.decision-trees-for-game-ai
name: decision-trees-for-game-ai
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, decision-tree, decision-making, random-decision-tree, data-driven-ai, behavior-tree, game-ai, game-programming]
level: practitioner
status: verified
description: "Use decision trees for fast NPC choices: tree structure, typed condition nodes, random branches with persistence, data-driven authoring and when to move to BTs or utility AI."
sources: ["https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9781138483972", "https://www.gameaipro.com/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decision trees for game AI

**Goal:** a cheap, readable way to map an NPC's situation to an action, evaluated every tick or
on events (Millington, AI for Games).

## Structure
Internal nodes test one condition; leaves are actions.
```
Enemy visible?
 |- no  -> Heard noise recently?  - yes -> Investigate
 |                                \ no  -> Patrol
 \- yes -> Distance < 3 m?
           |- yes -> Melee attack
           \- no  -> Has ammo? - yes -> Shoot
                               \ no  -> Take cover / reload
```
```python
class Decision:
    def __init__(self, test, yes, no): self.test, self.yes, self.no = test, yes, no
    def decide(self, ctx): return (self.yes if self.test(ctx) else self.no).decide(ctx)
class ActionLeaf:
    def __init__(self, action): self.action = action
    def decide(self, ctx): return self.action
```
Evaluation is O(depth) with no allocation (the tree has one test per level on the path taken).

## Typed decision nodes
- Boolean (flag), float range (`health < 0.3`), multi-way branch on enums (`switch` over weapon
  type) to avoid long chains of binary tests.
- Put the most discriminating and cheapest tests near the root; expensive tests (raycast line of
  sight) deeper, and cache their results per tick in the context.

## Randomness without dithering
A random branch re-evaluated every frame flips between actions. Make random decisions **sticky** (a random A/B pick every frame changed branch 3,023 times in 6,000 frames; with a 60-frame hold, 50 times):
store the chosen branch and keep it until a timeout or until the branch's parent changes.

## Data-driven authoring
Represent trees in data (JSON or editor graph): `{"test":"enemy_visible","yes":{...},"no":{...}}`
with a registry of named condition functions. Designers can edit without code; validate at load
that all named tests/actions exist.

## Limits
- No memory of "what I was doing": transitions happen whenever conditions change, so long actions
  need a state machine or behaviour tree around them.
- Trees grow combinatorially with conditions; duplicated subtrees signal that utility scoring or a
  behaviour tree fits better.
- Learned decision trees (ID3) are possible from recorded play data but rarely used in shipped games.

## Verify
- [ ] Unit tests: each leaf reachable with a crafted context.
- [ ] Debug overlay shows the path taken per NPC per tick.
- [ ] Random branches do not change more often than their configured hold time.

## Checked (2026-10-22)
- Re-implemented the C++ node classes in Python and ran the example tree on crafted contexts: each of the six leaves is reachable and each decision costs one test per level on its path. The sticky-random numbers above are from a 6,000-frame simulation.
- Book chapter number removed (Millington is not available here); 'ID3' is the standard name for the decision tree learning algorithm; the JSON data-driven layout is a design suggestion, not run.
