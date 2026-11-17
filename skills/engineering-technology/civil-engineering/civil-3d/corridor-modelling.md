---
id: engineering-technology.civil-engineering.civil-3d.corridor-modelling
name: corridor-modelling
category: engineering-technology
field: civil-engineering
product: civil-3d
tags: [civil-3d, autocad-civil-3d, autodesk, corridor, corridor-modelling, corridor-modeling, assembly, subassembly, alignment, profile, targets, regions, frequency, corridor-surface, daylight, sample-lines, cross-sections, earthworks-volumes, road-design, highway-design, data-shortcuts, subassembly-composer, civil-engineering]
level: practitioner
status: verified
description: "Build a Civil 3D corridor from alignment, profile and assemblies: frequency, targets, regions, corridor surfaces, and checking volumes before sheets."
sources: ["Autodesk Civil 3D Help: Corridors, Assemblies and Subassemblies", "Autodesk Civil 3D Subassembly Reference", "Autodesk Civil 3D Help: Data Shortcuts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Civil 3D corridor modelling — a model you can trust for volumes and sections

**Goal:** turn an alignment, a design profile and a typical section (assembly) into a
dynamic 3D corridor whose top and datum surfaces give correct earthworks volumes and
clean cross-section sheets.

## 1. Get the inputs right first
- **Existing ground (EG) surface** in its own drawing, referenced by **data shortcut**,
  not copied. Corridors in the same drawing as a heavy TIN surface are slow and fragile.
- **Alignment** with design speed set and design criteria (superelevation) applied —
  the corridor reads superelevation from the alignment, not the assembly.
- **Design (finished-grade) profile** on that alignment. Check K values and grade
  breaks before building anything; fixing the profile later rebuilds everything anyway.
- One drawing per corridor family (e.g. mainline, each side road). Keep XREF/shortcut
  links one-way: EG -> alignments -> corridor -> sheets.

## 2. Build the assembly
1. `CreateAssembly` (Home tab › Assembly). Name by typical section, e.g. `MAIN_2L_URBAN`.
2. Add subassemblies from the Tool Palette from the baseline outward: `LaneSuperelevationAOR`
   (confirmed in the Autodesk Civil 3D Subassembly Reference: lane that uses the baseline alignment's superelevation slope; attaches at the inside lane edge; codes ETW, Pave1, Base, Sub; link codes Top/Pave, Pave1, Pave2, Base, SubBase), `ShoulderExtendSubbase` (confirmed: paved shoulder whose subbase extends to a daylight point, default width 2.4 m / 8 ft) or a curb (`UrbanCurbGutterGeneral` (gated: unconfirmed, source is paywalled or blocked)), then `LinkSlopesToSurface` or `DaylightMultipleWidth` (gated: unconfirmed, source is paywalled or blocked)
   for the batters. Mirror for the other side.
3. Use **Pavement/Subbase depths** in the lane subassembly so a datum (subgrade) surface
   is created; volumes need it. Check which link code your lane uses for the bottom surface (the AOR lane page lists SubBase; whether it also carries `Datum` is unconfirmed (gated: unconfirmed, source is paywalled or blocked)).
4. Set the batter: a common default is 1V:2H cut and 1V:3H fill (or flatter for
   traversable/clear-zone fill) (gated: unconfirmed, source is paywalled or blocked); the real values come from the geotech report.
5. Give links and points consistent **codes** (Top, Datum, Pave1, ETW, Daylight). Code
   set styles and surfaces depend on them — misspelled codes are the commonest reason a
   corridor surface comes out empty.
6. For anything the stock catalogue cannot do, build a `.pkt` in **Subassembly
   Composer** rather than hand-faking with many conditional subassemblies.

## 3. Create the corridor
1. `CreateCorridor`: baseline = alignment + profile, assembly, target surface = EG.
2. **Frequency** (Corridor Properties › Parameters › Frequency): 10 m / 25 ft on tangents
   is typical for preliminary, 5 m (or less) on curves and through vertical curves (practice figures (gated: unconfirmed, source is paywalled or blocked));
   also tick "at horizontal geometry points", "superelevation critical points" and
   "profile high/low points" (all three are real Autodesk frequency options: help pages describe them; where a horizontal and a vertical setting overlap, the smaller interval is used; horizontal and superelevation settings are ignored if a feature line is the horizontal baseline). Too coarse a frequency chords curves and understates
   volumes; too fine bloats the file.
3. **Regions:** split the baseline wherever the assembly changes (intersections, bridge,
   widening). Leave a small gap rather than overlap; overlapping regions build twice.
4. **Targets** (Target Mapping): width/offset targets (edge-of-pavement alignments or
   polylines for tapers), elevation targets (profiles or feature lines for curb returns),
   surface targets for daylight. A subassembly with an unset target silently uses its
   default width — always open Target Mapping and confirm nothing reads `<None>` that
   should be set.

## 4. Corridor surfaces and boundaries
- Add a **Top** surface (from links coded Top) and a **Datum** surface (links coded
  Datum). Feature lines: add ETW, Back of Curb etc. as breaklines for better TINs.
- Add a boundary: **Corridor extents as outer boundary**. Without it the TIN triangulates
  across concave edges and inflates volumes.
- Set **Overhang correction** to Top Links / Bottom Links respectively, or the surface
  picks up the underside of curb overhangs.

## 5. Volumes and sections
1. `CreateSampleLines` along the alignment at the same frequency as the corridor (or at
   corridor stations) with swath widths beyond daylight.
2. Compute Materials with a Quantity Takeoff criteria (Cut and Fill) comparing EG to
   Datum, not Top — paving depth is not earthworks.
3. Cross-check average-end-area volumes against a **TIN-to-TIN volume surface**
   (EG vs Datum). Agreement within ~2–5% is normal (gated: unconfirmed, source is paywalled or blocked); larger gaps point to sampling
   frequency, missing boundaries or region gaps.

## Gotchas
- A corridor marked **out of date** (yellow shield in Prospector) is not reflecting the
  latest profile — rebuild before measuring anything. Avoid "Rebuild Automatic" on large
  models; rebuild deliberately.
- Superelevation transitions need the alignment's superelevation table recomputed after
  any curve edit.
- Daylight subassemblies that cannot hit the target surface stop at their max width with
  no warning in plan; look for spikes or gaps in the 3D view and the section views.
- Exact ribbon locations and subassembly names shift between releases; names above are
  from recent (2022+) releases and should be confirmed in your version's palette.

## Verify
- [ ] Corridor is up to date and Prospector shows no warnings on the corridor or surfaces.
- [ ] Target Mapping has no unintended `<None>` entries in any region.
- [ ] Top and Datum surfaces both have an outer boundary and look clean in 3D (no spikes, no triangles across the median or outside daylight).
- [ ] Section views at curves, superelevation runoff and region joins show the intended shape.
- [ ] Earthworks from sample lines agree with an EG-vs-Datum volume surface to within a few percent.
- [ ] EG and alignments are data-shortcut references, not local copies.
