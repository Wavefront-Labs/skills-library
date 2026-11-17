---
id: transportation-logistics.navigation-wayfinding.celestial-navigation.sextant-sight-to-position-line
name: sextant-sight-to-position-line
category: transportation-logistics
field: navigation-wayfinding
product: celestial-navigation
tags: [celestial-navigation, astro-navigation, sextant, navigation-wayfinding, sight-reduction, intercept-method, marcq-st-hilaire, nautical-almanac, hs-ho-hc, index-error, dip, refraction, semi-diameter, gha, lha, declination, noon-sight, meridian-passage, latitude-by-noon-sight, polaris, star-identification, twilight-star-sights, ho-229, ho-249, chronometer, utc, running-fix]
level: advanced
status: draft
description: "Take a sextant sight and turn it into a position line: index error, dip and refraction corrections, almanac GHA/declination, intercept sight reduction, plotting, plus noon-latitude and star timing."
sources: ["Nautical Almanac (UKHO/USNO)", "Pub. 229 / Pub. 249 sight reduction tables"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sextant sight to position line — fixing position from the sky

**Goal:** measure a celestial body's altitude, correct it, compare with the altitude
calculated for an assumed position, and plot the resulting line of position (LOP).
Two or more LOPs make a fix. Needs: sextant, accurate UTC time (to the second), the
current **Nautical Almanac**, and sight reduction tables (Pub. 229/249) or a calculator.

## 1. Check the sextant
- **Index error (IE):** set index to 0°, look at the horizon (or a star); if the two
  horizon images don't line up, bring them together and read the error. Reading
  "on the arc" (positive) → subtract; "off the arc" → add ("If it's on, take it off").
- Check perpendicularity and side error periodically; adjust only if large.

## 2. Take the sight
- **Sun (lower limb):** bring the sun down to the horizon, **rock** the sextant
  (swing) so the sun traces an arc; the lowest point of the arc just touching the
  horizon is the vertical. Shout "mark" and note UTC to the second.
- **Stars/planets:** at nautical twilight (horizon visible, stars visible) — ~30–45 min
  after sunset or before sunrise. Pre-compute which stars and their approximate altitude
  and azimuth so you can find them quickly.
- Take several sights of the same body, plot altitude vs time, and use a consistent one.
- Note height of eye (for dip).

## 3. Correct the altitude (Hs → Ho)
1. Hs (sextant) ± IE = **Hs corrected**.
2. − **Dip** (from height of eye: ≈ 1.76′ × √(h in m)) = **apparent altitude Ha**.
3. Apply the almanac's **main correction** (refraction, plus semi-diameter and
   parallax for sun/moon; refraction only for stars) → **observed altitude Ho**.
4. Non-standard temperature/pressure corrections for low altitudes (<10°); avoid
   sights below ~10–15° where refraction is uncertain.

## 4. From almanac to calculated altitude
1. From the almanac daily page: **GHA** and **declination** for the hour of UTC; add the
   increments for minutes and seconds (and v/d corrections).
2. Choose an **assumed position (AP)**: latitude rounded to the nearest whole degree;
   longitude chosen so that **LHA = GHA + east longitude (− west)** is a whole degree.
3. Enter the tables with latitude, LHA, declination → **Hc** (calculated altitude) and
   **Zn** (true azimuth).

## 5. Intercept and plot (Marcq St Hilaire)
- **Intercept** = Ho − Hc, in minutes of arc = nautical miles.
- Positive (Ho > Hc): "**Towards**" the body. Negative: "**Away**". (HoMoTo — "Ho more
  toward".)
- From the AP, draw the azimuth line Zn, measure the intercept toward or away, draw the
  LOP perpendicular to the azimuth.
- Fix: cross LOPs from bodies with azimuths 60–120° apart (three stars ~120° apart
  give a cocked hat — take the centre, beware systematic errors). For sun lines at
  different times, advance the earlier LOP by the run between (running fix).

## 6. Noon sight (latitude without tables)
At local meridian passage, the sun peaks. Watch the altitude stop rising; take the
maximum Ho. Then:
- **Zenith distance z = 90° − Ho**, named **opposite** to the sun's bearing (sun bears
  S → z is named N).
- If z and declination have the **same name**: Lat = z + Dec. If **contrary names**:
  Lat = the difference, named after the larger.
- Example: sun bears S, Ho = 50°, Dec = 10° N → z = 40° N, same name → Lat = 50° N.
  Same sight with Dec = 10° S → contrary → Lat = 30° N.
Polaris altitude, corrected with the almanac's Polaris tables, gives latitude directly in
the northern hemisphere.

## Gotchas
- Time errors: 4 seconds of time ≈ 1′ of longitude ≈ up to 1 nm at the equator.
- Wrong year's almanac, or the wrong day column.
- IE sign reversed; dip applied twice.
- Haze or a false horizon (land, swells) gives systematic errors.

## Verify
- [ ] IE measured and applied with the correct sign.
- [ ] Each sight timed to the second with UTC.
- [ ] Hs → Ho corrections written in a standard sight form.
- [ ] Intercept direction correct (HoMoTo); LOP perpendicular to azimuth.
- [ ] Fix compared with DR position; difference explained.

*Uncertainty:* dip formula and twilight timings are approximate; use the almanac's tables and a standard sight form, and check the method against a worked example before relying on it at sea.
