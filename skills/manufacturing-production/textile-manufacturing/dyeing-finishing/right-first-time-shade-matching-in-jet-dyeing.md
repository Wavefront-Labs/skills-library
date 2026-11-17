---
id: manufacturing-production.textile-manufacturing.dyeing-finishing.right-first-time-shade-matching-in-jet-dyeing
name: right-first-time-shade-matching-in-jet-dyeing
category: manufacturing-production
field: textile-manufacturing
product: dyeing-finishing
tags: [dyeing-finishing, dyehouse, jet-dyeing, soft-flow, jigger, pad-batch, exhaust-dyeing, reactive-dyes, disperse-dyes, cotton, polyester, liquor-ratio, recipe, lab-dip, bulk-correction, add, shading-addition, rft, right-first-time, spectrophotometer, delta-e, cmc, d65, metamerism, light-box, shade-band, levelness, rope-marks, crease-marks, stenter, heat-setting, colour-fastness, color-matching, datacolor]
level: practitioner
status: draft
description: "Get dye lots right first time on jet machines: lab-to-bulk recipe correction, process control that matters (liquor ratio, salt/alkali dosing, temperature ramp), spectro shade checks and adds."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Right-first-time shade matching in jet dyeing

**Goal:** a dye lot that matches the approved standard without adds (shading additions)
or re-dyes. Every add costs time, water, energy and often levelness. Dyehouses measure
this as **RFT %** — the lot's shade passes at first assessment.

## 1. From lab dip to bulk
- The customer approves a **lab dip** (small dyed sample) against their standard,
  usually assessed in a light box under the specified illuminant (often D65 plus a
  secondary like TL84/A to check metamerism).
- Bulk rarely dyes exactly like the lab. Keep a **lab-to-bulk correction factor** per
  machine type, substrate and dye class from past lots and apply it to the recipe.
- Use the **same fabric batch** (same greige lot, same preparation) as bulk for the lab
  dip; a different bleach or mercerisation level changes dye uptake.

## 2. Process control that decides the shade
For reactive dyes on cotton (exhaust, jet/soft-flow):
- **Liquor ratio** (fabric weight : water) — weigh the batch accurately and fill to
  the right level. A wrong batch weight is a wrong recipe.
- **Pretreatment** consistency: absorbency, residual peroxide (kills reactive dyes),
  pH, whiteness.
- **Salt** and **alkali** dosing — amount and **dosing profile** (progressive dosing)
  controls exhaustion and fixation; dumping alkali gives unlevel dyeing.
- **Temperature** gradient and hold time per the recipe; ramp too fast → unlevel.
- **Water quality**: hardness, metals (iron, copper) — affects shade and brightness.
- **Washing-off/soaping** after dyeing removes hydrolysed dye; poor wash-off gives a
  shade that changes later and bad wet fastness.
For polyester (disperse, high-temperature jets ~130 °C): heating rate through the
critical range, dispersing/levelling agents, and reduction clearing after dyeing.
Automatic dispensing systems (dyes and chemicals) remove a big source of human error —
verify their calibration.

## 3. Assessing the shade
- Take a sample at the end of dyeing (before unloading), dry it in a consistent way
  (wet samples read darker), condition it.
- **Spectrophotometer**: measure against the standard; report **ΔE CMC (2:1)** or the
  customer's formula, plus components (lighter/darker, redder/greener, yellower/bluer,
  brighter/duller).
- **Visual** check in the light box under the specified illuminants — the instrument
  doesn't overrule a visible metameric mismatch.
- Typical pass tolerance is around ΔE CMC ≤ 1.0 but customers define their own.

## 4. Making an add
- Calculate the add from the spectro's correction suggestion, scaled to the bulk
  correction factor; adds are usually small fractions of the original recipe.
- Add dye at the right temperature/conditions so it levels; reactive adds after
  fixation are less effective — some colours can't be corrected and need stripping.
- Record every add against the lot: it feeds the lab-to-bulk factors for next time.

## 5. Machine-related faults
| Fault | Cause |
|---|---|
| **Rope/crease marks** | Fabric running too long in one fold, low nozzle pressure, cooling too fast |
| Unlevel/patchy | Fast dosing or ramp, poor pretreatment, insufficient circulation |
| Shade variation end-to-end of lot | Different greige lots in one batch; circulation |
| Spots | Undissolved dye, foam, contamination |

## 6. Finishing affects shade too
Stenter heat setting, softeners and resin finishes shift shade slightly. Approve shade
on **finished** fabric where the customer assesses finished goods; keep a shade band
per lot.

## Verify
- [ ] Batch weight and liquor ratio recorded; recipe includes the lab-to-bulk factor.
- [ ] Dosing and temperature profile followed (machine log).
- [ ] Shade within ΔE tolerance and visually acceptable under specified illuminants.
- [ ] Adds recorded; RFT % tracked per machine/shade family.

*Draft: tolerance values and illuminant choices are customer-defined; dye chemistry
summarised, not a recipe.*
