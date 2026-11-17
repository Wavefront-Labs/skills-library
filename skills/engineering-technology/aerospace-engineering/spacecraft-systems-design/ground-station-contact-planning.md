---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.ground-station-contact-planning
name: ground-station-contact-planning
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [ground-contact, pass-duration, data-volume, doppler-shift, ground-station-network, spacecraft-communications]
level: practitioner
status: docs-checked
description: "Compute LEO pass duration and contact opportunities from orbit geometry and minimum elevation, then data volume per day and Doppler range."
sources:
  - "https://en.wikipedia.org/wiki/Orbital_period"
  - "https://en.wikipedia.org/wiki/Doppler_effect"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ground station contact

**Goal:** time in contact, data downlinked per day, and tracking needs.

## Geometry
- Earth central angle to the horizon at minimum elevation `eps`: `lambda = acos( R_E/(R_E + h) * cos(eps) ) - eps`.
- Visible arc `2 lambda`; maximum pass duration (zenith pass, ignoring Earth rotation) `T_pass = (2 lambda / 360 deg) * T_orbit`.
- Example: 500 km altitude (period about 94.6 minutes): `eps = 0`: about 11.5 minutes; `eps = 10` degrees: about 7.4 minutes. Average passes are shorter than the maximum because they are off-zenith.

## Procedure
1. Propagate the orbit with a ground station list; compute access intervals above the minimum elevation (set by terrain and the antenna).
2. Count passes per day and total contact time per day.
3. Data volume per day `= data rate x contact time x link availability x protocol efficiency`; compare with data generated onboard; add storage margin.
4. Doppler: `delta_f/f = v_los / c`; at 7 km/s line of sight and 437 MHz the shift is about plus or minus 10 kHz; at 8.4 GHz about plus or minus 200 kHz; the ground station tracks the shift.
5. Latency: wait time between contacts; define the commanding cadence.
6. More stations or relay satellites increase contact time; polar stations add passes for polar orbits.

## Regulatory and operational
Frequency use needs coordination and licensing through the national regulator and ITU procedures; use only authorised frequencies.

## Gotchas
- Rain fade at high frequencies reduces availability.
- Station availability, weather and scheduling conflicts lower contact time.

## Verify
- [ ] Orbit-propagation access times agree with the analytical pass duration for a zenith pass.

## Checked
2026-11-01. Re-computed with a short script (R_E 6378.137 km): 500 km period 94.6 min; pass 11.6 min at 0 degrees and 7.4 min at 10 degrees elevation; Doppler at 7 km/s is 10.2 kHz at 437 MHz and 196 kHz at 8.4 GHz. Removed: typical elevation range and the Ka/K rain-fade band claim. Frequency use stays subject to the national regulator and ITU procedures.
Method: documentation only; no commands were run.
