---
id: engineering-technology.materials-engineering.metallurgy-heat-treatment.steel-heat-treatment-design
name: steel-heat-treatment-design
category: engineering-technology
field: materials-engineering
product: metallurgy-heat-treatment
tags: [materials-engineering, metallurgy-heat-treatment, metallurgy, heat-treatment, steel, iron-carbon-diagram, fe-c-phase-diagram, austenitising, austenitizing, quenching, tempering, quench-and-temper, hardenability, jominy, end-quench-test, astm-a255, ttt-diagram, cct-diagram, martensite, ideal-critical-diameter, carbon-equivalent, normalising, normalizing, annealing, temper-embrittlement, quench-cracking, decarburisation, decarburization, weldability]
level: practitioner
status: gated
description: "Design a steel quench-and-temper schedule: read the Fe-C diagram, set austenitising temp, check hardenability with Jominy data, choose quenchant and tempering."
sources:
  - "ASM Handbook, Vol. 4: Heat Treating (ASM International)"
  - "Krauss, Steels: Processing, Structure, and Performance"
  - "Bhadeshia and Honeycombe, Steels: Microstructure and Properties"
  - "ASTM A255, Standard Test Methods for Determining Hardenability of Steel"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Steel heat-treatment design — quench and temper to a hardness spec

**Goal:** turn a drawing callout ("4140, 28–32 HRC through section") into a schedule
a heat treater can run, with a check that the section can actually harden and that
the part will not crack or embrittle on the way.

## 1. Read the Fe–C diagram for the grade
Key lines (plain carbon, approximate — alloying shifts them; use the grade's datasheet):
- **A1** ≈ 727 °C (eutectoid 727 °C and about 0.77 % C seen in sources, not in an authoritative free handbook): eutectoid; below it ferrite + cementite are stable.
- **A3**: ferrite fully gone; falls from ~912 °C at 0% C to 727 °C at ~0.77% C (gated: unconfirmed, source is paywalled or blocked).
- **Acm**: cementite solvus for hypereutectoid steels.

**Austenitising temperature:** hypoeutectoid steels A3 + 30–50 °C (e.g. 1045 ≈
840–860 °C; 4140 ≈ 845–870 °C; typical handbook ranges (gated: unconfirmed, source is paywalled or blocked)). Hypereutectoid tool/bearing steels are usually
austenitised between A1 and Acm (e.g. 52100 ≈ 830–860 °C (gated: unconfirmed, source is paywalled or blocked)) to keep some carbides and
avoid excess retained austenite. Soak roughly 1 h per 25 mm of section after the
core reaches temperature (rule of thumb; follow the specification if it says otherwise).

## 2. Check hardenability before choosing a quench
As-quenched martensite hardness depends almost only on carbon (roughly 0.2% C →
~50 HRC, 0.4% C → ~57–60 HRC, ≥0.6% C → ~64–66 HRC; figures (gated: unconfirmed, source is paywalled or blocked)). Whether the **core** reaches it
depends on hardenability:
1. Get the grade's **Jominy band** (end-quench test per ASTM A255 / ISO 642): hardness
   vs distance from the quenched end. Use the lower band edge for design.
2. Convert your section to an equivalent Jominy distance using published
   bar-diameter vs J-distance charts for the quenchant (water, agitated oil, polymer).
   Centre of a 50 mm round in agitated oil corresponds to roughly J ≈ 12–16 mm
   (chart-dependent; verify (gated: unconfirmed, source is paywalled or blocked)).
3. Read hardness at that distance. Common criterion: ≥ 50% martensite at the centre
   for general parts, ≥ 90% for highly stressed shafts and springs.
4. If short, choose a more hardenable grade (1045 → 4140 → 4340) rather than a more
   severe quench. Grossmann's ideal critical diameter D_I calculation from composition
   is an alternative estimate.

## 3. Choose the quenchant
Severity (Grossmann H, approximate (gated: unconfirmed, source is paywalled or blocked)): still oil ~0.25–0.3, agitated oil ~0.5–0.8,
still water ~1, agitated brine ~2–5. Polymer (PAG) solutions sit between oil and
water depending on concentration. Rule: the mildest quench that meets hardness.
Water-quenching medium-carbon alloy steels with sharp corners invites cracks.

## 4. Temper — always, and promptly
Move parts to the tempering furnace as soon as they are hand-warm (~50–70 °C) and
within an hour or two of quenching; leaving as-quenched martensite at room temperature
risks delayed quench cracking. Typical 4140 tempering response, approximate (gated: unconfirmed, source is paywalled or blocked) (use the grade's tempering curve):

| Temper °C | Approx. HRC (from ~55 as-quenched) |
|---|---|
| 205 | 50–53 |
| 315 | 45–48 |
| 425 | 40–43 |
| 540 | 32–35 |
| 650 | 22–27 |

Hold ≥1 h per 25 mm, minimum ~2 h. Use the grade's tempering curve; Hollomon–Jaffe
parameter P = T(C + log t) (T in K, t in h, C ≈ 20; e.g. 425 °C for 2 h gives P ≈ 14,170, equal to about 11 h at 400 °C, computed) lets you trade time against temperature.
**Avoid ~260–370 °C** (gated: unconfirmed, source is paywalled or blocked) in many alloy steels (tempered martensite embrittlement) and slow
cooling through ~375–575 °C in susceptible grades (temper embrittlement).

## 5. Weldability note
Check carbon equivalent, e.g. IIW CE = C + Mn/6 + (Cr+Mo+V)/5 + (Ni+Cu)/15. Roughly (gated: unconfirmed, source is paywalled or blocked):
< 0.40 good; 0.40–0.60 preheat needed; > 0.60 preheat, low-hydrogen process and
often PWHT (the IIW formula as written gives 0.77 for a typical 4140 composition, computed). Hardened-and-tempered parts welded afterwards lose their temper locally.
Preheat values come from the welding code (e.g. AWS D1.1, EN 1011-2), not this rule.

## Gotchas
- **Decarburised surface** reads soft; specify protective atmosphere or machining
  allowance, and test hardness below the decarb layer.
- **Retained austenite** in high-carbon steels: low hardness, later growth. Consider
  sub-zero treatment and double temper.
- **Mass effect** — datasheet properties are often for small test bars; large forgings
  are softer in the core.
- **Distortion** scales with quench severity and asymmetry; leave grind stock.
- Safety-critical parts (pressure, lifting, structural) need the governing code and
  a competent metallurgist's sign-off.

## Verify
- [ ] Austenitising temperature is above A3 (or in the A1–Acm window) for this grade.
- [ ] Jominy lower band at the section's equivalent distance meets the core hardness.
- [ ] Quenchant is the mildest that meets hardness; geometry reviewed for cracking.
- [ ] Tempering temperature/time from the grade's curve, outside embrittlement ranges.
- [ ] Hardness checked at surface (below decarb) and, on a sectioned sample, the core.
