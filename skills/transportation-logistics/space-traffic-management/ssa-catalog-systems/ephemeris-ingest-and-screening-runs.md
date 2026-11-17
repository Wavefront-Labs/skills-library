---
id: transportation-logistics.space-traffic-management.ssa-catalog-systems.ephemeris-ingest-and-screening-runs
name: ephemeris-ingest-and-screening-runs
category: transportation-logistics
field: space-traffic-management
product: ssa-catalog-systems
tags: [ssa, space-situational-awareness, space-domain-awareness, catalog, space-track, gp, tle, omm, oem, ccsds, ephemeris, conjunction-screening, screening-volume, cdm, sgp4, norad-id, cospar-id, owner-operator-ephemeris, leolabs, comspoc, eu-sst, stm]
level: practitioner
status: draft
description: "Pulling GP/TLE data from Space-Track, submitting owner-operator ephemeris in CCSDS OEM, and configuring conjunction screening runs (volumes, spans, cadence) without silent data gaps."
sources: ["https://www.space-track.org/documentation", "CCSDS 502.0-B Orbit Data Messages", "CCSDS 508.0-B Conjunction Data Message", "NASA Spacecraft Conjunction Assessment and Collision Avoidance Best Practices Handbook (2023)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ephemeris ingest and screening runs in an SSA catalog

**Goal:** keep your own satellites' trajectories in the catalogue correctly, pull the
catalogue you screen against, and run screenings whose results you can trust — the
most common failure is not bad maths but a stale or mis-framed input nobody noticed.

## 1. Know your data products
| Product | What it is | Use for | Don't use for |
|---|---|---|---|
| GP / TLE / OMM (Space-Track `gp` class) | SGP4 mean elements | Situational overview, coarse filtering | Pc calculation — no covariance, km-level error |
| Special-perturbations (SP) ephemeris | Precise numerical orbit + covariance | Screening by 18th/19th SDS, CARA, EU SST | Not public; arrives via CDMs |
| Owner/operator ephemeris (CCSDS OEM) | Your predicted trajectory incl. planned burns | Submit so screeners see your manoeuvres | Without covariance it may be screened but Pc quality suffers |
| CDM (CCSDS 508) | Conjunction result: TCA, miss distance, covariances, Pc | Assessment | Treating one CDM as final — watch the trend |

## 2. Pulling catalogue data (Space-Track)
Log in once per session, then query the `gp` class rather than legacy `tle` classes:
```
POST https://www.space-track.org/ajaxauth/login   (identity, password from your account)
GET  https://www.space-track.org/basicspacedata/query/class/gp/NORAD_CAT_ID/25544/format/json
GET  .../class/gp/EPOCH/>now-1/orderby/NORAD_CAT_ID/format/omm   # recent full-catalogue delta
GET  .../class/cdm_public/SAT_1_ID/<your NORAD id>/orderby/TCA desc/format/json
```
- Respect the published rate limits (order of tens of queries per minute and a few
  hundred per hour; check the current figures in the documentation) — pull the full
  catalogue at most a few times a day and use `EPOCH>now-x` deltas in between.
- Store `CREATION_DATE` and `EPOCH` of every element set; screening against
  element sets several days old is the classic hidden error.
- Five-digit catalogue numbers are running out; use OMM/JSON fields (`NORAD_CAT_ID`
  as an integer) and do not parse fixed TLE columns in new code.

## 3. Submitting owner/operator ephemeris
1. Generate OEM from your flight-dynamics system with **frame and time stated
   explicitly** (`REF_FRAME = EME2000` or `ITRF`, `TIME_SYSTEM = UTC`), covariance
   block if you have it, step ≤ 60 s in LEO.
2. Include every **planned manoeuvre** in the predicted span; label it operational
   vs. a candidate avoidance ephemeris so the screener runs the right one.
3. Cover at least the screening window (typically 7 days LEO; longer beyond).
4. Upload on a fixed cadence (e.g. after each OD update, at least daily) and check
   the acknowledgement/screening receipt; no receipt = assume not screened.

## 4. Configuring a screening run (your own tool or a commercial service)
- **Primary set:** your assets, from your best ephemeris (not GP).
- **Secondary set:** full catalogue, plus other operators' shared ephemerides.
- **Screening volume:** an ellipsoid or box in the primary's radial/in-track/cross-track
  frame. In-track is always largest because along-track error grows fastest. As an
  order of magnitude, LEO screening volumes are ~1–2 km radial by tens of km
  in-track/cross-track, GEO volumes far larger — use the values in your provider's
  service agreement (*unconfirmed which current exact values each provider uses*).
- **Span and cadence:** 7 days ahead, rerun at least every 8 hours and immediately
  after any new primary ephemeris or manoeuvre plan.
- **Outputs:** CDM per event, ordered by Pc then by miss distance, with object type
  (payload/debris/rocket body) and size proxy (RCS).

## Gotchas
- **Frame mix-ups** (TEME from SGP4 vs. J2000 vs. ITRF) produce kilometre errors
  that look like real close approaches — tag every file with its frame.
- **Leap seconds and UTC vs. TAI** offsets of 37 s move a LEO object ~280 km along track.
- Debris from a fresh breakup may be **uncatalogued for days**; an empty screening
  after a breakup in your shell is not reassurance.
- A screening service that silently fails to ingest your file will keep screening the
  last good one — check the ephemeris ID/start time on every CDM.

## Verify
- [ ] Every primary ephemeris in the last run has a timestamp < 24 h old and covers the full span.
- [ ] Frame and time system are declared in every OEM header.
- [ ] CDMs reference the ephemeris you last uploaded (check the originator/ID fields).
- [ ] Planned manoeuvres appear in the screened trajectory.
- [ ] You can name the screening volume and span your provider is using.
