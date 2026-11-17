---
id: agriculture-environment.irrigation-water-management.stock-water-systems.stock-water-reticulation-and-trough-checks
name: stock-water-reticulation-and-trough-checks
category: agriculture-environment
field: irrigation-water-management
product: stock-water-systems
tags: [stock-water-systems, stock-water, livestock-water, reticulation, troughs, water-troughs, float-valve, ball-valve, poly-pipe, polyethylene-pipe, header-tank, solar-pumping, solar-pump, bore, windmill, water-quality, tds, salinity, sulphate, nitrate, blue-green-algae, cattle, sheep, water-requirements, trough-flow-rate]
level: practitioner
status: gated
description: "Plan and check stock water: daily litres per head, pipe and trough sizing for peak demand, float valves, solar pump checks and water-quality limits."
sources: ["https://www.agric.wa.gov.au/node/3989"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stock water reticulation and trough checks

**Goal:** every animal can drink as much as it wants on the hottest day, from water
that won't make it sick — and you find failures within a day, not when stock are
bellowing at an empty trough.

## 1. How much water (planning figures) (gated: unconfirmed, source is paywalled or blocked)
Typical daily intake, **litres per head per day** (rises sharply with heat, dry feed,
lactation and salty feed; often quoted ranges):

| Stock | Cool / green feed | Hot / dry feed |
|---|---|---|
| Sheep, dry | 2–4 | 6–10 |
| Ewe with lamb | 4–6 | 8–12 |
| Beef cattle, dry | 30–40 | 60–80 |
| Lactating dairy cow | 70–100 | 120–200 |
| Horse | 30–40 | 50–60 |
| Goat | 3–6 | 8–12 |

Design for the **hot-day figure**, and remember most drinking happens in a few hours:
cattle may take 25–30% of the day's water in one hour (gated: unconfirmed, source is paywalled or blocked) after coming off feed.

## 2. Trough flow and capacity
- **Peak flow to a trough** must refill it as fast as the mob drinks. A common design
  target is that the trough + inflow can supply the herd's peak-hour demand. Example:
  200 cows × 80 L/day × 25% in the peak hour = 4,000 L/h ≈ 1.1 L/s.
- If the pipeline can't deliver that, add **trough storage** (bigger trough or a
  header tank) so the deficit comes from storage.
- **Trough access:** allow roughly 10% of the mob drinking at once (gated: unconfirmed, source is paywalled or blocked); ~0.3–0.4 m of
  trough edge per drinking cow, less for sheep. Bully animals guard short troughs.

## 3. Pipe and pressure basics
- Most farm reticulation is **polyethylene (poly) pipe**. Check the pipe's pressure
  rating (PN) exceeds the highest static pressure: every **10 m of fall adds ~1 bar
  (100 kPa)**. Low points on long downhill runs see the most pressure.
- Friction loss grows fast with flow; undersized pipe is the commonest fault. Use the
  manufacturer's friction tables (head loss per 100 m at your flow) rather than guessing.
- Fit air valves at high points and drain/flush points at low points; bury pipe below
  cultivation and frost depth, and mark the line.

## 4. Pumps and solar
- **Solar pumps** only deliver in daylight: size so that one sunny day fills a
  storage tank holding **2–3 days** (gated: unconfirmed, source is paywalled or blocked) (more in cloudy climates) of peak demand, then
  gravity-feed troughs.
- Weekly check: panel surfaces clean, controller showing normal operating status,
  pump output (time how long a known volume takes), and tank level at dawn.
- Bores: record standing water level and pumping level; a falling pumping level or
  sand in the water is an early warning.

## 5. Trough and float-valve maintenance
- Check every trough on a schedule that matches the risk: **daily in hot weather**
  where stock depend on it, by camera/telemetry level sensors where distance makes that
  impractical.
- Float valves: keep a spare valve, washers and a seat in the ute. Silt, snails and
  algae jam them. Fit a **float guard** so stock can't knock it.
- Clean troughs regularly (scrub out algae, remove dead birds/rodents — botulism risk).
  Fit a bird/wildlife escape ramp.

## 6. Water quality checks
Test new sources and any source that changes taste, colour or smell. Key items and
commonly quoted upper limits (vary by guideline, species and production level):
- **Total dissolved solids (salinity):** beef cattle up to ~4,000 mg/L no adverse effect,
  sheep up to ~5,000 mg/L (gated: unconfirmed, source is paywalled or blocked); dairy and young stock lower. A cheap EC meter gives a
  quick estimate: `TDS (mg/L) ≈ EC (µS/cm) × 0.65` (gated: unconfirmed, source is paywalled or blocked) (approximation).
- **Sulphate:** > ~1,000 mg/L (gated: unconfirmed, source is paywalled or blocked) can cause scouring and, in cattle, polioencephalomalacia.
- **Nitrate:** high levels (e.g. hundreds of mg/L as nitrate) are dangerous combined
  with nitrate-rich feed.
- **Blue-green algae:** stop access to scummy, still dams in warm weather and test.
Treat these thresholds as starting points — **unconfirmed for your stock class**; ask
your vet or agricultural lab to interpret a result.

## Gotchas
- A trough fed through a long thin pipe looks fine at dawn and is empty by 2 pm.
- Frozen pipes and floats in cold climates — insulate, use heated or frost-free troughs.
- New poly pipe in sun expands and kinks; snake it in the trench.

## Verify
- [ ] Peak-hour demand calculated and met by flow + trough/tank storage.
- [ ] Pipe pressure rating exceeds static pressure at the lowest point.
- [ ] Solar storage holds ≥ 2 days of hot-weather demand.
- [ ] Trough check routine set (daily in heat) and float spares on hand.
- [ ] Water test on file for each source, interpreted against stock class.

## Checked

- Date: 2026-10-25. Jurisdiction: Australia assumed (ANZECC/ARMCANZ 2000 guideline values).
- Confirmed against: WA DPIRD (adapted from ANZECC) lists mature beef cattle at 0-4000 mg/L TDS as no adverse effects; the head figure was recomputed (every 10 m of fall is about 1 bar, 9.81 kPa per metre); the peak-hour arithmetic (200 x 80 x 25% = 4,000 L/h = 1.1 L/s) was recomputed.
- Not confirmed: the daily water-use table, sheep TDS limit, sulphate limit, EC-to-TDS factor, peak-hour share, trough access and storage days (the WA page returned 404 to the fetch tool, so only search excerpts were read; no free source stating the other figures was found).

Method: documentation only; no commands were run.
