---
id: hospitality-culinary.brewing.mashing-and-wort-production.running-the-mash-lauter-and-boil
name: running-the-mash-lauter-and-boil
category: hospitality-culinary
field: brewing
product: mashing-and-wort-production
tags: [brewing, mashing-and-wort-production, hot-side, mashing, single-infusion, step-mash, decoction, mash-temperature, strike-water, beta-amylase, alpha-amylase, fermentability, lautering, vorlauf, recirculation, sparging, fly-sparge, batch-sparge, stuck-mash, rice-hulls, boil, hot-break, dms, boil-off, whirlpool, wort-chilling, heat-exchanger, refractometer, hydrometer, gravity-correction, pre-boil-gravity, brew-day, mash-tun]
level: practitioner
status: draft
description: "Run the hot side of a brew day: strike temperature, mash rests for fermentability, vorlauf and sparge without a stuck mash, a vigorous boil, chilling, and correcting gravity on the fly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running the mash, lauter and boil — hitting gravity and fermentability

**Goal:** clear, fermentable wort at the planned volume and gravity, chilled and in the
fermenter quickly, with no stuck mash and no surprises.

## Mash
- **Strike temperature:** water must be hotter than the target mash temperature because
  cold grain absorbs heat. Common estimate (US units): `Tstrike = (0.2 ÷ R) × (Tmash − Tgrain) + Tmash`
  where R = water-to-grain ratio in qt/lb (typical 1.25–1.5; about 2.6–3.1 L/kg).
  Then tune for your tun's heat loss — preheat the tun.
- **Temperature sets fermentability:**
  - 62–65 °C favours beta-amylase → more fermentable, drier beer.
  - 66–68 °C middle ground for most ales.
  - 68–70 °C favours alpha-amylase → more dextrins, fuller body, higher FG.
- Rest 45–60 min. Modern, well-modified malts don't need a protein rest; step mashes
  (e.g. 63 → 72 °C) tune body and foam; decoction is for tradition and Maillard depth.
- Stir thoroughly to break up dough balls; check temperature in several spots after 5 min.
- Check **mash pH** (5.2–5.6) about 15 min in — see the grain-bill skill for corrections.
- Optional iodine test: no blue-black on a white plate = starch converted.

## Lauter
1. **Vorlauf:** recirculate the first runnings gently until they run clear of grain bits (5–15 min).
2. **Run off slowly** — a fast draw compacts the bed. Keep liquid above the grain bed.
3. **Sparge** at ~75–78 °C (stops conversion, eases flow). Fly sparge: matching inflow to
   outflow. Batch sparge: add all sparge water, stir, vorlauf, drain.
4. **Stop collecting** when runnings fall to ~1.008–1.010 gravity or pH rises above ~5.8–6.0;
   past that you extract tannins (astringency).
- **Stuck mash:** high proportions of wheat, oats or rye; fine crush; too-fast runoff.
  Prevention: 3–5% rice hulls, coarser crush. Cure: stop draining, underlet hot water
  from below, gently stir, re-vorlauf.

## Measure pre-boil and correct
Measure pre-boil volume and gravity (refractometer readings need wort correction
factor; hydrometers need temperature correction to calibration, usually 20 °C).
- Low gravity → extend the boil (lose more water) or add DME/sugar.
- High gravity → top up with water to the planned OG at the end.
Gravity points × volume is conserved: `GP_pre × V_pre = GP_post × V_post`.

## Boil
- Rolling, vigorous boil, uncovered, typically 60 min (90 min for pilsner malt to drive off
  DMS — a sweetcorn off-flavour). A lid traps DMS back in.
- Watch for **boil-over at hot break** (foam just as it comes to the boil); have a spray of
  water and lower heat briefly.
- Measure boil-off rate per hour on your system and log it.
- Add kettle finings (Irish moss/Whirlfloc) ~10–15 min before end; yeast nutrient same time.

## Chill and transfer
- Whirlpool to cone the trub, rest 10–20 min (hops in whirlpool add aroma and some IBU).
- Chill to pitching temperature fast (plate/counterflow chiller or immersion) — slow
  cooling means more DMS and infection risk.
- **Everything after the chiller is cold side: sanitise it.** Aerate/oxygenate wort for
  the yeast (see fermentation skill).

## Verify
- [ ] Mash temperature within ±1 °C of target, pH in range, conversion complete.
- [ ] Runnings clear; collection stopped before tannins.
- [ ] OG within ±2 points and volume within ±5% of plan; efficiency logged.
- [ ] Wort chilled to pitch temperature within ~30–45 min (homebrew) and sanitised path.

*Status draft: strike formula and temperature bands are the common homebrew/craft references.*
