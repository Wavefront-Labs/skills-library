---
id: transportation-logistics.aviation-piloting.flight-planning-performance.fuel-and-weight-and-balance-planning
name: fuel-and-weight-and-balance-planning
category: transportation-logistics
field: aviation-piloting
product: flight-planning-performance
tags: [aviation-piloting, flight-planning-performance, flight-planning, preflight-planning, fuel-planning, fuel-reserve, final-reserve, alternate, contingency-fuel, taxi-fuel, trip-fuel, weight-and-balance, mass-and-balance, center-of-gravity, cg, moment, arm, loading-envelope, mtow, mlw, takeoff-performance, landing-performance, density-altitude, pressure-altitude, metar, taf, weather-briefing, poh, afm]
level: practitioner
status: gated
description: "Plan a flight's fuel (trip, contingency, alternate, reserve), compute weight and balance with arms and moments, and check takeoff and landing performance against conditions."
sources: ["14 CFR 91.151 Fuel requirements for flight in VFR conditions (eCFR, ecfr.gov)", "FAA Pilot's Handbook of Aeronautical Knowledge and Airplane Flying Handbook (faa.gov)", "Aircraft POH/AFM"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fuel, weight-and-balance and performance planning

**Goal:** before engine start you know you can take off, reach the destination or
an alternate, and land with legal and personal reserves — with the CG inside the
envelope for the whole flight.

> Worked with light-aircraft numbers (all arithmetic recomputed). Fuel rules differ (FAA 14 CFR 91.151, confirmed in the eCFR: day VFR
> 30 min / night 45 min after the first point of intended landing, rotorcraft 20 min; EASA and commercial rules use trip + contingency +
> alternate + final reserve (gated: unconfirmed, source is paywalled or blocked)). Use your POH/AFM and applicable regulations.

## 1. Weather first
- METARs and TAFs for departure, destination, alternates; area forecasts, winds aloft,
  SIGMETs/AIRMETs, NOTAMs.
- Decide go/no-go and the **alternate** before calculating fuel — weather drives fuel.

## 2. Fuel plan (commercial-style structure, use it for GA too)
| Component | Meaning | Example (piston single, ~9 USG/h) |
|---|---|---|
| Taxi | start, taxi, run-up | 1.1 USG |
| Trip | climb + cruise + descent with forecast winds | 120 NM at 110 kt GS ≈ 65 min → 10 USG |
| Contingency | e.g. 5–10% of trip | 1 USG |
| Alternate | destination → alternate | 30 NM ≈ 20 min → 3 USG |
| Final reserve | e.g. 45 min | 6.8 USG |
| **Required** | sum | **≈ 22 USG** |
Then add **extra/discretionary** for known delays. Compare required with **usable**
fuel (not total) in the POH. Plan to land with the final reserve untouched.

## 3. Weight and balance
1. List each item with weight and **arm** (distance from datum, from the POH).
2. **Moment = weight × arm**. Sum weights and moments.
3. **CG = total moment ÷ total weight.**
Example (illustrative values):
| Item | Weight (lb) | Arm (in) | Moment (lb-in) |
|---|---|---|---|
| Empty aircraft | 1,650 | 39.0 | 64,350 |
| Pilot + front pax | 360 | 37.0 | 13,320 |
| Rear pax | 170 | 73.0 | 12,410 |
| Baggage | 50 | 95.0 | 4,750 |
| Fuel 40 USG × 6 lb (avgas, about 6 lb/USG (gated: unconfirmed, source is paywalled or blocked)) | 240 | 48.0 | 11,520 |
| **Total** | **2,470** | **43.1** (106,350 ÷ 2,470 = 43.06) | **106,350** |
4. Check total ≤ **MTOW** and the CG within the envelope at takeoff **and at landing**
   (with fuel burned) — fuel burn can move the CG out of limits in some types.
5. Too heavy → offload fuel (if still meets the fuel plan), bags or a passenger.

## 4. Takeoff and landing performance
1. **Pressure altitude** = field elevation + (1013 − QNH) × ~30 ft (gated: unconfirmed, source is paywalled or blocked) (or (29.92 − altimeter)
   × 1,000 ft).
2. **Density altitude** ≈ PA + 120 ft × (OAT − ISA temp) (gated: unconfirmed, source is paywalled or blocked), ISA temp = 15 °C − 2 °C per
   1,000 ft. Example: PA 2,000 ft, OAT 30 °C → ISA 11 °C → DA ≈ 2,000 + 120×19 ≈ 4,300 ft.
3. Read the POH chart for ground roll and **distance over 50 ft obstacle** at that DA,
   weight and wind.
4. Apply corrections (grass, wet, slope) and then a **safety factor** (e.g. ×1.3–1.5 (gated: unconfirmed, source is paywalled or blocked) or
   your operator's factor). Compare with available runway.
5. Do the same for landing at the destination and alternate.

## 5. Gotchas
- Using total fuel instead of usable fuel.
- Forgetting headwind increases trip fuel at *your* planned altitude — use winds aloft.
- Rear-heavy loading feels fine on the ground and is dangerous in a stall.
- POH performance assumes a new aircraft and good technique — the factor is there for a reason.
- Hot, high, heavy, humid: each worsens climb; together they can make a "normal"
  strip impossible.

## Verify
- [ ] Fuel plan sums taxi, trip, contingency, alternate and final reserve vs usable fuel.
- [ ] Weight ≤ MTOW and CG inside the envelope at takeoff and landing.
- [ ] Density altitude was computed and used in the performance charts.
- [ ] Factored distances fit the runways at departure, destination and alternate.
- [ ] Weather and NOTAMs were checked before the fuel calculation.
