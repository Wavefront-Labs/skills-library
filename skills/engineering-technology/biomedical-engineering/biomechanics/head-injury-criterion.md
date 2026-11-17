---
id: engineering-technology.biomedical-engineering.biomechanics.head-injury-criterion
name: head-injury-criterion
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [head-injury-criterion, hic, head-acceleration, crash-testing, injury-criteria]
level: practitioner
status: gated
description: "Compute the Head Injury Criterion (HIC15 and HIC36) from head acceleration, with filtering, window search, units and the limits used in regulation and rating."
sources: ["49 CFR 571.208 Standard No. 208 Occupant crash protection, S6.2 and S15.3.2 (https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-571/subpart-B/section-571.208)", "SAE J211 Instrumentation for impact test (confirm edition)", "Versace, A review of the severity index (SAE paper, 1971)", "https://www.nhtsa.gov"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Head Injury Criterion

**Goal:** compute HIC correctly from the resultant head acceleration time history.

## Definition
HIC = max over windows [t1, t2] of (t2 - t1) times [ (1 / (t2 - t1)) times the integral of a(t) dt from t1 to t2 ] raised to the power 2.5, with a in units of g and time in seconds. HIC15 limits the window to 15 ms and HIC36 to 36 ms.

## Procedure
1. Take the resultant of the three head acceleration components, filtered with the channel class specified in the test standard (SAE J211 defines channel classes; CFC 1000 is commonly used for head acceleration (gated: unconfirmed, source is paywalled or blocked)).
2. For every start time and window length up to the limit, compute the average acceleration and HIC; take the maximum. Use an efficient search but verify with brute force.
3. Check the unit (g, not m/s squared) and sampling rate (10 kHz or higher is typical (gated: unconfirmed, source is paywalled or blocked)).
4. Worked check: a constant 100 g for 10 ms gives HIC = 0.010 x 100 to the 2.5 = 0.010 x 100000 = 1000.

## Limits
- 49 CFR 571.208 (FMVSS 208) S6.2 sets, for the Hybrid III 50th percentile male dummy, HIC15 not above 700 (the 15 ms window) and gives a HIC36 not above 1,000 alternative; other dummies have their own HIC15 limits in the same standard (for example 570 and 390 appear for smaller dummies). Consumer rating programmes set their own limits. Confirm the current text and dummy.
- HIC predicts risk of skull fracture and severe brain injury from linear acceleration only; it does not capture rotational acceleration, a known limitation.

## Verify
- [ ] Reproduce a published example (as above) in test code.
- [ ] Filter class, sampling and window limits recorded.
- [ ] Dummy size and limit source stated.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
