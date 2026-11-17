---
id: manufacturing-production.packaging-operations.checkweighing-inspection-systems.checkweigher-and-metal-detector-setup-and-challenge-testing
name: checkweigher-and-metal-detector-setup-and-challenge-testing
category: manufacturing-production
field: packaging-operations
product: checkweighing-inspection-systems
tags: [checkweighing-inspection-systems, packaging-operations, checkweigher, check-weigher, dynamic-weighing, reject-limits, metal-detector, metal-detection, ferrous, non-ferrous, stainless-steel, test-pieces, test-wands, challenge-test, product-effect, product-learn, x-ray-inspection, foreign-body, contaminant, reject-confirmation, fail-safe, locked-reject-bin, haccp, ccp, brcgs, retailer-code-of-practice]
level: practitioner
status: draft
description: "Set up inline checkweighers, metal detectors and x-ray: learn the product, set reject limits, run test-piece challenge tests at the right positions and frequency, and handle rejects and failures."
sources: ["BRCGS Global Standard Food Safety (foreign-body detection clauses)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checkweigher and metal detector setup and challenge testing

**Goal:** inline inspection that rejects every non-conforming pack — and the evidence
that it did. In food plants the metal detector or x-ray is often a **critical control
point** (CCP) in the HACCP plan; a missed check can mean holding everything since the
last good test.

## 1. Checkweigher setup
- **Product recipe:** nominal weight, tare, target and reject limits for the pack.
  Limits come from the fill-weight rules (see
  manufacturing-production.packaging-operations.filling-sealing-lines.filler-setup-fill-weight-control-and-seal-integrity):
  typically reject below the TNE limit, and optionally reject overweight packs
  (double-fills, missing component detection).
- **Zero and calibrate:** auto-zero between packs is normal; full calibration with
  certified weights at the frequency your quality system sets (and after moving or
  cleaning the unit).
- **Dynamic vs static:** a pack weighed on a moving belt reads differently from a static
  scale. Compare by passing the same packs through several times and weighing them on a
  calibrated static scale; adjust the dynamic correction if the recipe allows.
- **Spacing:** only one pack on the weigh belt at a time; touching packs give wrong
  weights. Infeed speed-up belts create the gap.
- **Feedback** to the filler (mean weight trend) is worth enabling — it reduces giveaway.

## 2. Metal detector setup
- **Product learn:** wet, salty, warm or frozen product (and metallised film) gives
  a signal of its own — the **product effect**. The detector learns this so it can tell
  product from metal. Re-learn on every product change, and for temperature-sensitive
  products when temperature changes.
- **Sensitivity** is expressed as the smallest test sphere reliably detected for
  **ferrous**, **non-ferrous** and **stainless steel** (stainless is the hardest,
  especially in wet product). Retailer codes set the expected sizes by aperture and
  product (often around 1.5–2.0 mm Fe, 2.0–2.5 mm non-Fe, 2.5–3.5 mm SS for mid-size
  apertures — check the code you work to).
- **Aperture** should be as small as the pack allows; sensitivity is worst at the
  aperture's geometric centre.

## 3. Challenge testing (the routine)
- Use certified **test pieces** (sphere in a card or wand) of each metal type at the
  required size.
- Place the test piece **in or on a pack**, at the hardest-to-detect position (the
  centre of the pack / leading and trailing edges as your procedure defines), and pass
  it through at normal line speed in normal product flow.
- Each test must be: **detected, rejected, and found in the locked reject bin.**
  Detection with no rejection is a failure.
- Frequency: start-up, every set interval (often hourly), product change, after any
  stoppage or adjustment, and end of production. Record time, pieces, result, initials.
- **Fail-safe checks:** reject confirmation sensor, bin-full sensor, air pressure
  monitor for pneumatic rejecters, belt stop on fault. Test them too, per procedure.

## 4. When a test fails
1. Stop the line.
2. **Quarantine all product since the last successful test.**
3. Fix (re-learn, reposition reject, repair) and re-challenge until it passes.
4. Re-inspect the quarantined product through the working detector.
5. Record and escalate to quality.

## 5. X-ray inspection
Detects dense contaminants (metal, glass, stone, calcified bone, dense plastics)
regardless of magnetic properties, and also checks fill/missing components. Low-density
items (wood, most plastics, hair) may still be missed. Test with the x-ray test
pieces supplied for that unit. Operate within the radiation safety rules; never
defeat the curtains or interlocks.

## 6. Reject handling
- Reject bins **locked**, key held by quality/supervision; the operator must not be
  able to reach in and put product back.
- Investigate rejects: keep the found contaminant, identify the source (worn sieve,
  broken blade).

## Verify
- [ ] Checkweigher calibrated and limits match the recipe.
- [ ] Metal detector product-learned for this product.
- [ ] All three test metals detected, rejected and found in the locked bin.
- [ ] Tests on schedule and recorded; failure procedure known by every operator.

*Uncertain: sensitivity figures and test frequencies depend on the customer or retailer
code and the HACCP plan.*
