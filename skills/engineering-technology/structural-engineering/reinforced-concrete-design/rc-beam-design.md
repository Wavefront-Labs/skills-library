---
id: engineering-technology.structural-engineering.reinforced-concrete-design.rc-beam-design
name: rc-beam-design
category: engineering-technology
field: structural-engineering
product: reinforced-concrete-design
tags: [reinforced-concrete-design, rc-beam, concrete-beam, flexure, rectangular-stress-block, whitney, shear, stirrups, links, crack-control, deflection, span-depth-ratio, detailing, development-length, minimum-reinforcement, tension-controlled, aci-318, eurocode-2, en-1992-1-1, as-3600, ultimate-strength-design, serviceability, cover]
level: practitioner
status: verified
description: "Design a reinforced concrete beam for flexure, shear, deflection and crack control to ACI 318 with Eurocode 2 cross-checks: sizing, steel area, stirrups, detailing."
sources:
  - "ACI 318 Building Code Requirements for Structural Concrete and Commentary"
  - "EN 1992-1-1 Eurocode 2 - Design of concrete structures, General rules"
  - "Wight, Reinforced Concrete: Mechanics and Design"
  - "The Concrete Centre, How to Design Concrete Structures using Eurocode 2"
  - "CRSI Manual of Standard Practice"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# RC beam design — size it, reinforce it, detail it

**Goal:** a reinforced concrete beam with a section that controls deflection,
tension-controlled flexural steel, adequate stirrups and buildable detailing.

Clauses are ACI 318-19, with US units for dimensional formulas (ACI 318-25 is now out,
so check what your jurisdiction adopts). EC2 equivalents are given where useful. The
engineer of record must confirm the governing edition. ACI 318 and EN 1992 are paywalled, so clause numbers and coefficients are unconfirmed against the text (gated: unconfirmed, source is paywalled or blocked) unless marked computed.

## 1. Size the section
- **ACI Table 9.3.1.1** minimum h for no deflection calculation (normal-weight
  concrete, Grade 60 steel). These values are for beams and one-way ribbed slabs:
  - simply supported: L/16;
  - one end continuous: L/18.5;
  - both ends continuous: L/21;
  - cantilever: L/8 (gated: unconfirmed, source is paywalled or blocked).
- Practical width b ≈ 0.4–0.6h, and at least the column width when framing in. A
  beam no deeper than the slab plus 100–150 mm only saves formwork if it is wide.
- **EC2 7.4.2 (Table 7.4N)** basic span/effective depth: 20 (simple) to 30 (interior span)
  at ρ = 0.5%, falling to 14–20 at ρ = 1.5% (gated: unconfirmed, source is paywalled or blocked). Modify by 310/σs and for flanged
  sections.

