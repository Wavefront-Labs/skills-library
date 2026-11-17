---
id: transportation-logistics.road-driving.cargo-securement.tie-down-working-load-limits
name: tie-down-working-load-limits
category: transportation-logistics
field: road-driving
product: cargo-securement
tags: [cargo-securement, load-securing, load-restraint, tie-downs, working-load-limit, wll, lashing-capacity, lc, ratchet-straps, chains, binders, edge-protection, dunnage, blocking-and-bracing, friction-mats, anti-slip-mats, flatbed, tarping, 49-cfr-393, fmcsa-cargo-securement, en-12195-1, en-12195-2, load-distribution, axle-weights, securement-inspection, coils, machinery]
level: practitioner
status: verified
description: "Secure loads on road vehicles: size the aggregate working-load limit, count tie-downs by length and weight, use blocking, friction mats and edge protection, and re-check securement en route."
sources: ["https://www.ecfr.gov/current/title-49/part-393/subpart-I","https://www.ecfr.gov/current/title-49/section-392.9"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tie-downs and working-load limits

**Goal:** a load that cannot shift, fall or spill under hard braking, cornering and
bumps — and that passes a roadside securement inspection.

*Summarises US FMCSA rules (49 CFR 393.100–136, checked against eCFR 2026-10-15) and the European standard
EN 12195-1 approach (EN text is paywalled: confirm values there). Commodity-specific rules (logs, coils, vehicles, concrete pipe,
machinery) add requirements. Read the actual text for your load type.*

## 1. Forces you are securing against
US performance criteria, 49 CFR 393.102, applied separately:
- **Breaking strength basis:** 0.8 g forward, 0.5 g rearward, 0.5 g lateral.
- **Working-load-limit basis:** 0.435 g forward, 0.5 g rearward, 0.25 g lateral (this is the
  basis tiedown WLLs are sized to, so do not read 0.8 g as a WLL requirement).
- Vertical: a downward force of at least 20% of the article's weight when the article is not
  fully contained within the vehicle structure.
EN 12195-1 uses its own acceleration coefficients: confirm in the standard.

## 2. US aggregate WLL rule (summary)
- The **sum of working-load limits** of all tie-downs must be at least **half the
  cargo weight**.
- Per 393.106(d): a tie-down running from a vehicle anchor to a cargo anchor counts **50%** of its
  WLL; one that passes over/through/around the cargo and returns to an anchor on the *same* side
  also counts 50%; one that crosses the cargo to an anchor on the *other* side counts **100%**.
- **Minimum number of tie-downs** (for articles not blocked at the front):
  - one tie-down for an article ≤ 5 ft (1.52 m) long *and* ≤ 1,100 lb (500 kg),
  - two tie-downs if ≤ 5 ft but > 1,100 lb, or if > 5 ft and ≤ 10 ft (3.04 m) at any weight,
  - two if longer than 10 ft, plus one more for each additional 10 ft or fraction beyond the
    first 10 ft,
  - if the article is blocked forward (headerboard, bulkhead, secured cargo), one tie-down per
    10 ft of length or fraction (393.110(c)).
  - 393.110(d) exempts machinery and fabricated structural items that need special methods, but
    they must still be securely fastened.
- Unmarked tie-downs are rated at the default WLL in 393.108 (confirm the table values there).

Worked example: 12,000 lb machine on a flatbed → aggregate WLL ≥ 6,000 lb. Using
4 chains rated 6,600 lb WLL each attached direct (vehicle-to-cargo, 50% each) →
4 × 3,300 = 13,200 lb ✓. Length 16 ft, unblocked → minimum 3 tie-downs (2 + 1 for the fraction beyond 10 ft), so 4 is fine.
Commodity rules in 393.116–136 (e.g. 393.128 vehicles up to 10,000 lb: at least two tie-downs, front and
rear) can add requirements; read the one for your load.

## 3. EN 12195-1 approach (Europe)
- Calculate needed lashing force from load weight, friction coefficient and the method
  (top-over/frictional lashing vs direct lashing). **Friction matters a lot**: anti-slip
  mats raise friction and can cut the straps needed substantially; take μ from EN 12195-1 or the mat certificate.
- Use the strap's label: **LC** (lashing capacity, daN) and **STF** (standard tension
  force — what a ratchet actually pre-tensions to). Top-over lashing works through
  STF, not LC.

## 4. Practical method
1. **Block first**: load against the headboard/bulkhead or block the front — the
   cheapest restraint against forward force.
2. **Fill gaps** with dunnage, airbags or empty pallets so the load can't build momentum.
3. **Friction mats** under loads on smooth decks.
4. **Edge protectors** wherever straps cross sharp edges — a cut strap has zero WLL.
5. Distribute weight to keep axle loads legal (heavy items over/just ahead of the
   trailer axles on flatbeds; avoid heavy loads at the very rear).
6. Tarp after securing; tarps don't secure anything.

## 5. Inspect en route
- US rule (§392.9(b)): inspect within the first **50 miles**, then again on a change of duty status
  or after 3 hours or 150 miles of driving, whichever occurs first. Straps loosen as loads
  settle.
- Replace damaged straps/chains: cuts, knots, stretched links, damaged hooks.

## Gotchas
- A strap's WLL is only as strong as the anchor point it's hooked to — check the rail's
  rating.
- Knotting a strap to shorten it destroys its rating.
- Loads on loads (stacked pallets) need securing per tier.

## Verify
- [ ] Aggregate WLL ≥ ½ cargo weight (US) or EN 12195-1 calculation done.
- [ ] Tie-down count meets the minimum for length/weight.
- [ ] Load blocked forward, gaps filled, edges protected.
- [ ] Re-checked after the first 50 miles / per local rule.
