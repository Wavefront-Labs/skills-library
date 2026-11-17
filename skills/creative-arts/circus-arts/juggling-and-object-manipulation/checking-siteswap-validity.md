---
id: creative-arts.circus-arts.juggling-and-object-manipulation.checking-siteswap-validity
name: checking-siteswap-validity
category: creative-arts
field: circus-arts
product: juggling-and-object-manipulation
tags: [juggling-and-object-manipulation, circus-arts, siteswap, siteswap-notation, vanilla-siteswap, siteswap-validity, average-theorem, juggling-notation, juggling-patterns]
level: practitioner
status: verified
description: "Read vanilla siteswap and test whether a sequence is jugglable: the average theorem for ball count, the landing-time collision test, and worked examples like 441, 531 and 5551."
sources: ["Siteswap notation (invented by Paul Klimek 1981, developed by Tiemann, Hamkins and Magnusson 1985) - https://en.wikipedia.org/wiki/Siteswap", "Polster, The Mathematics of Juggling (2003)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checking siteswap validity

**Goal:** given a vanilla (asynchronous, one-object-per-throw) siteswap, know how many
objects it needs and whether it can be juggled at all.

## What the numbers mean
Each digit is a throw on a beat, hands alternating R, L, R, L. The number is how many
beats later the object is thrown again. Odd numbers cross to the other hand, even
numbers return to the same hand. 0 = empty hand, 2 = hold, 1 = quick hand-to-hand pass.
`3` = three-ball cascade, `4` = four-ball fountain, `441`, `531` are three-ball tricks.

## Test 1: average theorem
Number of objects = sum of digits / number of digits. Must be a whole number.
- 441: (4+4+1)/3 = 3 objects. OK.
- 531: 9/3 = 3. OK.
- 54: 9/2 = 4.5 - not valid.
A whole-number average is necessary but not sufficient.

## Test 2: no two objects land on the same beat
For a sequence of length n, compute (i + t_i) mod n for each position i (starting at 0)
and throw t_i. All results must be different.
- 441: (0+4)%3=1, (1+4)%3=2, (2+1)%3=0 -> {1,2,0} all different. Valid.
- 432: (0+4)%3=1, (1+3)%3=1 -> collision. Invalid (even though the average is 3).
- 5551: (0+5)%4=1, (1+5)%4=2, (2+5)%4=3, (3+1)%4=0 -> valid, 4 objects.

## Using it in practice
- Sanity-check tricks you read about; many forum typos are invalid.
- Generate variations: swap two adjacent throws' landing times (site swap) to create new
  valid patterns from old ones - adjacent throws a, b become b+1, a-1, so 33 -> 42
  (two-in-one-hand with holds) and 531 -> 441 - then check.
- Learning a trick: juggle it slowly saying the numbers aloud.

## Checked
Every pattern in this skill (3, 4, 441, 531, 54, 432, 5551, 51, 52, 744, 33, 42) was run through the average and landing-time tests in a script on 2026-10-18; the throw meanings (0 empty, 1 quick pass, 2 hold, odd crosses, even stays) and the invention history match the Wikipedia siteswap article. The Juggling Information Service page could not be reached from the review network and was removed from sources.

## Gotchas
- Vanilla siteswap assumes one object per hand per beat; multiplex and synchronous
  patterns use extended notation.
- Siteswap describes timing, not throw style (behind the back, under the leg).

## Verify
- [ ] You can show by both tests that 51 is valid with 3 balls and 52 is not valid.
- [ ] You can name the ball count of 744 (5).