## 2. Flexure
1. Take Mu from the envelope, with pattern live load where L is significant.
2. Trial: As ≈ Mu / (φ·fy·0.9d).
3. Check:
   - a = As·fy / (0.85·f'c·b);
   - φMn = φ·As·fy·(d − a/2), with φ = 0.90 if tension-controlled;
   - c = a/β1, where β1 = 0.85 for f'c ≤ 4000 psi and falls by 0.05 per 1000 psi to
     a minimum of 0.65.
4. **Tension-controlled:** ACI 318-19 requires εt ≥ εty + 0.003 (about 0.0051 for
   Grade 60: computed 60/29000 + 0.003 = 0.00507). Earlier editions used 0.005 (gated: unconfirmed, source is paywalled or blocked). If εt is too low, deepen the section or add
   compression steel. Do not just accept a lower φ.
5. **Minimum steel:** As,min = max(3√f'c / fy, 200/fy)·bw·d. Use a T-beam with the
   flange in tension for negative moment.
6. **EC2:**
   - K = M/(b·d²·fck), with K ≤ K'. K' = 0.598δ − 0.18δ² − 0.21 (δ = moment redistribution ratio; computed 0.208 at δ = 1.0, 0.168 at δ = 0.85), so 0.167-0.168 is the limit for up to 15% redistribution, not for none (gated: unconfirmed, source is paywalled or blocked).
   - z = d·[0.5 + √(0.25 − K/1.134)] ≤ 0.95d. The constant 1.134 = 2·αcc/γc with αcc = 0.85 and γc = 1.5 (UK NA; derived and computed). With the EN recommended αcc = 1.0 it is 1.333.
   - As = M/(0.87·fyk·z), using γs = 1.15 (0.87 = 1/1.15).

## 3. Shear (ACI 22.5, 9.6.3, 9.7.6)
- φ = 0.75. Design Vu at d from the support face when the support is in compression.
- **Vc:** ACI 318-19 Table 22.5.5.1. With at least minimum stirrups, the simplified
  Vc = 2λ√f'c·bw·d may be used. Without them, the size effect λs = √(2/(1+d/10)) ≤ 1
  (d in inches) and ρw^(1/3) apply (gated: unconfirmed, source is paywalled or blocked). Check every alternative expression in that table directly.
- **Stirrups:** Vs = Av·fyt·d/s, with Vs ≤ 8√f'c·bw·d (otherwise enlarge the section).
- **Maximum spacing:** d/2 or 24 in, halved when Vs > 4√f'c·bw·d.
- **Minimum stirrups** are needed when Vu exceeds about φλ√f'c·bw·d (318-19 9.6.3.1).
  Confirm the exact threshold in your edition (gated: unconfirmed, source is paywalled or blocked), because it changed from 0.5φVc in
  318-14.
- **EC2:** variable strut-angle method, cotθ 1.0–2.5. VRd,s = (Asw/s)·z·fywd·cotθ.

## 4. Serviceability
- **Crack control, ACI 24.3.2:** bar spacing s ≤ 15(40,000/fs) − 2.5cc and
  ≤ 12(40,000/fs), with fs ≈ (2/3)fy (gated: unconfirmed, source is paywalled or blocked). That gives about 10–12 in for Grade 60 with
  1.5–2 in cover (computed: fs = 40 ksi gives 15 − 2.5cc = 10 in at cc = 2 in, 11.25 in at 1.5 in, capped at 12 in).
- **Deflection when the h-table is not met:**
  - immediate: ACI 318-19 Ie (Bischoff form, with Mcr reduced by 2/3);
  - long-term multiplier: λΔ = ξ/(1 + 50ρ′), with ξ = 2.0 for 5 years or more.
  - Limits (Table 24.2.2): L/360 for live load on floors; L/480 for the portion after
    attaching non-structural elements likely to be damaged (gated: unconfirmed, source is paywalled or blocked).
- **EC2:** crack width wk ≤ 0.3 mm under quasi-permanent load for most exposure
  classes (Table 7.1N recommended values) (gated: unconfirmed, source is paywalled or blocked).

## 5. Detailing
- **Clear cover, ACI 20.5.1.3:** 1.5 in to stirrups for beams not exposed to weather;
  2 in for #6 and larger bars exposed to weather (gated: unconfirmed, source is paywalled or blocked).
- **Bar clear spacing** ≥ max(1 in, db, 4/3 × maximum aggregate size). Leave a gap for
  a vibrator in wide beams.
- Develop bars beyond the point where they are no longer needed by d or 12db.
  Continue at least 1/4 of the positive steel into supports (1/3 for simple spans).
- Use closed stirrups (135° hooks) where torsion or seismic detailing applies.
- Lap splices: class B (1.3ld) is typical. Avoid lapping at points of maximum moment.

## Verify
- [ ] h meets Table 9.3.1.1 (or the EC2 span/depth ratio), or a deflection calculation is done.
- [ ] εt ≥ εty + 0.003 (318-19) and As ≥ As,min at every design section.
- [ ] φVn ≥ Vu along the whole beam with spacing limits respected.
- [ ] Crack-control spacing, cover and bar clear spacing are satisfied.
- [ ] Development, cut-offs and support anchorage are detailed.
- [ ] Code edition (ACI 318-19 vs -25, EC2 generation and National Annex) is confirmed by the engineer of record.
