---
id: mathematics.numeracy-and-mental-calculation.speed-calculation-systems.vedic-trachtenberg-and-calendar-shortcuts
name: vedic-trachtenberg-and-calendar-shortcuts
category: mathematics
field: numeracy-and-mental-calculation
product: speed-calculation-systems
tags: [numeracy-and-mental-calculation, speed-calculation-systems, speed-maths, speed-math, vedic-mathematics, vedic-maths, nikhilam, urdhva-tiryagbhyam, vertically-and-crosswise, trachtenberg-system, multiply-by-11, multiply-by-12, squaring-shortcuts, squares-ending-in-5, near-base-multiplication, doomsday-rule, day-of-week-calculation, calendar-calculation, mental-calculation, competition-maths]
level: practitioner
status: draft
description: "Named rapid-calculation shortcuts that actually pay off: squares ending in 5, near-base (Nikhilam) multiplication, vertically-and-crosswise, Trachtenberg ×11/×12, and the Doomsday weekday rule."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vedic, Trachtenberg and calendar shortcuts

**Goal:** learn the handful of named speed-calculation techniques with the best payoff,
know exactly when each applies, and check results so speed doesn't cost accuracy.
(General strategies are in
mathematics.numeracy-and-mental-calculation.mental-arithmetic.mental-multiplication-percentages-and-fractions.)

A note on names: "Vedic mathematics" is a 20th-century system (Bharati Krishna Tirtha,
published 1965) presented through Sanskrit sutras; its techniques are ordinary algebra
in clever form. Trachtenberg's system was developed in the 1940s. Both are useful
tricks, not deeper mathematics.

## 1. Squares of numbers ending in 5
(10a + 5)² = 100·a(a + 1) + 25. Multiply the leading part by its successor, append 25.
- 65² → 6 × 7 = 42 → **4,225**.
- 115² → 11 × 12 = 132 → **13,225**.
Extends to x.5²: 7.5² = 7 × 8 + 0.25 = 56.25.

## 2. Squares near 50
(50 ± d)² = 100·(25 ± d) + d².
- 47² → 25 − 3 = 22, 3² = 09 → **2,209**.
- 53² → 25 + 3 = 28, 09 → **2,809**.
Always write d² as **two digits** (09, not 9).

## 3. Near-base multiplication (Nikhilam)
For numbers close to 10, 100, 1,000:
1. Write each number's difference from the base (deficit negative, surplus positive).
2. Left part: cross-add — either number plus the other's difference.
3. Right part: multiply the differences; it must have as many digits as the base has zeros.
- 97 × 94 (base 100; −3, −6): 97 − 6 = 91; (−3)(−6) = 18 → **9,118**.
- 104 × 107 (+4, +7): 104 + 7 = 111; 4 × 7 = 28 → **11,128**.
- 88 × 97 (−12, −3): 88 − 3 = 85; 12 × 3 = 36 → **8,536**.
- If the right part overflows (e.g. 85 × 85: 70 | 225), carry: 70 + 2 | 25 = **7,225**.
- Mixed signs (103 × 98: 101 | −6) borrow: 10,100 − 6 = **10,094**.
Works poorly when numbers are far from a base — then use section 4.

## 4. Vertically and crosswise (any two-digit × two-digit)
For ab × cd, compute right to left:
1. Units: b × d.
2. Cross: a × d + b × c.
3. Left: a × c.
Carry as usual. 23 × 41: 3 × 1 = 3; 2×1 + 3×4 = 14 → write 4, carry 1; 2×4 + 1 = 9 → **943**.
It's the standard algorithm rearranged so the whole product can be written in one line —
good for paper speed; mentally it needs you to hold carries.

## 5. Trachtenberg ×11 and ×12
- **×11:** write the last digit; then each digit plus its right-hand neighbour, right to
  left, carrying; finally the first digit (plus carry).
  3,425 × 11: 5; 2+5 = 7; 4+2 = 6; 3+4 = 7; 3 → **37,675**.
- **×12:** each digit *doubled* plus its right-hand neighbour.
  3,142 × 12: 2×2 = 4; 4×2 + 2 = 10 (0, carry 1); 1×2 + 4 + 1 = 7; 3×2 + 1 = 7; 3 → **37,704**.
Trachtenberg has rules for every multiplier 3–12; ×11 and ×12 are the ones worth memorising.

## 6. Day of the week: Conway's Doomsday rule
Each year, these dates fall on the same weekday ("doomsday"): 4/4, 6/6, 8/8, 10/10,
12/12, 5/9, 9/5, 7/11, 11/7 (month/day — "9-to-5 at the 7-11"), the last day of February,
and 3 Jan in common years / 4 Jan in leap years.
**Year's doomsday** = century anchor + (y ÷ 12) + (y mod 12) + ((y mod 12) ÷ 4), all integer
division, mod 7. Century anchors: 1900s Wednesday, 2000s Tuesday, 2100s Sunday.
- 2026: y = 26 → 2 + 2 + 0 = 4; Tuesday + 4 = **Saturday**. So 10 Oct 2026 is Saturday and
  14 Oct 2026 is a **Wednesday**.
- 20 Jul 1969: 69 → 5 + 9 + 2 = 16 ≡ 2; Wednesday + 2 = Friday; 11 Jul is Friday → 18th
  Friday → 20th **Sunday**.
(Both verified against a calendar library.)

## Checking
- **Casting out nines:** reduce each factor to its digit sum mod 9, multiply, reduce;
  must match the answer's digit sum mod 9. 97 × 94: 7 × 4 = 28 → 1; 9,118 → 19 → 1 ✓.
- **Estimate:** 104 × 107 ≈ 11,000.

## Gotchas
- Shortcuts have conditions (near a base, ending in 5); forcing them elsewhere is slower
  than plain partitioning.
- Digit-count rule in Nikhilam is the commonest error: 97 × 98 is 95 | 06 = 9,506, not 956.
- Claims that Vedic methods are "ancient" are historically disputed — teach them as tricks.
- Uncertain: century anchors beyond 2199 follow the Gregorian 400-year cycle
  (2200s Friday); check before relying on them.

## Verify
- [ ] 85², 47², 97 × 94 and 104 × 107 done in your head in under 10 s each, correct.
- [ ] Right-hand parts always written with the base's digit count.
- [ ] Today's weekday computed by Doomsday and matches the calendar.
- [ ] Every result cross-checked by casting out nines or an estimate.
