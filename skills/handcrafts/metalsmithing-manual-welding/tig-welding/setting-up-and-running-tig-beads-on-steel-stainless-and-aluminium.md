---
id: handcrafts.metalsmithing-manual-welding.tig-welding.setting-up-and-running-tig-beads-on-steel-stainless-and-aluminium
name: setting-up-and-running-tig-beads-on-steel-stainless-and-aluminium
category: handcrafts
field: metalsmithing-manual-welding
product: tig-welding
tags: [tig-welding, tig, gtaw, heliarc, tungsten, lanthanated-tungsten, 2-percent-lanthanated, ceriated, pure-tungsten, argon, shielding-gas, gas-lens, cup-size, dcen, ac-balance, ac-frequency, foot-pedal, amperage, filler-rod, er70s-2, er308l, er316l, er4043, er5356, mild-steel, stainless-steel, aluminium, aluminum, thin-section, sugaring, back-purge, contamination, welding]
level: practitioner
status: draft
description: "Set up a TIG machine for mild steel, stainless and aluminium (tungsten, polarity, amps, gas, filler), then run a consistent bead with steady arc length, torch angle and rod dipping."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting up and running TIG beads on steel, stainless and aluminium

**Goal:** lay a clean, evenly rippled TIG bead with full fusion on 1–3 mm material,
with the machine set correctly for the metal so the weld is sound, not just pretty.

## 1. Machine set-up by metal

| | Mild steel | Stainless | Aluminium |
|---|---|---|---|
| Polarity | DCEN | DCEN | AC |
| Tungsten | 2% lanthanated (gold/blue tip) | 2% lanthanated | 2% lanthanated (modern inverter) or pure on old transformers |
| Tip | Sharp point, length 2–2.5× diameter | Sharp point | Small flat or slight ball |
| Filler | ER70S-2 or -6 | ER308L (304), ER316L (316) | ER4043 general, ER5356 for 5xxx alloys/anodising |
| Rough amps | ~1 A per 0.025 mm (1 A/thou) | ~10–20% less than steel | ~1.2–1.5× steel |

- The "1 amp per thousandth of an inch" rule is a starting point, not a setting:
  1.6 mm steel ≈ 60–70 A on the pedal; 3 mm ≈ 110–125 A. Set the machine max
  about 25% above and ride the pedal.
- **Tungsten size:** 1.6 mm (1/16") up to ~150 A; 2.4 mm (3/32") above.
- **Gas:** pure argon, 7–10 L/min (15–20 CFH) with a #7–#8 cup; gas lens lets you
  stick the tungsten out further (up to ~10 mm) for corners. Post-flow ~1 s per
  10 A (protects the tungsten as it cools).
- **AC (inverter):** balance around 65–75% EN (cleaning action shown as a frosted
  band either side of the bead — widen it with more EP if the puddle is dirty);
  frequency 100–150 Hz for a tight arc. Exact labels vary by maker — check the manual.

## 2. Preparation — most TIG faults start here
- Grind tungsten **lengthwise** on a dedicated wheel (grind marks pointing to the tip).
- Steel: grind or flap-disc to bright metal; remove mill scale.
- Stainless: stainless-only brush and disc; degrease with acetone.
- Aluminium: degrease, then stainless brush just before welding (oxide re-forms
  within hours). Keep filler rod clean in a tube.
- Fit-up gap ≈ zero for thin sheet; tack every 25–50 mm.

## 3. Torch and filler technique
1. Brace the torch hand on the bench or work; comfort decides consistency.
2. **Arc length** ≈ the tungsten diameter (1.5–2.5 mm). Longer = wide, hot, dirty.
3. **Torch angle:** 10–20° from vertical, pointing in the direction of travel (push).
4. Strike (HF or lift arc), hold until a shiny puddle forms of the bead width you want.
5. **Rod** at 15–20° to the surface, its tip held in the gas shield. Dab it into the
   **leading edge** of the puddle — never touch it to the tungsten — then pull it
   back slightly; move the torch forward one ripple. Rhythm: dip, move, dip.
6. At the end, ramp down on the pedal (or crater-fill) while adding a last dab, then
   keep the torch over the crater through post-flow.
- Aluminium needs more pedal at the start (cold mass) and less as heat builds.

## 4. Faults
- **Tungsten contaminated** (balled grey, arc wanders): stop, break off and regrind.
  Do not weld on.
- **Grey, sooty or "sugared" stainless back side:** needs an argon **back purge** for
  full penetration on stainless; front discolouration beyond straw/light blue =
  too hot or too little gas.
- **Porosity:** draughts, gas leak, dirty metal or rod, too little or too much flow
  (turbulence above ~15 L/min with a small cup).
- **Black specks in aluminium bead:** oxide not cleaned, or balance too far to EN.
- **Undercut:** too hot or too little filler at the toes.
- **Cracking in aluminium:** wrong filler (e.g. 4043 on 5xxx anodised work, or no
  filler on 6061 — autogenous welds on 6xxx crack).

## Safety
UV from TIG is intense: auto-darkening helmet shade 10–13 for these currents, full
skin cover (TIG burns skin like sunburn). Thoriated (red) tungsten is mildly
radioactive — grind with extraction or use lanthanated. Hexavalent chromium fume
from stainless: extraction. Grind tungsten with eye protection. HF start can upset
nearby electronics and pacemakers.

## Verify
- [ ] Polarity, tungsten type and tip, filler and gas match the metal.
- [ ] Tungsten clean and freshly ground lengthwise.
- [ ] Bead width consistent ±0.5 mm; ripples even; no undercut.
- [ ] Penetration visible on the back for butt joints (purged on stainless).
- [ ] Cut-and-etch or bend test on a scrap coupon before trusting a structural weld.
