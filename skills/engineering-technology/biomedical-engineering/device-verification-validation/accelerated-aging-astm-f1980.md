---
id: engineering-technology.biomedical-engineering.device-verification-validation.accelerated-aging-astm-f1980
name: accelerated-aging-astm-f1980
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [accelerated-aging, packaging-validation, shelf-life, packaging-shelf-life, astm-f1980, q10, arrhenius, real-time-aging, expiry-date]
level: practitioner
status: gated
description: "Plan accelerated ageing of sterile packaged devices per ASTM F1980: Q10 formula, temperature and time calculation, humidity limits, real-time confirmation and package tests."
sources: ["ASTM F1980 Standard guide for accelerated aging of sterile barrier systems and medical devices (confirm edition)", "ISO 11607-1 Packaging for terminally sterilized medical devices (shelf-life and stability)", "ISO 11607-2 Validation requirements for forming sealing and assembly processes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Accelerated ageing per ASTM F1980

**Goal:** support a labelled shelf life before real-time data exist, by ageing packaged devices at elevated temperature for a computed time.

## Formula
AAT = RT / Q10^((T_AA - T_RT) / 10)
- AAT: accelerated ageing time. RT: desired real-time shelf life. T_AA: ageing temperature. T_RT: ambient storage temperature. Q10: reaction-rate factor per 10 C, commonly **2.0** as a conservative default in the guide (gated: unconfirmed, source is paywalled or blocked); other values need justification. Formula and worked numbers below were recomputed (365/8 = 45.6 days; 2^3.3 = 9.85, 365/9.85 = 37.1 days), but the exact F1980 wording is paywalled: confirm edition (F1980-21 at astm.org) and clause text.

## Worked example
Shelf life 1 year at T_RT = 25 C, T_AA = 55 C, Q10 = 2:
factor = 2^((55-25)/10) = 2^3 = 8, so AAT = 365 / 8 = 45.6 days.
At T_RT = 22 C: 2^3.3 = 9.85, giving 37 days.

## Procedure
1. Define the package (final sterile barrier system, sterilised by the production process) and the device; age the final sterile product.
2. Set T_AA, usually 50-60 C (the guide advises keeping T_AA modest, with maximum around 60 C (gated: unconfirmed, source is paywalled or blocked), and that materials must not change mechanism, such as melting or glass transition). Control relative humidity (ambient or a stated lower value to avoid condensation); record temperature and humidity continuously.
3. Calculate the time for each shelf-life claim (for example 1, 2 and 3 years) and pull samples at those points.
4. After ageing, test **package integrity and strength** (seal strength, see seal-strength-astm-f88; dye penetration, see dye-penetration-astm-f1929; bubble leak) and **device performance** (functional, material properties, drug stability where relevant).
5. **Real-time ageing** at the labelled storage conditions starts at the same time and continues to the claimed life; the accelerated results are provisional until real-time data confirm.

## Gotchas
- Q10 is an assumption; materials with a transition near the ageing temperature break the model.
- Adhesives and polymers differ; test all components of the system.
- Humidity-sensitive devices (hydrogels, biologic coatings) may need different conditions.
- Do not forget transport and distribution testing (see distribution-testing).

## Verify
- [ ] Calculation sheet includes Q10 rationale and chamber logs.
- [ ] All time points pass the pre-set criteria.
- [ ] Real-time study running with a protocol and dates.
