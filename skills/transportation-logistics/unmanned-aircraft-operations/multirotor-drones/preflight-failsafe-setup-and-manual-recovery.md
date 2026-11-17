---
id: transportation-logistics.unmanned-aircraft-operations.multirotor-drones.preflight-failsafe-setup-and-manual-recovery
name: preflight-failsafe-setup-and-manual-recovery
category: transportation-logistics
field: unmanned-aircraft-operations
product: multirotor-drones
tags: [multirotor, quadcopter, drone, uas, suas, dji, dji-pilot-2, dji-fly, ardupilot, px4, preflight-checklist, return-to-home, rth, rth-altitude, failsafe, lost-link, atti-mode, gps-loss, compass-interference, imu, battery-management, lipo, cold-weather, wind-limits, precision-hover, payload-release]
level: practitioner
status: gated
description: "Multirotor preflight and failsafe setup (RTH altitude, lost-link action, battery thresholds) and how to fly out of GPS loss or compass errors in attitude mode without panicking."
sources: ["https://ardupilot.org/copter/docs/radio-failsafe.html", "https://ardupilot.org/copter/docs/gcs-failsafe.html", "https://docs.px4.io/main/en/config/safety.html", "https://www.ecfr.gov/current/title-14/section-107.51"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preflight failsafe setup and manual recovery

**Goal:** make sure the aircraft does something sensible when things go wrong, and be
able to fly it home yourself when the automation can't. Settings named for DJI
Pilot 2 / DJI Fly and ArduPilot/PX4; menus move between firmware versions.

## 1. Set failsafes for *this* site, every flight
- **RTH altitude:** above the tallest obstacle on any path home (trees, masts,
  buildings) plus margin — commonly obstacle + 20 m, but never above the legal ceiling
  (e.g. 400 ft AGL under US Part 107.51, or lower where local rules apply). A default 100 m RTH can hit a wind turbine; a default 30 m
  can hit trees.
- **Lost-link action:** RTH (default for most), Hover, or Land. Choose Hover/Land when
  RTH would fly over people or into airspace you aren't cleared for.
  ArduPilot: `FS_THR_ENABLE` (radio), `FS_GCS_ENABLE`; PX4: `NAV_RCL_ACT`, `COM_RC_LOSS_T`.
- **Home point:** confirm it updated to your take-off location (or set it to your
  position for moving launch sites) before leaving the area.
- **Low-battery actions:** low-battery warning around 25–30 %, critical (auto-land)
  around 10–15 % (gated: unconfirmed, source is paywalled or blocked). Plan to be landed with ≥ 20–25 % (gated: unconfirmed, source is paywalled or blocked).
  ArduPilot: `BATT_LOW_VOLT/MAH`, `BATT_FS_LOW_ACT`.
- **Obstacle sensing:** know whether it's on and which directions it covers — many
  aircraft have none sideways in some modes, and sensing is off in sport/ATTI modes.

## 2. Preflight checks (beyond the walk-round)
- Props undamaged and seated, arms locked, gimbal clamp removed, payload secured.
- Battery: charged, warm (> ~15 °C in cold weather), cells balanced, firmware match.
- GNSS: enough satellites and a home point lock; IMU and compass status OK. Don't take
  off next to steel structures, reinforced concrete, vehicles or rebar — move to a
  clean spot to avoid **compass interference** warnings in the air.
- Hover test at 2–3 m for 10–20 s: drift, vibration, abnormal sound, controls correct.

## 3. When the aircraft switches to attitude (ATTI) mode
Causes: GNSS loss (near buildings, under bridges), compass error, or flying indoors.
In ATTI the aircraft holds altitude but **not position — it drifts with the wind**.
1. Don't panic or grab the sticks hard. Climb gently away from obstacles if safe.
2. Orient: use the camera view and map; identify which way the wind is pushing.
3. Counter the drift with small, steady pitch/roll inputs — fly it like a helicopter.
4. Fly toward open space and GNSS reception; it may recover positioning by itself.
5. Land early in a clear area rather than attempting a long transit.
Practise this deliberately in a large open field at height (most apps let you select
ATTI, or ArduPilot `ALT_HOLD`) until it's boring.

## 4. Wind and payload
- Respect the manufacturer's max wind (often ~12 m/s for small enterprise models (gated: unconfirmed, source is paywalled or blocked)) but
  plan for **gusts at altitude** being stronger than ground readings.
- Fly out **upwind** so the return leg is downwind and battery-cheap.
- Payload release/drops: confirm drop area clear, release at low height, and expect
  a jump in altitude/attitude when mass is shed.

## Gotchas
- Calibrating the compass near metal makes it worse — calibrate only when prompted and
  in a clean location.
- "Return to home" with a moving pilot (boat, vehicle) returns to where you *were*.
- Cold LiPo voltage sags under load → sudden critical battery landing.
- *Parameter names checked against the ArduPilot and PX4 documentation (see Checked); check your
  firmware version.*

## Verify
- [ ] RTH altitude set above site obstacles and below the legal ceiling.
- [ ] Lost-link action chosen for this site and home point confirmed.
- [ ] Battery thresholds set; landing planned with ≥ 20 %.
- [ ] Hover test done with no warnings.
- [ ] You have practised ATTI/ALT_HOLD flight within the last few months.

## Checked

Jurisdiction: US Part 107 altitude limit; autopilot parameters are vendor-neutral. Checked 2026-10-25: ArduPilot radio failsafe page (FS_THR_ENABLE), ArduPilot GCS failsafe page (FS_GCS_ENABLE), PX4 safety configuration page (NAV_RCL_ACT failsafe action and COM_RC_LOSS_T timeout, RC loss actions Disabled, Loiter, Return, Land, Disarm, Terminate, Hold), 14 CFR 107.51 (400 ft AGL). DJI manual figures and battery thresholds were not confirmed and are marked gated.

Method: documentation only; no commands were run.
