---
id: transportation-logistics.space-traffic-management.conjunction-assessment.probability-of-collision-and-risk-thresholds
name: probability-of-collision-and-risk-thresholds
category: transportation-logistics
field: space-traffic-management
product: conjunction-assessment
tags: [conjunction-assessment, ca, probability-of-collision, pc, miss-distance, tca, covariance, covariance-realism, hard-body-radius, cdm, encounter-plane, b-plane, 2d-pc, foster, alfano, chan, dilution-region, maximum-pc, red-yellow-green, cara, collision-risk, space-traffic-management]
level: advanced
status: gated
description: "Reading a CDM, computing and sanity-checking probability of collision, recognising covariance-dilution traps, and applying red/yellow/green Pc thresholds to escalate events."
sources: ["https://www.nasa.gov/wp-content/uploads/2018/01/oce_51-nasa_spacecraft_conjunction_assessment_and_collision_avoidance_best_practices_handbook.pdf", "https://www.nasa.gov/wp-content/uploads/2025/03/cara-faq-npr-handbook-2025.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Probability of collision and risk thresholds

**Goal:** decide, for each close approach, whether it is safe to ignore, needs
watching, or needs a manoeuvre plan — using Pc correctly and knowing when Pc lies.

## 1. Read the CDM first
From each Conjunction Data Message pull: TCA, miss distance and its **radial /
in-track / cross-track** split, relative speed, both objects' covariances (and their
OD epoch/age), object types and sizes, and the computed Pc. Note the creation time —
you will compare CDMs over days.

## 2. Compute Pc (short-term encounter)
For LEO encounters relative speed is km/s, so the encounter is near-instantaneous:
1. Combine the two position covariances (add them; assume independence).
2. Project onto the **encounter plane** (perpendicular to relative velocity).
3. Choose a **hard-body radius (HBR)** = radius of a sphere enclosing both objects
   (sum of each object's circumscribing radius; for unknown debris use an RCS-based
   estimate or a conservative default).
4. Integrate the 2-D Gaussian over the HBR circle centred on the miss vector
   (Foster/Chan/Alfano methods agree to a few per cent for normal cases).
Use a 3-D/long-term method for slow encounters (GEO co-location, formation flying,
rendezvous) — the 2-D assumption breaks when relative speed is low.

## 3. Sanity checks before trusting the number
- **Dilution region:** if covariances are huge relative to miss distance, Pc is *low
  because we know little*, not because it is safe. Compute the **maximum Pc** over
  covariance scaling; if max Pc is high and the data are poor, request more tracking
  rather than closing the event.
- **Stale secondary OD** (days old) or a secondary with a tiny, unrealistic
  covariance — flag it.
- **Trend:** Pc should settle as TCA approaches. Pc swinging by orders of magnitude
  between CDMs means the covariance or orbit is unstable.
- **Radial miss distance:** a small radial separation with a large in-track miss
  can still collapse as in-track uncertainty shrinks.
- **Manoeuvrable secondary:** the other object may move — coordinate (see
  collision-avoidance-coordination).

## 4. Thresholds and escalation (common practice)
| Pc | Colour | Typical action |
|---|---|---|
| ≥ 1e-4 | Red | Plan an avoidance manoeuvre; execute unless data improve |
| 1e-5 – 1e-4 | Yellow | Increase tracking, prepare manoeuvre options, watch trend (gated: unconfirmed, source is paywalled or blocked) |
| < 1e-5 | Green | Routine monitoring |
1e-4 is the widely used NASA/CARA manoeuvre threshold; many operators use 1e-4 or
1e-5 depending on mission value and the debris-generation consequence. Some also
apply a **miss-distance backstop** (e.g. act if radial < ~200 m regardless (gated: unconfirmed, source is paywalled or blocked)) — *local
choice, not a universal rule.* Write your thresholds into the flight rules before
you need them.

## 5. Decision timing
Decide at a fixed lead time (often ~1–2 days before TCA for LEO (gated: unconfirmed, source is paywalled or blocked)): late enough that
data have converged, early enough to plan, screen and upload a burn.

## Gotchas
- Covariances in CDMs are in RTN of each object; combine them in a common frame.
- HBR choice moves Pc roughly with HBR² — an oversized default can trigger needless
  manoeuvres.
- Collision with a large debris object creates thousands of fragments; some operators
  weight Pc by consequence (mass) when prioritising.
- Repeating conjunctions with the same object (resonant orbits) — assess all TCAs.

## Verify
- [ ] Pc recomputed independently matches the CDM within ~10–20 %.
- [ ] Max-Pc / dilution check done for any low-Pc, small-miss event.
- [ ] Covariance age and realism noted for both objects.
- [ ] Event classified against written thresholds, with the decision time recorded.
- [ ] Trend across ≥ 3 CDMs reviewed before closing a yellow or red event.

## Checked

Jurisdiction: NASA-style conjunction assessment (not a regulation). Checked 2026-10-25: the NASA CARA handbook and NPR 8079.1 summaries state a baseline remediation threshold of Pc above 1E-04 (or a miss distance below the combined hard-body radius); this confirms the red band. The yellow and green bands, the miss-distance backstop and the decision lead time are operator conventions that the fetched NASA material did not state and are marked gated. The handbook PDF could not be text-extracted.

Method: documentation only; no commands were run.
