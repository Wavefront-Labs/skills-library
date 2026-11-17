---
id: manufacturing-production.printing-production.gravure-printing.cylinder-changeover-doctor-blade-and-viscosity-control
name: cylinder-changeover-doctor-blade-and-viscosity-control
category: manufacturing-production
field: printing-production
product: gravure-printing
tags: [gravure-printing, rotogravure, roto, gravure-press, flexible-packaging, publication-gravure, engraved-cylinder, chrome-plating, cylinder-changeover, cylinder-handling, doctor-blade, blade-angle, blade-pressure, blade-oscillation, hazing, streaks, solvent-ink, viscosity-control, zahn-cup, efflux-cup, automatic-viscosity-controller, solvent-retention, drying, electrostatic-assist, esa, missing-dots, snowflaking, colour-consistency, long-run]
level: practitioner
status: draft
description: "Run a rotogravure press for long-run consistency: handle and change cylinders safely, set the doctor blade, and hold solvent-ink viscosity and drying so colour does not drift across a long run."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gravure: cylinder changeover, doctor blade and viscosity control

**Goal:** keep gravure colour constant over very long runs. With engraved cylinders
the image itself does not change, so drift comes almost entirely from **ink
(viscosity, contamination), doctoring, and drying** — the three things the press crew
controls.

## 1. Cylinder handling and changeover
- Cylinders are heavy (often hundreds of kg) and the chrome surface is the product:
  move only with the proper lifting gear and cradles, never set them down on the face,
  store in racks with journals supported.
- Check each cylinder against the job: job number, colour/station, cylinder ID and
  circumference; inspect chrome for scratches, pits or worn areas (worn chrome prints
  weak highlights and shortens blade life).
- Clean cylinders after the run before ink dries in the cells — dried ink in cells
  is the most common cause of weak/missing tone on the next run.
- Pre-register (mechanical zero) cylinders on changeover; sleeve/quick-change systems
  shorten it but need the same checks.

## 2. Doctor blade setup
The blade wipes the non-image surface clean, leaving ink only in cells.
- **Blade angle** (contact angle) typically in the region of ~55–65° to the tangent
  for standard setups — follow press/blade supplier guidance; angle changes with blade
  wear and with how far the blade extends from the holder.
- **Pressure:** the lightest that wipes clean. Too high → blade and cylinder wear,
  streaks, heat. Too low → **hazing** (a light tint in non-image areas).
- **Oscillation** on: moves the blade side to side to spread wear and dislodge
  particles. Check it is running.
- New blades need a short wear-in; lamella-tip steel or plastic blades vary — set per
  type.
- **Streaks** (thin lines in print direction) usually mean a nick in the blade from a
  particle: change or hone the blade and **filter the ink** — the particle will come
  back otherwise.

## 3. Solvent ink viscosity
Gravure inks are low-viscosity solvent (or water) systems; solvent evaporates from
the open ink pan continuously, so viscosity rises during the run and density with it.
- Measure with an **efflux cup** (Zahn #2, Shell, DIN or Ford cup per site standard),
  in seconds, **at a recorded temperature** — viscosity is strongly temperature
  dependent.
- Use **automatic viscosity controllers** where fitted; check them against a manual
  cup reading each shift, and keep the solvent blend they add correct.
- Add the specified solvent **blend** (e.g. ethanol/ethyl acetate ratios for packaging
  inks, per supplier), not whatever solvent is closest. The wrong blend changes drying
  speed and can cause blushing or poor adhesion.
- Keep pans topped up with fresh ink in small additions; long-recirculated ink picks
  up contamination and drifts in shade.

## 4. Drying and solvent retention
- Dryer temperature and airflow per station: under-dry → set-off, blocking in the
  reel, odour and **retained solvent** (a food-packaging compliance issue — tested by
  headspace GC against customer limits).
- Over-dry / ink drying in cells → **missing dots** and loss of highlights. Retarder
  solvent slows cell drying; use per supplier advice.
- **Electrostatic assist (ESA)** improves ink pull-out from small cells on rough or
  hard stocks, reducing "snowflaking"/missing dots. Check it is on and set.

## 5. Long-run consistency routine
- Measure colour (spectro, ΔE to the approved standard) at set intervals; log viscosity
  and temperature alongside so you can see cause and effect.
- Investigate any trend before it leaves tolerance — usually viscosity creep or a
  dryer change.

## Gotchas
- Chasing density with blade pressure instead of viscosity.
- Measuring cup viscosity on ink that has cooled in the cup — time it immediately.
- Solvent vapours are flammable and harmful: earth/bond containers, keep pans covered,
  respect zone and extraction rules.

## Verify
- [ ] Cylinders checked against job, inspected, pre-registered.
- [ ] Blade angle and lightest clean-wiping pressure set; oscillation running.
- [ ] Viscosity measured with the site cup at recorded temperature; controller verified.
- [ ] Dryers set; retained solvent tested where required.
- [ ] ΔE log shows the run within tolerance from start to end.

*Draft note:* blade angles and solvent blends are typical; use press, blade and ink
supplier specifications for actual settings.
