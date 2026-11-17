---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.head-injury-criterion
name: head-injury-criterion
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [hic, head-injury-criterion, hic15, hic36, head-acceleration, injury-risk]
level: practitioner
status: gated
description: "Compute HIC from head acceleration data: the formula, window choice (15 or 36 ms), clipping, limits by regulation and how to read the result."
sources:
  - "FMVSS 208 and UN R94 head criteria; confirm current limits"
  - "Kleiven and others on head injury biomechanics"
  - "https://www.law.cornell.edu/cfr/text/49/571.208"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Head injury criterion (HIC)

1. Formula: `HIC = max over t1,t2 of [ (t2 - t1) * ( (1/(t2 - t1)) * integral(a dt from t1 to t2) )^2.5 ]` with a the resultant head acceleration in g and time in seconds; windows are limited to 15 ms (HIC15) or 36 ms (HIC36).
2. Data: head CG resultant acceleration from the dummy's 3-axis accelerometer, filtered to CFC 1000 (per the test standard), sampled at 10 kHz or more.
3. Calculation: scan all window pairs up to the maximum length (efficient code uses a sliding window); report HIC and the window.
4. Limits: US FMVSS 208 requires HIC15 not above 700 (checked in 49 CFR 571.208); ECE R94 uses HPC (HIC36) 1000 (gated: unconfirmed, source is paywalled or blocked); consumer programmes use graded sliding scales. Confirm current values and dummy scaling in the text.
5. Also report the 3 ms clip value (FMVSS 208 limits chest 3 ms clip to 60 g; head clip limits in other regulations: confirm (gated: unconfirmed, source is paywalled or blocked)).
6. Interpretation: HIC does not capture rotational loads that cause brain injury; research on rotational criteria (BrIC) is ongoing.
7. In engineering: HIC drives airbag stiffness, steering column and header design for head contact.

**Gotchas:** wrong filter class; unit mix-up (m/s^2 vs g).

## Verify
- [ ] Code checked against a reference acceleration pulse with known HIC.
- [ ] Filtering class and units logged with results.
