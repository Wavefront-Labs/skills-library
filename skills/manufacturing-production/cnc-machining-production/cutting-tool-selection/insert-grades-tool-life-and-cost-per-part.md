---
id: manufacturing-production.cnc-machining-production.cutting-tool-selection.insert-grades-tool-life-and-cost-per-part
name: insert-grades-tool-life-and-cost-per-part
category: manufacturing-production
field: cnc-machining-production
product: cutting-tool-selection
tags: [cutting-tool-selection, cutting-tools, carbide-inserts, insert-grade, iso-513, iso-p, iso-m, iso-k, iso-n, iso-s, iso-h, insert-geometry, chip-breaker, nose-radius, iso-1832, cvd-coating, pvd-coating, cermet, cbn, pcd, solid-carbide, end-mill, tool-life, taylor-equation, tool-wear, flank-wear, crater-wear, built-up-edge, notch-wear, coolant-strategy, mql, cost-per-edge, cost-per-part, tool-crib, cnc-machining-production]
level: practitioner
status: draft
description: "Choose and manage production tooling: ISO material groups and insert grades, geometry and nose radius, reading wear patterns, tool life by count, coolant choice and cost-per-part maths."
sources: ["ISO 513 (classification of hard cutting materials)", "ISO 1832 (indexable insert designation)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Insert grades, tool life and cost per part

**Goal:** pick tooling that gives predictable life and the lowest **cost per part**
(not the cheapest insert), and run it on a counted tool life rather than "until it
sounds wrong".

*Draft: grade names are manufacturer-specific; the ISO groups and wear-reading
principles are general. Use the maker's catalogue data for starting conditions.*

## 1. Start from the material group (ISO 513)
- **P (blue)** steels · **M (yellow)** stainless · **K (red)** cast iron ·
  **N (green)** non-ferrous (aluminium, copper) · **S (orange)** heat-resistant alloys
  and titanium · **H (grey)** hardened steel.
- Within a group, grades run from **wear-resistant** (hard, for stable continuous cuts,
  higher speed) to **tough** (for interrupted cuts, unstable setups, lower speed). Pick
  the toughest grade the conditions need, then move towards wear resistance as the
  process stabilises.
- Coatings: **CVD** (thick, heat-resistant — steel and cast iron turning); **PVD** (thin,
  sharp edges — stainless, superalloys, milling, small parts). Uncoated or polished/
  DLC for aluminium (stops built-up edge). **CBN** for hardened steel, **PCD** for
  non-ferrous/abrasive composites in volume.

## 2. Geometry
- **Insert shape:** stronger corner = larger included angle (round > 80° rhombic C >
  55° D > 35° V). Use the strongest shape the profile allows.
- **Nose radius:** larger = stronger edge and better finish at a given feed, but more
  radial force (chatter on slender parts). Theoretical finish `Ra ≈ f² / (32 × r) × 1000`
  (µm, with f in mm/rev and r in mm) — a planning estimate, not a guarantee.
- **Chip breaker** must match depth of cut and feed range; outside it, chips string or
  the edge overloads. Finishing, medium and roughing breakers exist for this reason.
- **Rake:** positive/sharp for low force and gummy materials; negative/strong for heavy
  roughing and interrupted cuts.

## 3. Read the wear
- **Flank wear (even):** normal; set life limit (e.g. VB 0.2–0.3 mm for finishing).
- **Crater wear:** too hot — reduce speed or use a more heat-resistant (CVD/alumina) grade.
- **Built-up edge:** too cold/sticky — raise speed, sharper/polished edge, better coolant.
- **Notch wear at depth-of-cut line:** work-hardened skin (stainless, superalloys) —
  vary depth of cut, use a round/larger-lead-angle insert.
- **Chipping/fracture:** too tough a job for the grade — tougher grade, stronger
  geometry, check setup rigidity and entry conditions.
- **Plastic deformation:** too hot and too much feed — reduce, or harder grade.

## 4. Tool life management
- Find the life: run to a defined wear limit (or quality limit) 3+ times, take the
  lower values, set the counter at ~80% of it. Track **parts per edge**.
- Use the control's tool life management (count or time) with sister tools for unattended runs.
- **Taylor:** `V × T^n = C` — life falls steeply with speed (n ≈ 0.2–0.3 for carbide),
  so a 20% speed cut can roughly double life. Use it to reason about trade-offs.

## 5. Coolant strategy
- **Flood** for heat and chip evacuation; **through-tool high pressure** (e.g. 70 bar and
  up) for deep drilling, chip breaking in superalloys and stainless.
- **Dry/air blast** often better for milling steel with coated carbide (thermal cracking
  from intermittent cooling) — follow the grade maker.
- **MQL** for aluminium and some steels where supported.
- Keep emulsion concentration in range (refractometer check) — weak coolant rusts parts
  and shortens tool life.

## 6. Cost per part
`Tool cost per part = (insert price / edges per insert) / parts per edge`
+ (tool change time × machine rate / parts per edge).
Machine time dominates: a premium grade that allows 20% higher speed usually wins
even at twice the insert price. Do the sum before standardising on the cheapest tool.

## Gotchas
- Mixing grades in the same drawer — label the tool crib by grade and geometry.
- Changing grade without resetting tool life counters.
- Judging a tool on one run; variation in material lot is real.

## Verify
- [ ] Grade chosen by ISO group and stability, coating matched to material.
- [ ] Wear pattern inspected and logged for the first runs.
- [ ] Tool life counter set from measured life with margin.
- [ ] Cost-per-part calculated including machine time.
- [ ] Coolant concentration checked on schedule.
