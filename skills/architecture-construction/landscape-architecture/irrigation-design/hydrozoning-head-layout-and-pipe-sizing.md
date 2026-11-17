---
id: architecture-construction.landscape-architecture.irrigation-design.hydrozoning-head-layout-and-pipe-sizing
name: hydrozoning-head-layout-and-pipe-sizing
category: architecture-construction
field: landscape-architecture
product: irrigation-design
tags: [irrigation-design, landscape-irrigation, irrigation-plan, hydrozones, hydrozoning, water-budget, et, evapotranspiration, plant-factor, head-layout, head-to-head-coverage, spray-heads, rotors, rotary-nozzles, mp-rotator, matched-precipitation, drip-irrigation, inline-drip, point-source, pipe-sizing, velocity, friction-loss, hazen-williams, static-pressure, dynamic-pressure, flow-rate, lpm, gpm, backflow-prevention, valves, controller, smart-controller, landscape-architecture]
level: practitioner
status: draft
description: "Design landscape irrigation: water budget and hydrozones, head-to-head spray and rotor layout, drip zones, zone flow limits, pipe sizing by velocity, pressure losses and backflow."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hydrozoning, head layout and pipe sizing

**Goal:** an irrigation design that delivers each plant group the water it needs,
uniformly, within the available supply, with pipes sized so the system runs at the
right pressure. (Auditing and scheduling an installed system is covered in
`agriculture-environment.landscape-grounds-keeping.grounds-irrigation.sprinkler-audit-and-controller-runtimes`.)

## 1. Start with the supply
- Measure **static pressure** at the point of connection (gauge on a hose bib with
  water off) and **available flow** (bucket test: time to fill a known volume with the
  tap fully open, or meter data/utility information). Design to a safe fraction of
  available flow (commonly ~75%) — supply pressure drops at peak times.
- Required **backflow prevention** device type per local code (double check valve,
  RPZ, PVB) — it costs pressure; include its loss.

## 2. Water budget and hydrozones
- Estimate need = reference ET × **plant factor** (e.g. turf ~0.6–0.8, mixed shrubs
  ~0.3–0.5, drought-tolerant ~0.1–0.3) × area ÷ efficiency. Many jurisdictions cap
  landscape water budgets (e.g. California's MWELO); check local rules.
- **Hydrozone:** group plants of similar water need **and** similar sun exposure and
  emitter type. Never mix turf sprays and shrub drip on one valve; split north and
  south slopes.

## 3. Head layout
- **Head-to-head coverage:** each head's spray reaches the next head (spacing ≈ the
  radius), on square or (better) triangular spacing. Reduce spacing (~50–55% of
  diameter) in windy sites.
- Start at corners and edges with part-circle heads, then fill the middle.
- **Matched precipitation:** heads on one valve should apply water at the same rate —
  match quarter, half and full arcs with matched-precipitation nozzles; don't mix
  sprays (~40 mm/hr) with rotors (~10–15 mm/hr) on a zone.
- Narrow strips (< ~2 m): use strip nozzles or drip to avoid overspray onto paving.

## 4. Drip
- Inline drip for beds (emitter spacing ~300–450 mm, row spacing similar) or point
  source for trees/shrubs (emitter count increasing as plants grow). Each drip zone
  needs a filter and pressure regulator (drip typically runs ~1.5–2.5 bar). Flush valves at ends.

## 5. Zone flow and pipe sizing
1. Sum the flow of all heads/emitters on a zone; keep it within the design supply.
2. Size each pipe section for **velocity ≤ ~1.5 m/s (5 ft/s)** to limit water hammer
   and friction loss. Use manufacturer charts for your pipe class (PVC/PE).
3. Calculate pressure at the most critical head: static − meter/backflow loss −
   friction losses (Hazen-Williams tables) − valve loss − elevation gain (~0.1 bar per
   metre rise). It must meet the nozzle's operating pressure (sprays ~2 bar, rotors
   ~2.5–3.5 bar) — and not exceed it much (misting); use pressure-regulating heads.
4. Mainline under constant pressure: sized for the largest zone; isolation valves.

## 6. Controller
Smart (ET or soil-moisture based) controller with rain sensor, cycle-and-soak for
slopes and clay, and the zone schedule on the drawing.

## Gotchas
- Designing to static pressure and getting low flow at the far heads.
- Mixed head types on a valve → wet and dry patches.
- Sprays on narrow strips watering the footpath.
- Ignoring elevation — uphill heads underperform, downhill heads drain out (use check valves).

## Verify
- [ ] Static pressure, flow and backflow loss recorded.
- [ ] Hydrozones by water need, exposure and emitter type.
- [ ] Head-to-head coverage with matched precipitation per zone.
- [ ] Zone flows within supply; velocities ≤ limit; critical-head pressure OK.
- [ ] Controller, sensors and schedule specified.
