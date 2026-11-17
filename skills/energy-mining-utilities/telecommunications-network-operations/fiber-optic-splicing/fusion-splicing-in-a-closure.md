---
id: energy-mining-utilities.telecommunications-network-operations.fiber-optic-splicing.fusion-splicing-in-a-closure
name: fusion-splicing-in-a-closure
category: energy-mining-utilities
field: telecommunications-network-operations
product: fiber-optic-splicing
tags: [fiber-optic-splicing, fibre-optic-splicing, telecommunications-network-operations, fusion-splicing, fusion-splicer, fujikura, sumitomo, inno, cleaver, cleave-angle, splice-loss, splice-protector, heat-shrink-sleeve, splice-tray, closure, dome-closure, inline-closure, buffer-tube, loose-tube, ribbon-fibre, mass-fusion, single-mode, g652, g657, colour-code, tia-598, bend-radius, otdr, bidirectional-otdr, restoration-splicing, fibre-cut]
level: practitioner
status: draft
description: "Fusion splice single-mode fibre into a closure: cable prep, stripping and cleaning, cleave quality, splicer loss estimates vs OTDR truth, sleeve and tray routing without bends."
sources: ["Splicer OEM manuals (Fujikura, Sumitomo — general practice, paraphrased)", "TIA-598 colour code", "ITU-T G.652/G.657"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fusion splicing in a closure

**Goal:** joint single-mode fibres in a splice closure so each splice is low-loss
(commonly specified at ≤0.1 dB, typically achieved ~0.02–0.05 dB), mechanically
protected, neatly stored and documented — on the first try, including in a
restoration at 3 a.m. in the rain.

## 1. Prepare the cable
- Confirm cable IDs and the **splice schedule** (which fibre goes to which) before
  cutting anything. Wrong fibre-to-fibre is worse than high loss.
- Strip the sheath back to the closure's specified length; secure strength members
  to the closure clamp; ground armour/metallic members to the closure's bond if
  present.
- Remove gel from loose tubes with a gel cleaner and lint-free wipes — not solvent
  that softens the tubes. Route tubes into the tray, keep the tube end inside the
  tray entry.
- Identify fibres by the **TIA-598 colour code**: blue, orange, green, brown, slate,
  white, red, black, yellow, violet, rose, aqua (tubes follow the same order). Other
  regions use different codes — check the cable spec sheet.

## 2. Strip, clean, cleave
1. Slide on the **splice protection sleeve** first. Forgetting this means re-cutting.
2. Strip the 250 µm (or 900 µm) coating with a calibrated stripper — clean, no
   nicks.
3. Clean the bare glass with ≥99 % isopropyl alcohol on a lint-free wipe; one pass,
   it should "squeak". Don't touch the glass afterwards.
4. **Cleave** with a precision cleaver at the length the splicer's holder expects
   (often 10–16 mm, set by the holder). The splicer reports cleave angle; reject
   above about **0.5–1°** (set your threshold in the splicer). Bad cleaves are the
   main cause of high loss.
5. Dispose of fibre shards into a marked container immediately — they penetrate skin
   and eyes.

## 3. Splice
- Load both fibres; core-alignment splicers align and fuse automatically. Choose
  the right program (SM-SM, G.657 bend-insensitive, dissimilar fibre).
- Watch the image: bubbles, a thin neck, a fat bulge, or a visible line at the joint
  → break and redo.
- The **estimated loss** displayed is an estimate. Accept typical values (≤0.05 dB),
  redo anything above the spec, but true loss is proven only by OTDR (section 5).
- Run the proof/tension test (the splicer's built-in pull).
- Centre the sleeve over the splice, heat-shrink in the oven, let it cool before
  handling.

## 4. Store in the tray
- Sleeve into the tray's holder, fibres coiled to the tray's minimum bend radius
  (commonly ≥30 mm for standard fibre; G.657 tolerates tighter, but follow the tray).
- No crossings under pressure, no fibre pinched by the lid. Macrobends cause high loss
  that shows at 1550/1625 nm more than 1310 nm.
- Label trays with cable and fibre ranges; close and seal per the closure maker,
  including the sealing test (air pressure valve on many closures).

## 5. Test
- OTDR at 1310 and 1550 nm (1625 nm too where macrobend risk matters). Splice loss
  from one direction can show "gainers" (negative loss) or exaggerated loss because of
  mode-field mismatch; **average both directions** for the true value.
- Record results against the splice schedule; retest any splice above spec before
  leaving the site.

## Gotchas
- Gel residue on the glass causes repeated bad cleaves. Clean again.
- Cold weather: sleeves shrink slowly, batteries drain fast; keep the splicer warm.
- Electrodes wear: arc check/calibration after replacing electrodes and when splice
  quality drifts.
- Restoration splicing: restore the highest-priority fibres first per the restoration
  list, then the rest.
- Uncertain: loss specs and bend radii differ by operator standard and product; follow
  the job spec.

## Verify
- [ ] Splice schedule checked against cable IDs before cutting.
- [ ] Every cleave angle within threshold; every splice ≤ spec estimated.
- [ ] Sleeves shrunk and cooled, fibres stored at or above minimum bend radius.
- [ ] Bidirectional OTDR loss recorded per splice at 1310/1550 nm.
- [ ] Closure sealed, labelled and pressure-tested where applicable.
