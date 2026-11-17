---
id: natural-sciences.biology.cell-culture.aseptic-technique-and-contamination-control
name: aseptic-technique-and-contamination-control
category: natural-sciences
field: biology
product: cell-culture
tags: [cell-culture, tissue-culture, aseptic-technique, sterile-technique, biosafety-cabinet, bsc, class-ii-cabinet, laminar-flow, contamination, mycoplasma, mycoplasma-testing, bacterial-contamination, fungal-contamination, yeast, cross-contamination, cell-line-authentication, str-profiling, incubator-cleaning, passaging, antibiotics, pen-strep, 70-percent-ethanol, mammalian-cells]
level: practitioner
status: draft
description: "Work in a Class II biosafety cabinet without contaminating mammalian cultures: hood workflow, spotting bacteria/fungi/mycoplasma, testing routine, and what to do when a flask goes bad."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aseptic technique and contamination control in cell culture

**Goal:** keep cultures free of bacteria, fungi, mycoplasma and other cell lines, and
catch contamination early enough that it does not spread through the incubator or
invalidate months of data.

## 1. The hood session
1. Cabinet on and running for the manufacturer's purge time (often ~5–15 min) before
   use; sash at the marked working height. Do not work with the sash raised above it —
   that breaks the air curtain.
2. Wipe the work surface, then every bottle and box as it goes in, with 70 % ethanol
   (70 % works better than absolute ethanol because water aids penetration). Let it
   evaporate before opening anything.
3. Load only what this session needs. Clutter blocks the front and rear grilles and
   disrupts airflow. Work at least ~10 cm inside the front edge.
4. One cell line at a time. Separate media bottles per line, or at least never put a
   pipette that has touched cells back into a shared bottle. This is the main defence
   against cross-contamination (e.g. HeLa overgrowing another line).
5. Never pass hands or arms over open vessels; keep caps face-down or held; open
   vessels only as long as needed.
6. Slow, deliberate movements; rapid arm movements in and out pull room air in.
7. Afterwards: remove everything, wipe down, run the purge time, then close. Do not
   rely on cabinet UV lamps as a substitute for wiping — their effect is limited to
   directly exposed surfaces and declines as the lamp ages.

Many labs avoid open flames in Class II cabinets: they disrupt the laminar airflow and
are a fire risk with ethanol. Follow your institution's biosafety rules.

## 2. Recognising contamination
| Type | What you see | Timeline |
|---|---|---|
| Bacteria | Medium cloudy, often turns yellow (acidic) quickly; shimmering particles between cells at 20–40× | Overnight to 1–2 days |
| Yeast | Round/oval budding particles, medium turbid later; pH change slower | Days |
| Mould | Filaments (hyphae), sometimes floating fuzzy clumps | Days |
| Mycoplasma | **Nothing visible.** Medium clear; subtle slowed growth, altered morphology or transfection efficiency | Persistent, chronic |
| Cross-contamination | Morphology drifts; growth rate changes | Weeks–months |

Mycoplasma is the dangerous one because you cannot see it and antibiotics such as
penicillin do not touch it (it has no cell wall).

## 3. Routine testing
- **Mycoplasma:** test every line on arrival (quarantine it until negative) and on a
  schedule — monthly or quarterly is common — plus before freezing banks and publishing.
  PCR-based kits and luminescence (enzyme-based) kits are fast; DAPI/Hoechst staining
  shows extranuclear speckles but needs experience. Culture the sample without
  antibiotics for a few days before testing if the kit says so.
- **Authentication:** STR profiling for human lines on receipt and before publication;
  many journals now ask for it. Compare against a reference database (e.g. Cellosaurus/ATCC).
- **Low-passage banks:** freeze a master bank early; work from it and discard working
  cultures after a fixed number of passages.

## 4. When a flask is contaminated
1. Do not open it in the hood you use for clean lines. Add bleach (or your lab's
   disinfectant) to the flask and discard as biohazard.
2. Check the other flasks from the same session and same media bottles; discard the
   shared media/reagents that were open.
3. Clean the incubator: water pan is the usual fungal reservoir — empty, disinfect,
   refill with sterile distilled water (some labs add a pan disinfectant). Wipe shelves.
4. Thaw a fresh vial from the bank rather than trying to rescue, unless the line is
   irreplaceable — mycoplasma elimination reagents exist but take weeks and must be
   followed by re-testing.

## Gotchas
- **Routine antibiotics mask poor technique.** Pen-strep keeps low-level bacterial
  contamination suppressed and hides cryptic infections; many labs culture without it
  and add it only for primary cells or short-term work.
- Sharing pipettors between the bench and the hood carries contamination in; keep a
  dedicated set.
- Water baths are filthy: wipe bottles dry and spray with ethanol after warming, or use
  a bead bath.
- Gloves sprayed with ethanol still carry contamination if you then touch your face, phone
  or the sash handle.

Unconfirmed here: specific purge times and testing intervals vary by cabinet model and
institutional policy; check your local biosafety manual.

## Verify
- [ ] Every active line has a negative mycoplasma test within your lab's interval.
- [ ] Human lines have an STR profile on file that matches the reference.
- [ ] One line per hood session; no shared media between lines.
- [ ] Incubator water pan cleaned on schedule and logged.
- [ ] Contaminated cultures were bleached and discarded, not "rescued" silently.
