---
id: architecture-construction.construction-estimating-scheduling.quantity-takeoff.measuring-and-checking-a-takeoff
name: measuring-and-checking-a-takeoff
category: architecture-construction
field: construction-estimating-scheduling
product: quantity-takeoff
tags: [construction-estimating-scheduling, quantity-takeoff, takeoff, take-off, measurement, quantity-surveying, qs, bill-of-quantities, boq, nrm2, nrm, cesmm, smm7, asmm, masterformat, dimension-sheets, timesing, deductions, waste-factor, girth, mean-girth, net-vs-gross, takeoff-qa, estimating, quantities]
level: practitioner
status: draft
description: "Measure work from drawings methodically: rules of measurement (NRM2/CESMM/MasterFormat), dimension sheets, timesing, deductions, waste factors, and independent checking of the takeoff."
sources: ["RICS NRM2: Detailed measurement for building works", "ICE CESMM4 Civil Engineering Standard Method of Measurement", "CSI MasterFormat"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measuring and checking a takeoff

**Goal:** produce quantities that a second person can follow, that match the agreed
rules of measurement, and that are checked before anyone prices them.

## 1. Fix the rules before measuring
- Agree the **method of measurement**: UK building — RICS **NRM2**; UK civils —
  **CESMM4**; Australia — **ASMM**; US practice usually follows **CSI MasterFormat**
  divisions with contractor-specific conventions. The method decides units, what is
  measured net, and what minimum deductions apply.
- Agree **net vs gross**. Bills of quantities are normally **net** (as fixed in place);
  waste is the estimator's allowance in the rate. Contractor takeoffs often add waste to
  the quantity instead — state which, never both.
- Agree units: m, m², m³, t, nr (US: LF, SF, SY, CY, EA, tons). Converting later invites
  error (1 CY = 0.7646 m³; 1 SY = 9 SF).

## 2. Work in a fixed order
1. Read the whole set first: drawings, specification, schedules, and addenda. Log
   discrepancies as queries/RFIs immediately.
2. Measure **by element or trade** in construction order (substructure → frame →
   envelope → internal → finishes → services → external works). Order prevents
   omissions.
3. Within each item: **largest to smallest, left to right, top to bottom** on the
   drawing, and tick or highlight what you measured (a coloured mark per item).
4. Record on **dimension sheets** or a structured spreadsheet: location/grid, timesing,
   dimensions, squared result, description. Write "where-from" notes (e.g. "grid A–D,
   dwg A-201 rev C") — the checker needs them.

## 3. Techniques that save errors
- **Timesing:** measure one typical bay or floor and multiply, noting the multiplier
  clearly (e.g. `6/` for six identical bays).
- **Mean girth** for walls/footings: centreline length = external perimeter −
  4 × wall thickness for a simple rectangle (each corner over-measured by the
  thickness). Then length × height × thickness.
- **Measure gross, deduct openings** where rules say so (e.g. many rules disregard
  voids below a threshold area — check the threshold in your method; often around
  0.5–1.0 m², unverified per rule set).
- **Waste rules of thumb** (contractor takeoffs, adjust by detail): concrete 3–5%,
  rebar 3–5% plus laps, blockwork/brick 5%, drywall 10–12%, tile 10–15% (diagonal
  layouts more), timber framing 10%. These are starting points, not standards.
- Keep **descriptions** tied to spec references, so pricing hits the right item.

## 4. Check it (always someone else, or you on a different day)
1. **Arithmetic check** — re-square a random 10% of lines; formula audit in spreadsheets
   (look for hard-typed numbers overriding formulas).
2. **Reasonableness ratios:** e.g. formwork m² to concrete m³ (slabs ~ 5–7 m²/m³ for a
   150–200 mm slab), rebar kg/m³ (often 80–150 for building elements), wall-to-floor
   ratio, door count vs rooms. Outliers point to errors.
3. **Cross-check totals** against an independent route: slab area vs gross floor area,
   paint area vs wall plaster area.
4. **Revision check:** confirm every sheet used is the latest revision; overlay changed
   sheets and re-measure clouds.
5. Sign and date the check; record corrections.

## Gotchas
- Scale errors on reduced prints (A1 printed at A3 = half scale).
- Double-counting at junctions (walls measured through corners twice; slab and beam
  concrete overlapping).
- Items shown on one discipline only (structural vs architectural) get missed or
  measured twice — reconcile disciplines.
- Provisional or "by others" items silently omitted — list exclusions explicitly.
- Unit confusion between tonnes, US tons and long tons on steel.

## Verify
- [ ] Method of measurement and net/gross basis are written at the top of the takeoff.
- [ ] Every quantity has location, drawing reference and revision.
- [ ] Waste is applied once, in a visible place.
- [ ] Ratios checked and outliers explained.
- [ ] An independent check is recorded and corrections applied.
- [ ] Queries/RFIs and exclusions listed for the estimator.
