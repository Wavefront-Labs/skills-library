---
id: natural-sciences.amateur-astronomy.meteor-satellite-watching.meteor-counts-and-aurora-watching
name: meteor-counts-and-aurora-watching
category: natural-sciences
field: amateur-astronomy
product: meteor-satellite-watching
tags: [meteor-satellite-watching, meteor-shower, meteor-counts, zhr, zenithal-hourly-rate, radiant, limiting-magnitude, imo, international-meteor-organization, perseids, geminids, quadrantids, sporadic-meteors, fireball-reporting, aurora, aurora-forecast, kp-index, bz, solar-wind, noaa-swpc, ovation, satellite-passes, iss, starlink, heavens-above, naked-eye-astronomy]
level: intro
status: docs-checked
description: "Watch and count meteor showers in a way the IMO can use (radiant, limiting magnitude, ZHR), read aurora forecasts beyond Kp, and predict satellite passes without a telescope."
sources: [https://www.spaceweather.gov/products/planetary-k-index, https://www.spaceweather.gov/noaa-scales-explanation, https://www.spaceweather.gov/products/aurora-30-minute-forecast, https://www.spaceweather.gov/products/real-time-solar-wind, https://www.imo.net/files/meteor-shower/cal2026.pdf]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Meteor counts and aurora watching

**Goal:** enjoy the naked-eye sky events and, if you want, record them so they're
scientifically useful — and stop missing aurora because you only looked at Kp.

## 1. Meteor showers: when and where
- Use the **IMO annual shower calendar** for peak times, the radiant position and expected
  **ZHR** (zenithal hourly rate — the rate an observer would see with the radiant overhead
  under ideal standard conditions; real rates are almost always lower).
- Rates rise as the radiant climbs: most showers are best after local midnight. Check
  **Moon phase** — a bright Moon can wipe out most of the faint meteors.
- Get away from lights; lie back on a reclining chair, warm clothes and a blanket (you'll
  be still for hours).
- Meteors appear all over the sky; looking straight at the radiant shows short trails.

## 2. Counting like the IMO
1. Note start/end times in **UTC**, your location, and the centre of your field of view.
2. Measure **limiting magnitude** (LM) every hour or so, e.g. by counting stars inside
   standard triangles of stars from the IMO guide.
3. Record each meteor: time, shower assignment (does its path trace back to the radiant,
   and does its speed fit the shower?) or **sporadic**, and estimated magnitude.
4. Log **breaks** and cloud cover (% of field obscured) — effective observing time matters.
5. Submit via the IMO's online visual report form. The IMO computes ZHR from many observers
   with corrections for LM, radiant altitude and cloud.
- **Fireballs**: report separately (IMO/AMS fireball forms) with
  start/end points against the stars, duration, colour, fragmentation, and sound.

## 3. Aurora: reading the forecast
- **Kp** (0–9) is a 3-hour global index (a 3-hour range, so it is not instant). NOAA's G1 storm level starts at Kp 5
  and G5 is Kp 9; higher levels reach lower latitudes. Don't stop at Kp.
- Watch the **real-time solar wind** (NOAA SWPC, from satellites upwind of Earth at L1):
  - **Bz** (negative = southward): SWPC's plot can shade Bz below 0 nT or below −5 nT.
  - Watch **speed** and **density** alongside it.
- NOAA's **OVATION** short-term forecast maps show where the aurora is and how intense, with a lead time of about 30 to 90 minutes
  (the solar-wind travel time from L1).
- Look **poleward** (north in the northern hemisphere) to a low horizon. Phone cameras
  often reveal faint aurora as colour that eyes see as grey arcs — take a short exposure.

## 4. Satellite passes
- Predict with Heavens-Above, Stellarium or a phone app: the ISS gives bright passes;
  visible only when you're in darkness but the satellite is sunlit.

## 5. Comets (naked eye/binocular)
Check current comet lists (e.g. from comet observing groups or the Minor Planet Center) —
predicted brightness is notoriously unreliable; observe rather than trust a forecast.

## Gotchas
- Going out for a high-ZHR shower expecting that rate — real counts are usually lower.
- Mixing local time and UTC in reports.
- Chasing aurora on Kp alone while Bz is northward.
- Looking at a phone screen at full brightness every few minutes (dark adaptation lost).

## Verify
- [ ] Shower peak, radiant rise time and Moon phase checked beforehand.
- [ ] Counts logged with UTC times, LM, cloud and shower assignments.
- [ ] Report submitted to the IMO (and fireballs to the fireball form).
- [ ] Aurora decision based on Bz, speed and OVATION, not only Kp.
- [ ] Satellite passes predicted for your exact location.

## Checked
2026-11-01. Confirmed: NOAA G1 = Kp 5 and G5 = Kp 9 (NOAA Scales explanation); OVATION 30 to 90 minute lead time from L1 and intensity maps (aurora 30 minute forecast page); Bz shading at 0 and −5 nT (real-time solar wind page). Removed: limiting-magnitude and observing-angle figures, fireball magnitude, Bz -10 nT and 500 km/s rules, CME lead time, exposure times, Starlink/Iridium claims, ZHR examples (not stated on pages read). The IMO calendar PDF could not be read as text, so IMO figures were dropped rather than kept.
Method: documentation only; no commands were run.
