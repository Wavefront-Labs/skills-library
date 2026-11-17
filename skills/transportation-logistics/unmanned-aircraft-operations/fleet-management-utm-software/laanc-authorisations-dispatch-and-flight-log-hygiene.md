---
id: transportation-logistics.unmanned-aircraft-operations.fleet-management-utm-software.laanc-authorisations-dispatch-and-flight-log-hygiene
name: laanc-authorisations-dispatch-and-flight-log-hygiene
category: transportation-logistics
field: unmanned-aircraft-operations
product: fleet-management-utm-software
tags: [utm, u-space, laanc, uas-facility-map, uasfm, faa-dronezone, aloft, airspacelink, dji-flighthub-2, airdata, dronedeploy, fleet-management, mission-dispatch, multi-aircraft-monitoring, remote-id, flight-logs, battery-cycles, maintenance-tracking, drone-program-management, part-107, uk-caa, ed-269, geozones]
level: practitioner
status: gated
description: "Running a drone fleet in UTM/fleet software: LAANC and geozone authorisations, mission dispatch, live multi-aircraft alerts, and audit-ready flight, battery and maintenance logs."
sources: ["FAA LAANC public description and UAS Facility Maps (faa.gov)", "FAA 14 CFR Part 107 and Part 89 (Remote ID)", "EU Regulation 2021/664 (U-space)", "Vendor documentation: DJI FlightHub 2, Airdata UAV, Aloft (public)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LAANC authorisations, dispatch and flight-log hygiene

**Goal:** turn individual pilots and aircraft into a managed fleet: every flight
authorised, assigned, watched and recorded, so you can answer a regulator, client or
insurer within minutes.

## 1. Airspace authorisation
**US (LAANC):**
- Controlled airspace near airports is gridded by **UAS Facility Maps**; each grid cell
  shows the maximum altitude (0–400 ft AGL) that can be approved automatically.
- Request through an FAA-approved LAANC provider app (e.g. Aloft, Airspacelink,
  others): location polygon, max altitude ≤ grid value, start time and duration, pilot
  certificate. **Near-real-time approvals** arrive in seconds.
- Above the grid value (up to 400 ft, Part 107 operators only), submit **further coordination** requests well in advance (FAA search results: up to 90 days ahead, no later than 72 hours before start; processing takes hours to days, not minutes) or apply via FAADroneZone.
- Carry the approval on the flight (the app holds it) and fly only inside its
  polygon, altitude and time.
**UK/EU:** check geozones (UK: NATS Drone Assist / Altitude Angel-type services; EU
national geozone maps under the U-space framework) and apply for permission from the
aerodrome or zone owner where required. In designated U-space airspace, flights go
through a certified U-space service provider. *Rules and apps evolve quickly;
confirm current providers. EU U-space, UK service names and vendor product names were not checked (gated: unconfirmed, source is paywalled or blocked).*

## 2. Dispatching missions
- Each mission record: site, purpose/client, aircraft and payload, pilot in command and
  observer, authorisations attached, risk assessment, planned time window, weather
  limits, emergency contacts.
- Assign aircraft whose maintenance status is green and batteries with enough
  remaining cycle life.
- Push the flight plan/waypoints to the crew device (DJI FlightHub 2, DroneDeploy,
  ArduPilot via GCS) and confirm the crew loaded the current version.
- Pre-flight sign-off in the app (checklist completed) before the aircraft arms, if the
  platform supports it.

## 3. Live monitoring
- Dashboard shows each aircraft's position, altitude, battery, link quality and any
  alerts. Set alert thresholds: geofence breach, altitude > authorised, battery <
  reserve, link loss > N seconds.
- A **remote supervisor** is on a defined channel to call holds (weather, airspace
  NOTAM changes, TFRs).
- Network Remote ID / broadcast Remote ID must be active (US Part 89 standard or
  broadcast module; EU class-marked aircraft broadcast) — check the status per aircraft.

## 4. Logs and records
- Auto-sync flight logs (DJI logs, ArduPilot `.bin`/`.tlog`) to the fleet platform
  (Airdata-style) after every flight; don't rely on pilots uploading manually.
- Track per aircraft: hours, cycles, incidents, firmware version, component
  replacements; per battery: cycles, max cell deviation, swelling/damage notes.
  Retire batteries on cycle limit or on cell imbalance trends.
- Record incidents and near misses with log links; reportable accidents go to the
  regulator within its time limit (US: serious injury, loss of consciousness, or damage to property
  other than the drone above $500 repair or fair-market-value cost, within 10 calendar days, 14 CFR 107.9, confirmed on eCFR).
- Data retention per your operations manual (commonly ≥ 2 years (gated: unconfirmed, source is paywalled or blocked)).

## Gotchas
- Firmware updates pushed fleet-wide without a test aircraft first can change
  behaviour (failsafes, Remote ID) — stage them.
- Time-zone errors in authorisation windows (UTC vs. local) — fly within the local
  window shown in the approval.
- LAANC doesn't cover TFRs or national security areas — check NOTAMs/TFRs separately.

## Verify
- [ ] Every flight in the log maps to an authorisation (or a documented "uncontrolled airspace" basis).
- [ ] Aircraft and battery maintenance status checked at dispatch.
- [ ] Alerts configured for geofence, altitude, battery and link.
- [ ] Logs synced within 24 h of every flight; incidents logged with links.
