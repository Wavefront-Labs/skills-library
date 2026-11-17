---
id: mathematics.numeracy-and-mental-calculation.abacus.soroban-four-operations-and-anzan
name: soroban-four-operations-and-anzan
category: mathematics
field: numeracy-and-mental-calculation
product: abacus
tags: [numeracy-and-mental-calculation, abacus, soroban, japanese-abacus, suanpan, anzan, mental-abacus, flash-anzan, heaven-bead, earth-beads, unit-rod, complement-of-5, complement-of-10, friends-of-5, friends-of-10, fingering, addition, subtraction, multiplication, division, abacus-training, mental-calculation]
level: practitioner
status: draft
description: "Calculate on a soroban: bead values and fingering, complements of 5 and 10 for addition and subtraction, the standard multiplication and division layouts, and building anzan mental-abacus skill."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Soroban: the four operations and anzan

**Goal:** use the Japanese abacus (soroban, 1 heaven bead + 4 earth beads per rod) for
fast, accurate arithmetic, and progress to **anzan** — calculating on an imagined abacus.

## 1. Setup and bead values
- Lay the soroban flat, beam horizontal. Each rod is a digit; the bead above the beam is
  **5**, each of the four below is **1**. A bead "counts" when pushed **toward the beam**.
- **Clear** it: tilt toward you so earth beads drop, lay flat, then run your index finger
  along the beam to push all heaven beads up.
- Pick a **unit rod** marked with a dot (dots usually appear every third rod) as the ones
  place; everything aligns from there.
- **Fingering (standard Japanese):** thumb pushes earth beads **up**; index finger pushes
  earth beads **down** and moves heaven beads both ways. Keep it consistent from day one.

## 2. Addition: direct, then complements
Work **left to right** (largest place first), unlike paper arithmetic.
- **Direct:** if the beads are available, push them. 3 + 1: add one earth bead.
- **Complement of 5** ("friends of 5": 1+4, 2+3): to add n when earth beads run out, add 5
  and subtract (5 − n). 4 + 3: no room for 3 earth beads → push heaven (5), remove 2 earth → 7.
- **Complement of 10** ("friends of 10": 1+9, 2+8, 3+7, 4+6, 5+5): to add n when the rod
  can't take it, subtract (10 − n) on this rod and add 1 to the rod on the left.
  8 + 7: subtract 3 (→ 5), add 1 to tens → 15.
- **Combined** (5 and 10 together): 6 + 6 → rod needs −4 then +10; −4 on a 6 isn't direct,
  so: subtract 4 = remove the 5 and add 1 → 2, then carry 1 → 12.
Example: 47 + 38 (left to right): tens 4 + 3 = 7; ones 7 + 8 → −2 on ones (5) and +1 on
tens (8) → **85**.

## 3. Subtraction: the mirror
- Direct removal when beads are there.
- **Complement of 5:** to subtract n without enough earth beads, add (5 − n) and remove the 5.
  7 − 3: 7 is heaven + 2 earth, so 3 earth beads aren't there → add 2 earth beads, then
  remove the heaven bead → **4**.
- **Complement of 10:** borrow: subtract 1 from the left rod, add (10 − n) on this rod.
  12 − 5: tens −1, ones +5 → **7**.

## 4. Multiplication (standard modern layout)
Place the **multiplicand** at the right-middle, the **multiplier** at the far left, leaving
empty rods between. Multiply digit by digit using the times tables, adding each partial
product to the answer rods with addition technique, shifting one rod per place.
Example 23 × 4: 4 × 3 = 12 on the rightmost answer rods, 4 × 2 = 8 one place left
(added) → **92**. Uncertain: placement rules differ between Japanese abacus federations and
teaching books — follow one consistently.

## 5. Division
Set the **dividend** on the right-middle, **divisor** at the left. Working from the left,
estimate each quotient digit, place it to the left of the current dividend portion
(standard rule: one rod left if the divisor's first digit ≤ the dividend's first digits,
two rods if not), then subtract quotient × divisor from the dividend with subtraction
technique. If the remainder is still ≥ divisor, raise the quotient digit (and subtract
again); if you can't subtract, lower it and add back.
Example 96 ÷ 4: quotient digit 2 (4 × 2 = 8 from 9 → 1); bring in 16, quotient 4 → **24**.
Uncertain: the one-rod/two-rod placement rule is the common modern Japanese method as
best understood; older texts use a division-table method instead.

## 6. Anzan (mental abacus)
1. Fluent physical soroban first — complements must be automatic.
2. **Shadow:** move fingers in the air over an imagined abacus while calculating.
3. Visualise 1–3 rods, then more; practise **dictated sums** (listen and add) and
   **flash anzan** (numbers flashed on screen).
4. Increase digits before speed, in short daily sessions (10–20 minutes is common
   teaching practice; the evidence for exact dosing is limited). Graded kyu/dan exams
   from abacus associations give a progression ladder.

## Gotchas
- Mixing fingering (using index to push up earth beads) caps speed later.
- Losing track of the unit rod gives answers off by powers of ten.

## Verify
- [ ] Soroban cleared and unit rod chosen before each problem.
- [ ] All 5- and 10-complements for addition and subtraction done without pausing.
- [ ] 47 + 38, 12 − 5, 23 × 4 and 96 ÷ 4 produce 85, 7, 92, 24.
- [ ] Anzan: a 5-number, 2-digit dictated sum done mentally and confirmed.
