---
id: creative-arts.film-live-action.cinema-cameras.camera-maintenance-firmware-and-sensor-cleaning
name: camera-maintenance-firmware-and-sensor-cleaning
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, sensor-cleaning, camera-maintenance, lens-cleaning, firmware-update, camera-licences, setup-files, user-setups, black-balance, sensor-calibration]
level: practitioner
status: draft
description: "Keep cameras healthy across a shoot: firmware matching, licences and user setup files, black balance/sensor calibration, sensor and lens cleaning, and daily maintenance."
sources:
  - "https://www.arri.com/en/learn-help (ARRI - camera software updates and user setups)"
  - "https://www.red.com/download (RED - firmware and sensor calibration)"
  - "https://www.zeiss.com/consumer-products/int/service/lens-cleaning.html (ZEISS - lens cleaning)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera maintenance, firmware and sensor cleaning

**Goal:** every camera body behaves identically, settings can be restored in seconds,
and dust and dirt never reach the image.

## 1. Firmware
- At prep, put **all bodies on the same firmware** (and the same version the DIT and
  post have tested). Read release notes; don't update mid-shoot unless fixing a problem
  that affects you, and test first.
- Update procedure from the manufacturer (ARRI Camera Software Update Packet on media,
  RED firmware via media, Sony via SD): full battery/mains, never interrupt.
- **Licences**: some features (ARRI ProRes 4444 XQ, anamorphic de-squeeze, specific
  recording formats; Sony options) are licensed - confirm the rental bodies have them.

## 2. Setup files
- Save the agreed configuration (project rate, codec, resolution, LUTs, monitoring, user
  buttons, timecode) as a **user setup / look file** on media - ARRI *User Setups*, RED
  presets, Sony "All File", Blackmagic presets.
- Load the same file into every body; save a dated copy on the DIT's drive. Re-load after
  firmware updates or factory resets.

## 3. Black balance / sensor calibration
Perform the manufacturer's black balance/ black shading (with the lens cap or body cap
on) after warm-up and when temperature changes significantly (RED "Calibrate sensor",
Sony APR/black balance, Blackmagic "black shading" calibration). Prevents fixed-pattern
noise and hot pixels. ARRI cameras perform automatic black balance in many cases - check
the manual.

## 4. Sensor cleaning
- Inspect with a sensor loupe/torch at lens changes; most dust shows at deep stops
  (T11+) against bright skies - test by shooting a defocused white card at a deep stop.
- Clean the **OLPF/sensor glass** (not the sensor itself) with a blower first; then
  sensor swabs and approved fluid only if trained and the rental house allows - many
  houses prefer you return it.
- Never use canned air (propellant) or touch with fingers.

## 5. Lens and daily care
- Blower, brush, then lens tissue with lens fluid in a spiral from centre; check front and
  rear elements at every change.
- Weather: rain covers, heaters in cold, silica gel in cases, acclimatise cameras
  (condensation when moving from cold to warm - bag them).
- Daily: check mount seating and backfocus/collimation (on charts), clean viewfinder optics,
  check fans and filters for dust.

## Gotchas
- Mixed firmware between A and B camera - different colour science or metadata.
- Missing licence discovered on day one.
- Dust on the OLPF ruining sky shots at deep stops.
- Condensation inside lenses after a cold exterior.

## Verify
- [ ] All bodies on the same tested firmware; licences confirmed.
- [ ] User setup file saved, loaded in all bodies and archived.
- [ ] Black balance performed after warm-up and temperature changes.
- [ ] Sensor/lens inspections and daily care routine done.
