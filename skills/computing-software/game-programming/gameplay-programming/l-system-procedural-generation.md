---
id: computing-software.game-programming.gameplay-programming.l-system-procedural-generation
name: l-system-procedural-generation
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, l-system, procedural-generation, plants, game-programming]
level: practitioner
status: verified
description: "Generate plants, trees and road networks with L-systems: rewriting rules, turtle interpretation, stochastic and parametric rules, and growth limits."
sources: ["http://algorithmicbotany.org/papers/abop/abop.pdf", "https://en.wikipedia.org/wiki/L-system"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# L-systems

**Goal:** grow branching structures (trees, coral, roads, lightning) from a few rewriting rules
(Prusinkiewicz and Lindenmayer, *The Algorithmic Beauty of Plants*).

## Rewriting
```python
rules = {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}
def expand(axiom, n):
    s = axiom
    for _ in range(n): s = "".join(rules.get(c, c) for c in s)
    return s
```
This is the 'fractal plant' from Wikipedia's L-system article (axiom `X` there is `-X`, turn angle 25 degrees, `+` left and `-` right). Run here, the string lengths from axiom `X` are 18, 89, 379, 1551, 6263, 25159 and 100839 characters for 1 to 7 iterations (about x4 per step: exponential growth); 5-7 iterations is typical. Cap string length and stop early.

## Turtle interpretation
- `F` move forward drawing, `f` move without drawing, `+`/`-` turn left/right about the up axis, `&`/`^` pitch down/up,
  `/` and `\` roll right/left (3D; the Algorithmic Beauty of Plants section 1.10.3 defines the parametric forms and its sign conventions), `[` push state, `]` pop state.
- State = position, orientation (3x3 or quaternion), segment length, width. Shrink length/width per
  depth for natural taper.

## Variations
- **Stochastic:** several productions per symbol with probabilities, driven by a seeded RNG so a
  seed reproduces the same tree.
- **Parametric:** `A(l,w) -> F(l)[+A(l*0.7,w*0.6)][-A(l*0.7,w*0.6)]` stores numbers per symbol.
- **Context-sensitive:** rules depend on neighbours, used for signal propagation.
- **Environment-aware:** query collision during interpretation to prune branches hitting walls
  (open L-systems).

## Game use
- Generate offline to meshes and LODs for vegetation; runtime generation suits stylised or
  low-count content.
- Road networks (Parish and Mueller, SIGGRAPH 2001, "Procedural Modeling of Cities", which proposes an approach based on L-systems) use extended L-systems with global goals and
  local constraints.

## Verify
- Same seed yields identical vertex counts; fixed iteration string matches a golden snapshot.
