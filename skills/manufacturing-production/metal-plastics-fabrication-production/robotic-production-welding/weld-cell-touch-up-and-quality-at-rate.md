---
id: manufacturing-production.metal-plastics-fabrication-production.robotic-production-welding.weld-cell-touch-up-and-quality-at-rate
name: weld-cell-touch-up-and-quality-at-rate
category: manufacturing-production
field: metal-plastics-fabrication-production
product: robotic-production-welding
tags: [robotic-production-welding, robotic-welding, weld-cell, gmaw, mig, mag, fanuc, abb, yaskawa, motoman, kuka, teach-pendant, touch-up, tcp, tool-centre-point, tcp-check, torch-cleaning, reamer, contact-tip, wire-feed, touch-sensing, seam-tracking, through-arc-seam-tracking, fixture, spot-welding, resistance-spot-weld, weld-schedule, electrode-dressing, peel-test, chisel-test, cut-and-etch, macro-etch, weld-quality, porosity, burn-through]
level: practitioner
status: draft
description: "Keep a robotic MIG/spot weld cell making good welds: TCP checks after a crash, safe program touch-up, torch maintenance, fixture checks, and peel, chisel and cut-and-etch weld verification."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Weld cell touch-up and quality at rate

**Goal:** a robotic weld cell that produces the same weld on part 1 and part 10,000 —
which mostly means keeping the **torch where the program thinks it is**, the **part
where the fixture says it is**, and catching drift with destructive checks before it
reaches the customer.

## Safety
Teach-mode work inside the cell: enabling device (deadman), reduced speed, one person in
control of the pendant, lockout for fixture work. Arc flash and fume extraction as for
manual welding.

## 1. TCP — the first check after anything bumps the torch
The **tool centre point** (wire tip position) defines every weld path. After a torch
collision, a torch neck change, or a cable/liner change:
1. Run the **TCP check** routine (pin/pointer or automatic TCP measurement station,
   e.g. a beam-break unit). Most cells have one; use it rather than eyeballing.
2. If out of tolerance: straighten/replace the neck, re-run; only re-teach the TCP
   per procedure if the hardware is right and it still disagrees.
3. Do **not** "fix" a bent torch by touching up every program point — you will
   corrupt all programs that use that tool.

## 2. Program touch-up rules
- Touch up only the points that are wrong, on a known-good part in a known-good fixture.
- Keep the **torch angles** (work angle, travel angle) and stick-out per the weld
  procedure; touch-ups that drag the angle change penetration.
- Save a backup before editing; comment the change (date, reason). Many sites lock
  weld parameters (WPS values) so operators can touch up positions only.
- Run the edited section at low speed with no arc (dry run) before welding.
- **Touch-sensing** (wire-touch search) and **through-arc seam tracking** compensate
  part variation — check they're enabled for the joints that need them and the
  search distances aren't maxed out (a maxed search hints at fixture or part issues).

## 3. Torch and wire maintenance
- **Torch cleaning station** (reamer, anti-spatter spray, wire cutter) on schedule —
  spatter build-up in the nozzle causes porosity and erratic arc.
- **Contact tip** change interval: worn tips wander and arc-start poorly. Set by count/time.
- Liner and drive rolls: feed problems show as burn-backs and erratic arc.
- Shielding gas flow at the nozzle (flowmeter at nozzle, not just at regulator).
- Wire stick-out cut consistent before touch-sensing.

## 4. Fixtures
Clamps, locators and pins wear; spatter on locators shifts parts. Clean locators every
shift; check with a gauge/master part on the site's interval.

## 5. Weld verification
- **Visual** every part (or per plan): size, undercut, porosity, missed welds,
  burn-through, start/stop quality.
- **Cut-and-etch (macro-etch)** on a sample per shift/lot: section the weld, etch, measure
  penetration, leg length and throat against the WPS/drawing.
- **Spot welding**: **peel** or **chisel test** per weld schedule check; nugget size
  against the minimum for the sheet thickness. Electrode **tip dressing** on schedule;
  mushroomed tips drop current density and nugget size. Weld controllers often step
  current up with tip wear ("stepper") — keep the stepper and dresser in sync.
- Monitor arc data (current, voltage, wire feed) if the cell logs it; alarms on
  deviations catch problems between destructive tests.

## Defect → first suspects
| Defect | Check |
|---|---|
| Weld off seam | TCP, fixture/part position, seam tracking disabled |
| Porosity | Gas coverage (nozzle spatter, draughts, flow), contamination on part |
| Burn-through | Gap too large (part fit-up), travel speed, wrong program |
| Poor arc start | Contact tip worn, wire stick-out, ground (work return) connection |
| Small spot nugget | Tip wear/dressing, current/stepper, part fit-up gaps |

## Verify
- [ ] TCP check passed this shift and after any collision.
- [ ] Program edits backed up, commented, dry-run before welding.
- [ ] Torch cleaning and tip change intervals met.
- [ ] Cut-and-etch / peel tests within spec at the required frequency.

*Draft: pendant workflows differ by brand (Fanuc, ABB, Yaskawa, KUKA); test
frequencies and criteria come from the WPS and customer standards (e.g. AWS D1.1, ISO 3834).*
