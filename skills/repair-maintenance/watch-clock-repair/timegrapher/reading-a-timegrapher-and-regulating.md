---
id: repair-maintenance.watch-clock-repair.timegrapher.reading-a-timegrapher-and-regulating
name: reading-a-timegrapher-and-regulating
category: repair-maintenance
field: watch-clock-repair
product: timegrapher
tags: [timegrapher, watch-repair, watchmaking, horology, rate, amplitude, beat-error, lift-angle, beat-rate, bph, 28800-bph, 21600-bph, positional-timing, dial-up, crown-down, regulation, index-regulator, swan-neck, free-sprung-balance, hairspring, trace-diagnosis, weishi-1000, witschi, mechanical-watch]
level: practitioner
status: draft
description: "Use a timegrapher on a mechanical watch: set lift angle and beat rate, read rate, amplitude and beat error across positions, diagnose from the trace, and regulate and correct beat error."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading a timegrapher and regulating

**Goal:** measure a mechanical watch's health in a minute, decide whether it needs
regulation or a service, and adjust rate and beat error correctly.

> Draft: menus differ by machine (Weishi 1000/1900, Witschi, Chronoscope etc.).
> Target figures are common workshop expectations, not a standard — chronometer
> (COSC) limits are stricter and defined per test protocol.

## 1. Set up
- **Lift angle:** the balance's angle of contact with the pallet fork. Most Swiss
  movements **52°** (ETA 2824, Sellita); many Japanese/older Swiss differ (e.g. some
  Seiko calibres ~53°, Omega 8500 family higher, some Rolex ~52°). **Wrong lift
  angle = wrong amplitude** (not wrong rate). Look up the calibre.
- **Beat rate:** auto-detect usually works; check manually: 18,000 / 21,600 / 25,200 /
  28,800 / 36,000 bph (2.5 / 3 / 3.5 / 4 / 5 Hz).
- **Wind fully** (or after 30–40 turns) and let run ~10–20 min. Reading a watch at
  low power reserve shows low amplitude that is "normal" for that state.
- Microphone stand in a quiet place; clamp watch firmly but gently.
- Sample period ≥ 10–20 s per position.

## 2. Read the numbers
- **Rate** (s/day): + fast, − slow. A healthy serviced watch: within roughly ±10 s/d
  in dial up, less spread better.
- **Amplitude** (degrees of balance swing):
  - Dial up/down (horizontal): **~270–310°** healthy; < 220° worrying.
  - Vertical positions typically **~30–50° lower** than horizontal.
  - Low amplitude = dirty/dry movement, weak mainspring, friction, or wrong lift angle.
  - Very high (> 320°) risk of **knocking** (banking: impulse pin hitting the outside
    of the fork horns) — rate jumps fast in one position.
- **Beat error** (ms): asymmetry of tick vs tock. **< 0.5 ms** good, < 1.0 acceptable
  for most watches; > 1.5–2 ms affects starting and isochronism.

## 3. Positional test (six-position or a quick four)
Test: dial up (DU), dial down (DD), crown down (CD), crown left (CL), crown up (CU),
crown right (CR) — common quick check: DU, DD, CD, CL. Record rate and amplitude each.
- **Delta** (max − min rate) shows how well poised the balance is and how clean
  the pivots are. Serviced good-grade watch: delta ~10–20 s/d; poor: > 30.
- DU vs DD big difference = pivot/jewel issue (damaged pivot, dirty cap jewel, end-shake).
- Vertical positions with big spread = poise problem (balance out of balance) or
  hairspring off-centre.

## 4. Read the trace (pattern)
- Two straight parallel lines: good. Slope up = fast, down = slow.
- Lines separated = beat error.
- **Wavy lines with a regular period** = something rotating is out of round/
  catching: period ~ every 60 s = escape wheel/fourth wheel issue (often seconds-wheel);
  shorter periods = escape wheel tooth damage.
- Scattered, noisy dots = dirty, worn pivots, magnetised hairspring, or poor mic contact.
- Lines that wander after a few minutes in one position = hairspring coils touching
  (magnetism) — check with a demagnetiser first.

## 5. Regulate
1. **Demagnetise** first if rate is wildly fast (+100 s/d or more) — a classic sign.
2. **Beat error:** on most index-regulated movements, rotate the **stud carrier**
   (movable stud) slightly with a fine tool while watching the reading; aim < 0.3 ms.
   Fixed-stud movements need the balance removed and the collet rotated — skilled job.
3. **Rate:** move the **index regulator** (+/− marks) toward + to speed up. Tiny
   movements; a swan-neck regulator uses its fine-adjust screw. Free-sprung balances
   (Rolex Microstella, Omega/Patek-type) adjust with weighted screws/nuts on the balance
   — follow the calibre's procedure.
4. Regulate in the average of the positions the owner uses (usually aim slightly
   fast: +2 to +5 s/d DU, so the averaged on-wrist rate ends near zero to slightly fast).
5. Recheck after 10 min.

## Gotchas
- Don't regulate a watch with low amplitude — service it instead; rate will drift.
- Wrong lift angle makes healthy watches look sick (or vice versa).
- A watch tested at 10% power reserve vs full wind gives different results; record when.
- Overturning the regulator can push the hairspring out of the regulator pins.

## Verify
- [ ] Correct lift angle and beat rate set; watch fully wound.
- [ ] Rate, amplitude and beat error recorded in at least 4 positions.
- [ ] Trace pattern checked for periodic faults and noise.
- [ ] Demagnetised before regulating if rate abnormal.
- [ ] Final: beat error < ~0.5 ms, positional delta acceptable, average rate slightly positive.
