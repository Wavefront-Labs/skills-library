---
id: manufacturing-production.packaging-operations.filling-sealing-lines.filler-setup-fill-weight-control-and-seal-integrity
name: filler-setup-fill-weight-control-and-seal-integrity
category: manufacturing-production
field: packaging-operations
product: filling-sealing-lines
tags: [filling-sealing-lines, packaging-operations, filler, filling-machine, volumetric-filler, piston-filler, gravimetric-filler, net-weight-filler, flowmeter-filler, auger-filler, fill-weight, average-quantity, e-mark, tne, tolerable-negative-error, nist-handbook-133, giveaway, overfill, heat-seal, induction-seal, capping, cap-torque, seal-integrity, leak-test, dye-test, vacuum-decay, bubble-test]
level: practitioner
status: draft
description: "Set up a filler and sealer: choose and tune the fill method, control fill weight against average-quantity rules with minimum giveaway, set seal time/temperature/pressure and prove seal integrity."
sources: ["UK Weights and Measures (Packaged Goods) Regulations 2006", "NIST Handbook 133 (Checking the Net Contents of Packaged Goods)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filler setup, fill-weight control and seal integrity

**Goal:** every pack legally contains at least what the label says, with as little
overfill (giveaway) as possible, and every seal or closure keeps the product in and
contamination out.

## 1. Know your filler type
- **Volumetric** (piston, timed-pressure, flowmeter, cup filler): meters a volume. Fill
  *weight* shifts with product density, temperature and aeration — check weight, not
  just volume setpoints.
- **Gravimetric / net-weight** (load cell per head): weighs as it fills; most accurate,
  slower, for high-value product.
- **Auger** (powders): weight depends on bulk density and hopper level — keep the hopper
  level steady.
- **Level / overflow** fillers (bottles, beverages): fill to a visual height; variance in
  bottle volume becomes variance in contents.

## 2. Setup and startup
1. Change parts and nozzles correct for the format; product recipe recalled.
2. Prime the filler and purge air from lines and pistons (air = short fills).
3. Bring product to its normal running temperature; viscosity and density change with it.
4. Run a **head-by-head check**: weigh, say, 3–5 fills from **every** head. One head
   out is a nozzle/valve issue; all heads out is a setpoint or product issue.
5. Adjust, recheck, record. Then start production with in-line checkweigher running
   (manufacturing-production.packaging-operations.checkweighing-inspection-systems.checkweigher-and-metal-detector-setup-and-challenge-testing).

## 3. Fill-weight rules (average quantity system)
Most of Europe, UK and Australia use the **average system** (℮ mark); the US uses a
broadly similar NIST Handbook 133 approach. Under the EU/UK rules, in outline:
1. The **average** content of a batch must be at least the nominal quantity.
2. Not more than a small proportion (2.5% in the EU/UK rules) may be below nominal by
   more than the **tolerable negative error (TNE)** — e.g. 15 g for a 500 g pack.
3. **No pack** may be short by more than twice the TNE.
Check the TNE table and current rules for your jurisdiction; the exact values and
sampling plans are statutory.

Setting the target: target = nominal + enough margin to meet the rules given your
filler's standard deviation. A filler with σ = 3 g needs much less overfill than σ =
8 g. **Cutting variation is the only safe way to cut giveaway.** Track the mean and σ
per head over time; giveaway = (mean − nominal) × packs per year — usually a large
number worth showing management.

Tare: weigh empties from the current container lot to find tare; container weight
varies between suppliers and lots.

## 4. Seals and closures
- **Heat seals** (lids, pouches, film): the three variables are **temperature, dwell
  time and pressure**. Set from the film supplier's seal window; contamination in the
  seal area (product splash, powder) is the commonest cause of leakers.
- **Induction seals** (foil under caps): power and conveyor speed set the energy;
  check foil adhesion by peeling.
- **Screw caps:** check application torque and **removal torque** (after the cap has
  relaxed — often measured after a set time) with a torque tester against spec.
- Crimp/roll-on closures and can seams have specialist checks (seam teardown) — follow
  the closure supplier's spec.

## 5. Proving seal integrity
Pick tests to suit the pack (and your quality plan's frequency):
- **Visual:** wrinkles, channels, burn-through, product in seal.
- **Bubble / immersion:** pack under water in a vacuum chamber; a stream of bubbles
  shows the leak.
- **Dye penetration:** dye along the seal edge; wicking through shows a channel.
- **Squeeze / burst / peel-strength** tests for pouches and lids.
- **Vacuum decay / pressure decay** instruments for non-destructive or high-assurance
  testing.

## Gotchas
- Foaming product: slow the fill or use bottom-up nozzles, or you get short fills and
  wet seals.
- Changing density after a new raw-material batch shifts volumetric fills — recheck
  weights at every batch change.
- Don't adjust on a single heavy or light pack; adjust on the mean of a sample.

## Verify
- [ ] Every head checked at startup and after adjustments.
- [ ] Batch mean ≥ nominal, below-TNE packs within the allowed proportion, none below 2×TNE.
- [ ] Mean and σ per head logged; giveaway known.
- [ ] Seal parameters within the film's window; integrity test passed and recorded.

*Uncertain: statutory percentages and TNE tables vary by country; check the local
legislation.*
