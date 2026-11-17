---
id: creative-arts.circus-arts.juggling-and-object-manipulation.finding-transitions-between-siteswap-patterns
name: finding-transitions-between-siteswap-patterns
category: creative-arts
field: circus-arts
product: juggling-and-object-manipulation
tags: [juggling-and-object-manipulation, circus-arts, siteswap-notation, siteswap-transitions, state-diagram, juggling-states, juggling-patterns, excited-state]
level: advanced
status: draft
description: "Use juggling states (which future beats have objects landing) to find transitions between siteswaps, including ground-state vs excited-state patterns, with worked 3-ball examples."
sources: ["Siteswap notation and state diagrams - https://en.wikipedia.org/wiki/Siteswap", "Polster, The Mathematics of Juggling (2003)", "Juggling Lab transition finder - https://jugglinglab.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finding transitions between siteswap patterns

**Goal:** move from one pattern to another mid-juggle, choosing the throws that get you
there.

## States
A **state** lists, for the next few beats, whether an object is due to land (x) or not
(-). With 3 objects and max throw 5, the cascade's state is `xxx--`: objects land on
each of the next three beats.
- On each beat, the leftmost symbol shifts out. If it was x, you must throw that object
  to an empty future slot (throw value t lands t beats ahead).
- **Ground state**: all objects land as soon as possible (`xxx--`). The cascade, 441,
  531, 423 and 4413 pass through this state, so you can enter them directly from a
  cascade.
- **Excited state**: a pattern that never passes through `xxx--`. The 3-ball shower `51`
  is the classic example: its states are `xx-x-` (before the 5) and `x-x-x` (before
  the 1).

## Finding a transition
1. Write the current state.
2. Write the target pattern's state at its entry point.
3. Pick throws that move the current state to the target, one beat at a time.
Example, cascade to shower: from `xxx--`, throw a **4**. The object due now lands 4 beats
later, giving `xx-x-` - exactly the shower's state before a 5. So juggle `...3 3 4`
then `5 1 5 1 ...`. Find the exit back to the cascade the same way (from a shower state,
choose throws that refill the gaps until you reach `xxx--`).

## Tools
Juggling Lab's transition generator computes transitions automatically; work a few by
hand first so you can do it in your head mid-routine.

## Gotchas
- Some patterns need more than one transition throw.
- The exit back to the cascade is just as important as the entry.

## Verify
- [ ] You can show that 441 can be entered directly from the cascade.
- [ ] You can find an entry throw into a simple excited-state pattern by hand.
