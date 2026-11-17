---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.tractor-implement-matching
name: tractor-implement-matching
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, tractor-implement-matching, machinery-selection, field-capacity, field-efficiency, implement-draft, draft-equation, drawbar-power, pto-power, tractive-efficiency, wheel-slip, ballast, ballasting, timeliness, asabe-d497, asabe-ep496, asae, tillage, disk-harrow, chisel-plough, chisel-plow, planter, sprayer, farm-machinery-management, agricultural-machinery, tractor-sizing]
level: practitioner
status: gated
description: "Size an implement and tractor together: required field capacity from the work window, implement draft by ASABE D497, drawbar-to-PTO power, ballast and slip targets, with a worked example."
sources:
  - "ASABE D497 Agricultural Machinery Management Data (current edition)"
  - "ASABE EP496 Agricultural Machinery Management"
  - "Hunt & Wilson, Farm Power and Machinery Management"
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tractor-implement matching — capacity first, then draft, then power

**Goal:** choose an implement width and a tractor that finish the job inside its
agronomic window, without over- or under-loading the tractor.

## 1. Required field capacity from the work window
`C_req (ha/h) = Area / (Days in window × Hours per day × P_workable)`

`P_workable` is the probability a day is fit for fieldwork (soil moisture, rain); use
local agronomy data or ASABE EP496/D497 regional tables. Typical 0.5–0.75 in spring (gated: unconfirmed, source is paywalled or blocked).

## 2. Effective field capacity and width
`C (ha/h) = S × w × E_f / 10`  (S in km/h, w in m, E_f as a fraction)

Rearranged: `w = 10 × C_req / (S × E_f)`. Typical D497 field-efficiency ranges (table values (gated: unconfirmed, source is paywalled or blocked)):

| Operation | Field efficiency E_f |
|---|---|
| Mouldboard plough | 0.70–0.90 |
| Chisel plough | 0.70–0.90 |
| Tandem disk harrow | 0.70–0.90 |
| Row-crop planter | 0.50–0.75 |
| Boom sprayer | 0.50–0.80 |
| Combine (grain) | 0.65–0.80 |

E_f falls with small or irregular fields, short rows, refills and unloading; measure
your own from logged data where possible.

## 3. Implement draft (ASABE D497 form)
`D = F_i × [A + B·S + C·S²] × W × T`

- D in N; S in km/h; W = width in m, or number of rows/tools, per the table's unit.
- T = tillage depth in cm for tillage tools; T = 1 for seeding and minor tools.
- F_i = soil texture factor (i = 1 fine, 2 medium, 3 coarse).
- A, B, C are machine-specific. Representative entries (ASABE D497 is paywalled (gated: unconfirmed, source is paywalled or blocked); verify against the current
  D497 table before relying on them): mouldboard plough A = 652, B = 0, C = 5.1 per
  m per cm; tandem disk (primary) A = 309, B = 16, C = 0 per m per cm, F = 1.0/0.88/0.78.
- The standard quotes a **range of ±25–50 %** per machine. Design for the high side
  where the tractor must not stall.

Add PTO and hydraulic power demands separately from drawbar power.

## 4. From draft to tractor rating
`P_db (kW) = D (kN) × S (km/h) / 3.6`

Convert to PTO power with the drawbar/PTO ratio, which depends on drive and soil:

| Tractor | Firm soil | Tilled | Soft/sandy |
|---|---|---|---|
| 2WD | ~0.72 | ~0.67 | ~0.55 |
| MFWD (front assist) | ~0.77 | ~0.73 | ~0.65 |
| 4WD | ~0.78 | ~0.75 | ~0.70 |
| Tracks | ~0.80 | ~0.78 | ~0.75 |

Values are D497-style averages (gated: unconfirmed, source is paywalled or blocked); check the edition in use. Size so the **continuous
load is about 80–85 % of rated PTO power**, leaving reserve for hard spots and slopes.

## 5. Worked example
400 ha to disk in a 15-day window, 10 h/day, P_workable 0.6 → 90 h → C_req = 4.4 ha/h.
At 8 km/h and E_f 0.8: w = 44/6.4 = 6.9 m → choose a 7.3 m disk.
Draft, medium soil, 10 cm deep: 0.88 × (309 + 16·8) × 7.3 × 10 ≈ 28 kN.
P_db = 28 × 8 / 3.6 ≈ 62 kW. MFWD on tilled soil: 62 / 0.73 ≈ 85 kW PTO.
At 80 % loading → a tractor of about 105–110 kW rated PTO power. (Worked example arithmetic recomputed: 4.44 ha/h, 6.94 m, 28.1 kN, 62.4 kW drawbar, 85.5 kW PTO, 107 kW rated.)

## 6. Ballast and slip
- Target wheel slip about **8–12 % on firm soil and 11–15 % on tilled soil** (gated: unconfirmed, source is paywalled or blocked), where
  tractive efficiency peaks. Below ~5 % means over-ballasted (rolling resistance,
  compaction); above ~15–20 % means under-ballasted.
- Ballast in kg per kW is given by each manufacturer and rises as speed falls;
  follow the operator's manual rather than a generic number.
- Keep at least ~20 % of total tractor weight on the front axle with a mounted
  implement raised, or steering and braking become unsafe; add front weights.

## Gotchas
- **Speed is not free.** Draft rises with speed (B and C terms); a disk at 11 km/h
  needs much more power than one at 8. Recheck draft whenever you change speed.
- **3-point hitch lift capacity** and tyre load ratings, not engine power, often limit
  mounted implements. Check lift at 610 mm behind the lift points (vendor rating).
- D497 drafts are averages; wet clay or heavy residue can exceed the quoted range.

## Verify
- [ ] Required capacity is calculated from area, window length and workable-day probability.
- [ ] Implement width gives C ≥ C_req at a realistic speed and field efficiency.
- [ ] Draft uses the correct soil factor, depth and width units for that machine row.
- [ ] Tractor PTO rating gives about 15–20 % reserve over the calculated continuous load.
- [ ] Slip measured in the field falls in the target band after ballasting.
- [ ] Front-axle load and hitch lift capacity are checked with the implement raised.
