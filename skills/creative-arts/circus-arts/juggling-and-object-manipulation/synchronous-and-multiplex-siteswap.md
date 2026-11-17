---
id: creative-arts.circus-arts.juggling-and-object-manipulation.synchronous-and-multiplex-siteswap
name: synchronous-and-multiplex-siteswap
category: creative-arts
field: circus-arts
product: juggling-and-object-manipulation
tags: [juggling-and-object-manipulation, circus-arts, siteswap-notation, synchronous-siteswap, multiplex, sync-notation, juggling-notation, juggling-patterns]
level: advanced
status: draft
description: "Read and write synchronous and multiplex siteswap: (a,b) pairs, x for crossing, square brackets, ball counts, examples like (4,4) and [43]14."
sources: ["Siteswap notation - https://en.wikipedia.org/wiki/Siteswap", "Juggling Information Service siteswap help - https://www.juggling.org/help/siteswap/", "Juggling Lab notation reference - https://jugglinglab.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Synchronous and multiplex siteswap

**Goal:** read and write patterns where hands throw at the same time, or a hand throws
more than one object at once.

## Synchronous notation
- Pairs in parentheses: `(left,right)` throws happen together. Beats count in twos, so
  synchronous patterns use only even numbers.
- `x` after a number means the throw crosses to the other hand: `(4x,4x)` is the
  4-ball synchronous crossing pattern; `(4,4)` is 4 balls in synchronous fountain columns.
- `(4,2x)(2x,4)` = a 3-ball synchronous pattern (the "box"-like shower).
- A `*` at the end means "repeat mirrored": `(4,2x)*` is shorthand for the above.
Ball count = sum of all numbers / number of beats (each pair counts as 2 beats).

## Multiplex notation
- Square brackets: several objects thrown from one hand on the same beat.
- `[33]` throws two balls as 3s together.
- `[43]14` = a well-known 4-ball multiplex trick.
- Synchronous multiplexes combine both: `([44],2)`.

## Validity
Same principle as vanilla: no two objects land in the same hand on the same beat unless
the landing is a deliberate multiplex catch. Use Juggling Lab to check and animate.

## Practice
- Learn `(4,4)` and `(4x,4x)` with 4 balls if you have a 4-ball fountain.
- Learn the box `(4,2x)*` with 3 balls.
- Try `[33]` multiplex splits with 3 balls.

## Verify
- [ ] Correct ball count for `(6x,4)*` (5 balls).
- [ ] You can juggle the box and write its notation.
