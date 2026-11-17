---
id: manufacturing-production.metal-plastics-fabrication-production.die-casting.hpdc-porosity-control-and-die-thermal-balance
name: hpdc-porosity-control-and-die-thermal-balance
category: manufacturing-production
field: metal-plastics-fabrication-production
product: die-casting
tags: [die-casting, hpdc, high-pressure-die-casting, aluminium-die-casting, zinc-die-casting, magnesium, cold-chamber, hot-chamber, shot-profile, slow-shot, fast-shot, intensification, biscuit, porosity, gas-porosity, shrinkage-porosity, vacuum-die-casting, die-spray, release-agent, thermal-imaging, die-temperature, thermal-oil, cold-shut, soldering, heat-checking, x-ray, ct-scan, trim-press, buhler, idra, frech]
level: practitioner
status: draft
description: "Control porosity in high-pressure die casting by telling gas from shrinkage porosity, tuning the shot profile and intensification, and balancing die temperature with spray and thermal units."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HPDC porosity control and die thermal balance

**Goal:** sound castings at rate — porosity below the drawing limit in the zones that
matter (machined sealing faces, threads, structural areas) — by controlling the shot
and the die's thermal state, not by scrapping after X-ray.

## 1. First identify which porosity
Section or CT/X-ray the defect and look:
- **Gas/air porosity**: round, smooth-walled, shiny pores — trapped air, steam from
  die spray/water, lubricant decomposition. Often near last-to-fill areas and overflows.
- **Shrinkage porosity**: irregular, jagged, dendritic cavities in **thick sections**
  and hot spots — metal contracting with no feed during solidification.
The fixes are almost opposite, so guessing wastes days.

## 2. The shot profile (cold-chamber aluminium)
1. **Slow shot (phase 1)**: push metal up the shot sleeve without rolling a wave that
   traps air. Too fast → air folded in; too slow → metal cools in the sleeve (cold
   flakes). Fill of the sleeve (% fill) matters — low fill means more air.
2. **Fast shot (phase 2)**: fills the cavity in tens of milliseconds; switch-over point
   should be when metal reaches the gates. Gate velocity is the key output (range per
   alloy/part, often quoted tens of m/s — confirm your design data).
3. **Intensification (phase 3)**: pressure ramp after fill to feed shrinkage while the
   gates are still open. Late or low intensification → shrinkage porosity. Monitor
   rise time and final pressure on each shot trace.
4. **Biscuit thickness**: consistent biscuit means consistent metal dose; thin/zero
   biscuit = the plunger ran out of metal to push for intensification.
Read the **shot monitoring trace** every shift and compare to the reference trace.

## 3. Die thermal balance
- Die temperature drives fill, solidification and soldering. Use **thermal imaging**
  after die open (same point in cycle) to map the die face against the reference image.
- Hot spots → shrinkage porosity, soldering (alloy welding to the die), and heat
  checking. Address with cooling lines/jet coolers, or local spray.
- Cold areas → cold shuts, flow lines, misruns. Address with thermal-oil units,
  less spray, or overflows that bring heat.
- **Die spray** is both release and cooling. Over-spraying cools the die and leaves
  water that becomes steam (gas porosity). Use the minimum spray; blow off with air;
  check spray nozzles aren't blocked or misaimed after die change.
- Warm-up shots after a stop: castings from a cold die are scrap; run the agreed
  number of warm-up shots.

## 4. Gas porosity levers
- Vacuum assist (if fitted): check vacuum valve/chill block is clear and the vacuum
  level reaches spec before fast shot.
- Overflows and vents clear; flash in vents blocks them.
- Melt quality: degassing (rotary degasser) and dross skimming in the holding furnace;
  hydrogen in the melt contributes to porosity (more relevant to shrinkage/gas mix in
  thicker parts).
- Lubricant on plunger tip: use the right amount; excess burns into gas.

## 5. Trim and inspection
- Trim press: check trim die alignment and that trimming doesn't tear thin walls
  near porosity.
- X-ray/CT sampling per plan on critical zones; leak testing for pressure-tight parts.
- Machined-face porosity often only shows after machining — get feedback from the
  machining line by cavity and shot number.

## Gotchas
- Raising intensification pressure increases flash and die wear — address hot spots first.
- A change of release agent or dilution ratio shifts porosity and soldering.
- Shot sleeve and plunger tip wear changes slow-shot behaviour; track tip life.

## Verify
- [ ] Porosity type identified from a section or CT image.
- [ ] Shot traces match reference (slow/fast switch, intensification rise, biscuit).
- [ ] Die thermal image matches reference at the set cycle point.
- [ ] Critical-zone porosity within drawing limits on the sample plan.

*Draft: gate velocities and pressures deliberately not given numerically — alloy- and
part-specific; confirm with process engineering and the die design.*
