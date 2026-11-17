---
id: architecture-construction.plumbing-building-services.hydronic-heating-installation.installing-and-balancing-radiator-and-underfloor-circuits
name: installing-and-balancing-radiator-and-underfloor-circuits
category: architecture-construction
field: plumbing-building-services
product: hydronic-heating-installation
tags: [plumbing-building-services, hydronic-heating-installation, hydronic-heating, central-heating, radiators, underfloor-heating, radiant-floor, ufh, manifold, flow-meters, circulator-pump, expansion-vessel, pressure-relief-valve, boiler, heat-pump, primary-secondary, purging, air-separator, bleeding-radiators, balancing, lockshield, delta-t, inhibitor, system-filter, trv]
level: practitioner
status: draft
description: "Install hydronic heating: radiator and underfloor loops, manifolds, pumps and expansion, then fill, purge air and balance flows to the design temperature drop."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installing and balancing radiator and underfloor circuits

**Goal:** every room reaches design temperature at the design flow temperature, with no
air, noise or cold spots, and the right temperature drop across each emitter.

## 1. Design inputs
- Heat-loss per room (from the designer) → emitter output → required flow
  rate per circuit (flow = heat ÷ (specific heat × ΔT)). Typical ΔT: radiators ~10–20 K
  on boilers, ~5–7 K on heat pumps and underfloor.
- Flow temperature: low-temperature systems (heat pumps) need bigger radiators or
  underfloor. Don't swap emitters without checking output at *that* flow temperature.

## 2. Radiators
- Fix brackets to solid fixings; radiator level (or very slight fall towards the bleed
  end so air collects at the vent).
- Two-pipe systems (flow and return to each radiator) — avoid old one-pipe layouts
  in new work.
- TRV (thermostatic valve) on flow; lockshield on return for balancing. Many codes
  require TRVs except in the room with the main thermostat.

## 3. Underfloor heating
- Insulation under the pipes (edge strip around the perimeter too) — without it heat
  goes down.
- Loop layout from the design: spacing (often 100–200 mm), maximum loop length (often
  ~80–120 m for 16 mm pipe — **check manufacturer**), denser near cold outside walls.
- No joints in the slab. Mark loops at the manifold with the room they serve.
- **Pressure test before and during the screed pour** (keep the system under pressure
  so a damaged pipe is obvious).
- Screed curing and initial warm-up schedule per screed supplier — heating too fast
  cracks it.

## 4. Plant
- Pump sized for the index (hardest) circuit's flow and head.
- **Expansion vessel** sized to system volume, pre-charge set to the cold fill pressure;
  **pressure relief valve** piped to a safe visible discharge.
- Air separator / automatic air vents at high points; dirt separator/magnetic filter on
  return to the heat source.
- Hydraulic separation (low-loss header or buffer) where multiple pumps or heat pumps
  with minimum flow need it.

## 5. Fill, purge, treat
1. Flush the system (manufacturers' warranties often require a power flush or cleanse on
   retrofit).
2. Fill to cold pressure (often ~1–1.5 bar on sealed domestic systems).
3. Purge each circuit in turn: on manifolds close all loops but one, flow water through it
   to a hose until no air, repeat.
4. Bleed radiators from the lowest floor up; re-check pressure; top up.
5. Add inhibitor at the specified concentration; record it.

## 6. Balancing
- Run at design conditions. For radiators, adjust lockshields so each achieves the design
  ΔT (measure flow/return pipe temps with a clip thermometer). Start fully open on the
  furthest radiator and close down the nearest ones.
- For underfloor, set manifold flow meters to each loop's design flow.
- Commission controls: room thermostats, weather compensation curve, pump speed.

## Gotchas
- Air locks: gurgling and cold tops of radiators — re-purge.
- No edge insulation → screed cracks and heat loss.
- Expansion vessel pre-charge never checked → pressure swings and relief valve weeping.
- Heat pump with micro-bore or undersized emitters → poor comfort and efficiency.

## Verify
- [ ] Pressure test passed (and maintained through screeding for UFH).
- [ ] All circuits purged; no noise; system pressure stable hot and cold.
- [ ] Measured ΔT/flows match design within tolerance.
- [ ] Inhibitor dosed and recorded; filter fitted.
- [ ] Controls commissioned and explained to the user.

*Status: draft — loop lengths, ΔTs and pressures are typical; manufacturer and designer
values govern.*
