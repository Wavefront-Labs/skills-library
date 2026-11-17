---
id: engineering-technology.technical-drawing-cad.gd-t.position-tolerancing-with-datums
name: position-tolerancing-with-datums
category: engineering-technology
field: technical-drawing-cad
product: gd-t
tags: [gd-t, gdt, gps, geometric-tolerancing, true-position, position-tolerance, datums, datum-reference-frame, drf, 3-2-1, feature-control-frame, basic-dimensions, ted, mmc, lmc, rfs, mmb, bonus-tolerance, virtual-condition, datum-shift, floating-fastener, fixed-fastener, composite-position, rule-1, envelope-principle, independency-principle, asme-y14.5, asme-y14.5-2018, iso-1101, iso-5459, iso-2692, iso-8015, inspection, cmm, functional-gauge]
level: advanced
status: draft
description: "Author and read position tolerances: datum selection (3-2-1), feature control frames, MMC bonus/virtual condition, ASME Y14.5-2018 Rule 1 vs ISO 8015 independency."
sources: ["ASME Y14.5-2018 (scope and concepts, paraphrased)", "ISO 1101, ISO 5459, ISO 2692, ISO 8015 (scope and concepts, paraphrased)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Position tolerancing with a datum reference frame

**Goal:** locate holes, pins and slots so that every part that passes inspection
assembles, while giving manufacturing the largest tolerance that function allows.

## 1. Know which rulebook the drawing invokes
The symbols look nearly identical in ASME and ISO; the defaults do not.
- **ASME Y14.5-2018:** **Rule #1** (envelope): the size limits of a regular feature of
  size also bound its form, so a shaft at MMC must be perfectly straight. Waive it per
  feature with the independency symbol (circled I). Tolerances apply RFS unless MMC/LMC
  is shown (Rule #2). Located features use **basic dimensions** (boxed).
- **ISO GPS (ISO 8015):** **independency principle** by default: size controls local
  size only, form is uncontrolled unless toleranced. Use the envelope modifier
  (circled E) where a fit needs it. Referencing any ISO GPS standard invokes the whole
  GPS system. Boxed dimensions are **theoretically exact dimensions (TEDs)**. Geometric
  tolerancing is ISO 1101, datums ISO 5459, the material requirements (M/L) ISO 2692.
- Datum establishment and some verification details differ between the systems, so
  a CMM program written for one can give different results on the other. Write the
  standard and edition in the title block.

## 2. Build the datum reference frame from function
1. **Primary datum** = the surface the part sits on in assembly (largest, most stable
   mating face). It removes 3 degrees of freedom (3 contact points minimum).
2. **Secondary** = the next locating feature, often a pilot bore or an edge; it
   removes 2 more.
3. **Tertiary** = the clocking feature; removes the last rotation.
That is the 3-2-1 frame. Order matters: `| A | B | C |` is a different part from
`| B | A | C |`. Choose datum features that are accessible to fixture and measure, and
that the mating part actually touches.

## 3. Write the feature control frame
For a 4-hole pattern on a flange:
```
4X  Ø10.0-10.2
[ position | Ø0.2 (M) | A | B | C ]
```
- Locate the holes with basic dimensions (PCD, angles) from the datums; **no**
  plus/minus on those.
- Use the diameter symbol for a cylindrical zone; omit it for a slot-width zone.
- Add MMC (circled M) whenever the requirement is assemblability: it is the
  setting that makes a functional gauge possible.

## 4. Bonus tolerance and virtual condition (worked numbers)
Hole Ø10.0-10.2, position Ø0.2 at MMC.
| Actual hole | Departure from MMC | Allowed position |
|---|---|---|
| 10.00 | 0.00 | Ø0.20 |
| 10.10 | 0.10 | Ø0.30 |
| 10.20 (LMC) | 0.20 | Ø0.40 |
**Virtual condition** (hole) = MMC - position tol = 10.0 - 0.2 = **Ø9.8**. A gauge pin of
Ø9.8 at true position checks every hole.

Fastener sizing:
- **Floating fastener** (clearance holes in both parts, nut and bolt): `T = H - F`.
  M8 bolt (F = 8.0), holes MMC H = 8.4: T = Ø0.4 in each part.
- **Fixed fastener** (one part threaded or press-fit): `T1 + T2 = H - F`, e.g. Ø0.2
  each. Add projected tolerance zone (circled P plus height) on the threaded part
  when the screw's perpendicularity matters beyond the hole depth.

## 5. Datum features of size at MMB
Referencing a bore datum as `B (M)` (ASME: maximum material boundary) lets the
pattern shift as a group when the bore departs from MMB. This **datum shift** is not
simple per-hole bonus; it moves the whole pattern relative to B. Gauges get it for
free; CMM software must be told to apply it, or you reject good parts.

## 6. Pattern refinements
- **Composite position** (two-tier frame): upper tier locates the pattern to the
  datums loosely; the lower tier controls hole-to-hole spacing tightly, usually
  referencing only the primary.
- Several patterns referencing the same datums in the same order and modifiers are
  treated as one simultaneous requirement by default in ASME; state SEP REQT to
  separate them.

## Gotchas
- Position needs located features of size. Using it on a flat surface is an error;
  that is profile of a surface.
- Concentricity and symmetry were removed in Y14.5-2018; use position or profile.
  ISO still has coaxiality and symmetry symbols with their own meaning.
- RFS everywhere is legal but expensive: no bonus and no hard gauge.

## Verify
- [ ] Standard and edition stated; Rule #1 vs independency understood for every fit.
- [ ] Datum order matches how the part is located in assembly.
- [ ] Every positioned feature is located by basic/TED dimensions only.
- [ ] Virtual condition of holes and pins computed and assembly checked at worst case.
- [ ] Inspection plan says how datum shift (MMB) is applied.
