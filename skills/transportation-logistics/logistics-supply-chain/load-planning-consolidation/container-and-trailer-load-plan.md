---
id: transportation-logistics.logistics-supply-chain.load-planning-consolidation.container-and-trailer-load-plan
name: container-and-trailer-load-plan
category: transportation-logistics
field: logistics-supply-chain
product: load-planning-consolidation
tags: [load-planning-consolidation, load-planning, logistics-supply-chain, container-loading, trailer-loading, cube-utilisation, cube-optimisation, pallet-pattern, pallet-configuration, consolidation, axle-weight, axle-load, weight-distribution, center-of-gravity, load-securing, dunnage, lashing, 20ft-container, 40ft-container, 53ft-trailer, euro-pallet, gma-pallet, cargo-planning-software, cubemaster]
level: practitioner
status: gated
description: "Plan a container or trailer load: check weight and cube limits, choose pallet patterns, place heavy freight for legal axle weights, consolidate orders and secure the load."
sources: ["https://www.ecfr.gov/current/title-23/section-658.17", "https://www.ecfr.gov/current/title-49/section-393.102", "https://www.fmcsa.dot.gov/regulations/cargo-securement"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container and trailer load plan — full, legal and undamaged

**Goal:** put the most freight in each unit without exceeding weight, volume or axle
limits, in an order that unloads correctly and arrives undamaged.

## 1. Know the box (typical internal figures — confirm with the carrier)
| Unit | Inside L × W × H (m) | Floor pallets | Max payload |
|---|---|---|---|
| 20' dry | 5.90 × 2.35 × 2.39 | 10–11 GMA, 11 euro | ~25–28 t (box), often road-limited |
| 40' dry | 12.03 × 2.35 × 2.39 | 20–21 GMA, 23–24 euro | ~26–28 t |
| 40' HC | 12.03 × 2.35 × 2.69 | same floor, +0.3 m height | ~26–28 t |
| EU 13.6 m curtainsider | 13.6 × 2.48 × ~2.7 | 33 euro, 26 UK/GMA | ~24–25 t |
| US 53' dry van | ~16.1 × 2.5 × 2.7 | 26 GMA single-stacked (13 × 2) | ~20 t (45,000 lb) |

Container and trailer dimensions, pallet counts, payloads and ISO centre-of-gravity limits in this skill come from ISO standards and carrier practice (gated: unconfirmed, source is paywalled or blocked). Use the unit data plate and carrier specification.

Euro pallet 1200 × 800 mm; GMA 48 × 40 in; UK 1200 × 1000 mm.
The road at either end often limits gross weight more than the container rating
(US federal Interstate limit 80,000 lb gross, 23 CFR 658.17; EU limits vary by country (gated: unconfirmed, source is paywalled or blocked)).

## 2. Weight vs cube: find the limiting factor
Compute density: kg per m³ of the shipment. A 40' holds ~67 m³ nominal; with ~26 t
payload the break-even density is ~390 kg/m³ (use ~85–90% of nominal cube as
practical). Denser freight "weighs out" — stop thinking about cube; lighter freight
"cubes out" — optimise stacking and pallet heights.

## 3. Pallet patterns
- Build cases to the full pallet footprint without overhang (overhang crushes cases
  and wastes space); allow up to ~25 mm underhang.
- Pick pallet height to fit the box: e.g. two layers of 1.15 m pallets in a 2.39 m
  container leaves ~9 cm clearance — check door height (~2.28 m in a 20'/40' dry,
  lower than internal height).
- Column stacking is strongest; interlocking is more stable but loses ~compression
  strength. Use stretch wrap and corner boards on column stacks.
- Pallet planning tools (CubeMaster, Cape Pack, TOPS, many free online calculators)
  solve case-on-pallet and pallet-in-container patterns.

## 4. Axle weights and centre of gravity
- Spread weight along the length; **don't put all heavy pallets at the nose** or tail.
  On a tractor-semitrailer, freight forward of the trailer midpoint loads the drive
  axle; rearward loads the trailer tandem.
- Check against axle limits (US federal: 20,000 lb single axle and 34,000 lb tandem under 23 CFR 658.17, and states may not limit steer axles below 20,000 lb or the manufacturer rating; EU per-axle limits
  typically 10–11.5 t drive axle (gated: unconfirmed, source is paywalled or blocked), check national rules). Slide the trailer tandem or
  reposition freight to balance; a truck scale ticket is the proof.
- Containers: keep the CoG near the centre lengthways and low; ISO guidance limits the
  CoG offset (roughly ±5% of length) — heavy goods distributed over the floor, never
  concentrated loads beyond the floor rating.

## 5. Consolidation
- Group orders by destination and delivery sequence; load **last-off first-in**
  (first delivery nearest the doors).
- Check compatibility: no food with chemicals, no odour transfer, DG segregation.
- Combine LTL shipments into a multi-stop truckload when stops are on a line and the
  sum is above ~10–12 pallets — compare cost and stop-off charges.

## 6. Secure the load
Block gaps with airbags/dunnage (voids > ~15 cm), use load bars or straps, and
follow the CTU Code (IMO/ILO/UNECE) for containers: brace against forward braking
forces (US 49 CFR 393.102 uses 0.8 g forward and 0.5 g rearward and lateral on breaking strength, and working load limits of 0.435 g forward, 0.5 g rearward and 0.25 g lateral; EN 12195-1 values (gated: unconfirmed, source is paywalled or blocked)).

## Gotchas
- Nominal cube ≠ usable cube; door opening is smaller than the interior.
- Reefer containers lose ~10% length to the unit and need airflow space at top (red line).
- Weight-based limits apply to the whole vehicle incl. tractor and fuel.
- VGM declared must match actual — misdeclared containers get rolled or fined.

## Verify
- [ ] Gross weight and each axle within legal limits (scale ticket where possible).
- [ ] Cube utilisation recorded; heavy freight spread, CoG near centre.
- [ ] Load sequence matches drop sequence.
- [ ] No voids; securing per CTU Code / EN 12195-1; photos taken before sealing.

*Uncertainty:* dimensions and limits vary by box manufacturer and jurisdiction — values here are typical, not authoritative.

## Checked

Jurisdiction: US federal weight and securement rules with EU notes. Checked 2026-10-25 on eCFR: 23 CFR 658.17 (80,000 lb gross, 20,000 lb single axle, 34,000 lb tandem, states may not limit steer axles below 20,000 lb or manufacturer rating) and 49 CFR 393.102 (breaking strength 0.8 g forward, 0.5 g rearward and lateral; working load limit 0.435 g forward, 0.5 g rearward, 0.25 g lateral). Corrected: the draft gave a 12,000 lb US steer-axle limit, which is not a federal limit. ISO, EN and carrier figures are marked gated.

Method: documentation only; no commands were run.
