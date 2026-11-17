---
id: engineering-technology.automotive-vehicle-engineering.nvh.acoustic-vehicle-alerting-system
name: acoustic-vehicle-alerting-system
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [avas, pedestrian-warning, un-r138, fmvss-141, alert-sound, quiet-vehicle]
level: practitioner
status: verified
description: "Specify an acoustic vehicle alerting system: regulatory scope (UN R138, FMVSS 141), sound content and level, frequency bands, speed range and engineering considerations."
sources:
  - "https://eur-lex.europa.eu/eli/reg/2017/71/oj/eng"
  - "https://www.law.cornell.edu/cfr/text/49/571.141"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Acoustic vehicle alerting system (AVAS)

1. Purpose: quiet EVs and hybrids need a sound that lets pedestrians detect them at low speed.
2. Regulations (confirm current texts and amendments for each market). UN R138 (as published in the EU as Regulation (EU) 2017/71; later amendments exist): sound required from above 0 up to and including 20 km/h (6.2); pass-by tests at 10 km/h and 20 km/h (6.2.1.1) with overall and one-third-octave band minimums in Table 2 (6.2.8); at least one tone must shift by an average of at least 0.8% per 1 km/h from 5 to 20 km/h forward (6.2.3.2); reversing sound (6.2.2.1); forward AVAS sound not above 75 dB(A) (6.2.7). FMVSS 141 (49 CFR 571.141): sound required up to 30 km/h; stationary, reverse and pass-by tests at 11, 21 and 31 km/h (S7); four-band (315-5000 Hz) or two-band compliance options (S5.1, S5.2); it does not require a pitch shift, but requires at least 3 dB relative volume change between adjacent speed steps (S5.4).
3. Content: broadband plus tonal content across several bands (so that it is detectable in urban noise), frequency shift with speed (the required amount is set in the regulation) and level increase with speed; avoid annoying tonal timbre. Pitch shift is required by UN R138 but not by FMVSS 141.
4. Hardware: external speaker (location, waterproofing, mounting), amplifier, controller reading speed and gear; check for failures and diagnostic.
5. Design: use the brand sound design but meet the regulatory spectrum; test in a semi-anechoic or outdoor pass-by facility with measurement per the standard.
6. Interior leakage: keep the cabin level low to avoid annoyance.
7. Document compliance with the test lab and type approval authority.

**Gotchas:** weather and mounting change levels; measure on the final vehicle.

## Verify
- [ ] Pass-by test at the specified speeds shows required band levels.
- [ ] Speed-dependent pitch change measured within spec.
