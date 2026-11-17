---
id: engineering-technology.materials-engineering.materials-characterisation.tensile-and-hardness-testing
name: tensile-and-hardness-testing
category: engineering-technology
field: materials-engineering
product: materials-characterisation
tags: [materials-engineering, materials-characterisation, materials-characterization, mechanical-testing, tensile-test, tension-test, astm-e8, iso-6892-1, yield-strength, proof-stress, 0.2-percent-offset, rp0.2, ultimate-tensile-strength, uts, elongation, reduction-of-area, extensometer, strain-rate, hardness, rockwell, brinell, vickers, microhardness, astm-e18, astm-e10, iso-6507, astm-e140, iso-18265, hardness-conversion, utm]
level: practitioner
status: verified
description: "Run and interpret tensile tests (ASTM E8 / ISO 6892-1) and hardness surveys: yield by 0.2% offset, elongation, strain rate, and hardness conversion limits."
sources:
  - "ASTM E8/E8M, Standard Test Methods for Tension Testing of Metallic Materials"
  - "ISO 6892-1, Metallic materials: Tensile testing at room temperature"
  - "ASTM E18 (Rockwell), ASTM E10 (Brinell), ASTM E384 / ISO 6507 (Vickers, microindentation)"
  - "ASTM E140 and ISO 18265, hardness conversion tables"
  - "Dieter, Mechanical Metallurgy (McGraw-Hill)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tensile and hardness testing — numbers you can defend

> Evidence note: ASTM, ISO and JIS test standards are paywalled and astm.org and iso.org returned 403, so clause-level values below are recalled and unconfirmed (gated: unconfirmed, source is paywalled or blocked) unless marked computed. Product specifications govern acceptance; testing for safety-critical use should be done by an accredited laboratory (ISO/IEC 17025).

**Goal:** produce tensile and hardness results that meet the test standard, mean what
the specification intends, and are interpreted correctly for an accept/reject or
design decision.

## 1. Plan the tensile test
1. **Standard**: ASTM E8/E8M (US) or ISO 6892-1 (international). They are close but
   not identical — gauge length, strain-rate control and elongation reporting differ,
   so state which was used. Product specs often name one.
2. **Specimen**: take it from the location and orientation the spec demands
   (longitudinal vs transverse; quarter-thickness for plate). Common round specimen:
   12.5 mm diameter, 50 mm gauge (4D, ASTM). ISO proportional specimens use
   L0 = 5.65√S0 (= 5d for rounds; computed 5.007d). Elongation from 4D and 5D gauges is **not**
   interchangeable.
3. **Measure** S0 at several points along the gauge (micrometer, ±0.5% typical (gated: unconfirmed, source is paywalled or blocked)),
   and mark the gauge length.
4. **Extensometer** on the gauge length for modulus and yield; crosshead displacement
   includes machine and grip compliance and will understate modulus badly.

## 2. Run it
- **Rate**: ISO 6892-1 Method A uses strain-rate control (e.g. ~0.00025 s⁻¹ through
  yield, higher afterwards (gated: unconfirmed, source is paywalled or blocked)); ASTM E8 allows stress-rate or strain-rate limits. Yield
  values can rise several percent at higher rates (gated: unconfirmed, source is paywalled or blocked) — use the standard's ranges.
- Alignment: bending of a few percent distorts yield; use proper grips, check with a
  strain-gauged alignment specimen periodically (ASTM E1012).
- Machine verification of force (ASTM E4 / ISO 7500-1) and extensometer class (ASTM
  E83 / ISO 9513) must be current.

## 3. Extract the results
| Quantity | How |
|---|---|
| Young's modulus E | Slope of linear elastic portion with extensometer; tensile tests are poor for E (±5–10% (gated: unconfirmed, source is paywalled or blocked)) |
| Yield (Rp0.2) | Line parallel to elastic slope offset by 0.2% strain; intersection with curve |
| Upper/lower yield (ReH/ReL) | For discontinuous yielding (mild steel, yield-point elongation) |
| UTS (Rm) | Maximum force / original area S0 |
| Elongation after fracture (A) | Fit broken halves, (Lu − L0)/L0; fracture should be in middle third or retest rules apply |
| Reduction of area (Z) | (S0 − Su)/S0 |

Report true stress-strain only up to UTS unless necking is corrected (Bridgman).

## 4. Hardness survey
| Method | Load / indenter | Use |
|---|---|---|
| Rockwell C (HRC) | 150 kgf, diamond cone | Hardened steels ~20–70 HRC |
| Rockwell B (HRB) | 100 kgf, 1/16 in ball | Softer steels, brass, aluminium |
| Brinell (HBW) | 3000 kgf, 10 mm carbide ball typical | Castings, forgings, coarse microstructures |
| Vickers (HV) / micro | 1 gf–100 kgf, diamond pyramid | Thin sections, case depth, weld HAZ traverses |

Rules: specimen thickness ≥ ~10× indentation depth (Rockwell) and ≥ 1.5× diagonal
(Vickers); indent spacing ≥ ~3 diameters from each other and from edges (check exact
values in the standard (gated: unconfirmed, source is paywalled or blocked)); flat, clean, decarb-free surface; curvature corrections for
rounds under ~25 mm diameter (Rockwell). Verify the tester daily on a certified block.

## 5. Converting hardness and estimating strength
- Conversions (ASTM E140 / ISO 18265) are **empirical and material-specific**: tables
  for carbon/low-alloy steel do not apply to austenitic stainless, aluminium or cast
  iron, and carry scatter. Report the measured scale; mark converted values as such.
- Steel UTS estimate: UTS (MPa) ≈ 3.3–3.45 × HB (≈ 500 × HB in psi; unit check: 500 psi = 3.45 MPa), roughly valid for
  carbon and low-alloy steels ~150–450 HB. Useful for screening, never as a
  substitute for a required tensile test.

## Gotchas
- **Machining damage** or cold work in the gauge raises yield; finish to spec.
- **Gripping failures** and breaks outside the gauge are invalid — note and retest.
- Hydrogen-charged or plated parts can give low elongation; bake before testing if spec allows.
- Microhardness at low loads (<100 gf) shows an indentation size effect; compare at equal loads.
- Elongation results from different specimen geometries cannot be compared directly.

## Verify
- [ ] Specimen location, orientation and geometry match the product spec and test standard.
- [ ] Force and extensometer calibrations current; extensometer used for yield and modulus.
- [ ] Strain/stress rate within the standard's limits and recorded.
- [ ] Hardness scale suits the material and thickness; tester verified on a reference block.
- [ ] Any converted hardness or strength estimate is labelled and from the right material table.
