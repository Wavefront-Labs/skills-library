---
id: transportation-logistics.space-traffic-management.launch-reentry-screening.launch-cola-windows-and-reentry-prediction
name: launch-cola-windows-and-reentry-prediction
category: transportation-logistics
field: space-traffic-management
product: launch-reentry-screening
tags: [launch-cola, collision-on-launch-assessment, launch-window, cola-closures, blackout-periods, reentry-prediction, tip, tracking-and-impact-prediction, debris-footprint, uncontrolled-reentry, controlled-reentry, casualty-risk, spaceflight, iss, crewed-vehicle, space-traffic-management, notam, navigational-warning, solar-flux]
level: advanced
status: draft
description: "Screening launch trajectories for COLA blackout periods inside a window, and reading reentry predictions (TIP windows, footprints) without over-trusting the predicted time."
sources: ["NASA Spacecraft Conjunction Assessment Best Practices Handbook (2023)", "ESA Space Debris Office reentry prediction notes", "Space-Track TIP message documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Launch COLA windows and reentry prediction

**Goal:** get a launch away without passing too close to tracked objects (especially
crewed stations), and handle reentries with honest uncertainty.

## Part A — Launch collision avoidance (COLA)
1. **Provide the trajectory.** The launch provider supplies nominal trajectories for
   every stage, payload and jettisoned item (fairing, adapters) across the window, at
   several liftoff times (e.g. every 1 s or 10 s of the window), in a format the
   screener accepts (state vectors with epoch relative to liftoff).
2. **Screen against the catalogue** from liftoff to the end of the screening period —
   usually through orbit insertion plus a few hours, or until first catalog
   tracking of the new objects.
3. **Criteria.** Typical practice uses a stand-off distance against crewed or
   crew-capable objects (often a large ellipsoid or ~200 km class spherical criterion)
   and a Pc or miss-distance criterion against other active and debris objects.
   *Values are set by the range or regulator (e.g. licence conditions); confirm the
   ones in your launch licence rather than relying on these orders of magnitude.*
4. **Result:** a list of **COLA closures** — seconds within the window where liftoff
   is prohibited. Feed them to the countdown team as hard no-launch times.
5. **Refresh** the screening with the latest catalogue close to launch (common
   practice: final run within ~hours of window open) and after any trajectory change.
Gotchas: a short window with closures can leave only a few usable seconds — make
sure the launch-control software and the countdown clock agree on UTC to the second;
recycle holds must re-check the closure list for the new T-0.

## Part B — Reentry prediction
- **Inputs:** latest OD with solved ballistic coefficient, forecast solar flux
  (F10.7) and geomagnetic index (Ap), object mass/area if known.
- **Product:** a predicted reentry epoch with a window. Rule of thumb: the uncertainty
  is roughly **±20 % of the remaining orbital lifetime** — a prediction 5 days out is
  ±1 day; 2 hours out is still ±~25 minutes. At 7.5 km/s, ±25 min is more than a full
  orbit of ground track.
- **TIP messages** (Tracking and Impact Prediction) on Space-Track give updated epoch,
  window and a location *at the nominal time only* — treat the location as almost
  meaningless until the final hours.
- **Footprint:** surviving debris (tanks, engine parts, titanium/steel) spreads along
  track over hundreds to ~1,000+ km. Casualty risk is assessed against the population
  under the possible ground tracks — regulators commonly cap uncontrolled reentry
  risk at ~1 in 10,000 per event (*e.g. US ODMSP; check your regulator*).
- **Controlled reentry:** plan a deorbit burn into a remote ocean zone, coordinate
  navigational warnings (NAVAREA) and NOTAMs for the impact area, and screen the
  deorbit trajectory against the catalogue like a launch.

## Gotchas
- Solar-activity forecasts are the dominant error; a geomagnetic storm can pull a
  reentry forward by hours to days.
- Tumbling objects have changing drag; solved ballistic coefficients jump.
- Communicate windows, not times: "between 14:00 and 20:00 UTC" — publishing a single
  location early causes needless alarm.

## Verify
- [ ] COLA closures generated from the latest catalogue and loaded into the countdown timeline.
- [ ] Every jettisoned object has a screened trajectory.
- [ ] Reentry products quoted with a window that respects the ~20 % rule.
- [ ] For controlled reentry: deorbit trajectory screened, warnings issued for the impact zone.
