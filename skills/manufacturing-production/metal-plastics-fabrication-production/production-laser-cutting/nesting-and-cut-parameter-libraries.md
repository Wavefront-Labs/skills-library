---
id: manufacturing-production.metal-plastics-fabrication-production.production-laser-cutting.nesting-and-cut-parameter-libraries
name: nesting-and-cut-parameter-libraries
category: manufacturing-production
field: metal-plastics-fabrication-production
product: production-laser-cutting
tags: [production-laser-cutting, laser-cutting, fibre-laser, fiber-laser, co2-laser, turret-punch, punch-laser-combo, trumpf, bystronic, amada, salvagnini, mazak, nesting, sigmanest, lantek, trutops, bysoft, common-line-cutting, micro-joints, tabs, lead-in, pierce, nitrogen-cutting, oxygen-cutting, dross, kerf, cut-parameter-library, technology-tables, nozzle, focus-position, tip-up, part-sorting, load-unload-automation, sheet-metal]
level: practitioner
status: draft
description: "Get yield and uptime from production laser/punch cells: nesting rules, micro-joints and lead-ins, cut technology tables for N2 vs O2, nozzle and focus care, and lights-out sorting pitfalls."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nesting and cut parameter libraries

**Goal:** high sheet utilisation and long unattended runs on a laser (or punch/laser)
cell, without tip-ups, collisions or bad edges on the night shift. Two things make this
work: **nesting rules** that suit automation, and a **controlled parameter library**.

## 1. Nesting for production
In the CAM/nesting software (Lantek, SigmaNEST, TruTops Boost, BySoft, Amada VPSS etc.):
- **Utilisation** matters, but parts that tip up and hit the head cost more than the
  scrap you saved. Balance it.
- **Micro-joints/tabs**: hold small parts in the skeleton for downstream removal,
  or leave them free for drop-through/sort. Choose per part size and the sorting
  system. Tabs on visible edges need deburring — put them on hidden edges.
- **Lead-ins** away from the finished edge (into scrap), pierce not on the part line;
  for small holes, lead-in length to suit the material thickness.
- **Common-line cutting** saves time and material on rectangular parts but needs
  consistent kerf; avoid on parts with tight tolerance on that edge.
- **Cut order**: inner contours before outer; cut sequence that avoids the head
  crossing already-cut (tipped-up) parts; head-up moves over cut areas.
- **Remnants**: record and reuse remnant sheets in the material inventory.
- Grain direction (brushed stainless) and protective film side respected.

## 2. Cut parameter (technology) libraries
Machines ship with technology tables per material/thickness/gas. Production practice:
- Keep a **site-controlled library**: approved modified parameters, versioned,
  changes logged with reason. Operators adjusting tables ad hoc creates parts that
  can't be reproduced.
- **Nitrogen** (fusion) cutting: clean, oxide-free edges on stainless and aluminium (and
  thin mild steel for paint/weld-ready edges). High gas consumption; edge burr/dross
  tells you about pressure/focus.
- **Oxygen** (flame) cutting mild steel: faster on thick plate, oxide layer on edge
  (may need removal before powder coat or welding — check the drawing/finish spec).
- **Compressed air** cutting on thin material is cheap but leaves some oxidation.
- Check material spec: surface scale, coatings, and alloy all change behaviour;
  a "same thickness" sheet from a new supplier can need retuning.

## 3. Daily head care
- **Nozzle**: inspect and clean; damaged/spattered nozzle → asymmetric cut, dross on
  one side. Run **nozzle centring** after change.
- **Protective window** (cover slide): inspect for spatter/burns; a dirty window
  scatters power and can crack.
- **Focus position** check (many machines auto-calibrate).
- Capacitive height sensing calibration.

## 4. Automation (load/unload, towers, sorting)
- Sheet separation (fanning magnets/air) and double-sheet detection working —
  double sheets jam or crash.
- **Part sorting** grippers/suction need flat, fully separated parts; tabs and
  micro-joints must suit the sorting method.
- Skeleton handling: thin skeletons tear and jam the unloader; leave a frame wide
  enough.
- Run a new program attended for the first sheet before letting it run lights-out.

## 5. Turret punching notes
Tool library (punch/die clearance by thickness), tool sharpening/hit counts, forming
tools hit last and up-forms avoided under the stripper path, slug pulling control.

## Verify
- [ ] First sheet of each new nest run attended: no tip-ups, sorting succeeds.
- [ ] Parameters used are from the controlled library version.
- [ ] Edge quality (dross, burr, oxide) meets the finish spec for the gas used.
- [ ] Nozzle, window and centring checked at shift start.

*Draft: vendor software and table names illustrative; cutting values intentionally
omitted (machine power and table-specific).*
