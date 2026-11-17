---
id: creative-arts.film-live-action.cinema-cameras.camera-builds-and-power-distribution
name: camera-builds-and-power-distribution
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, camera-power, battery-management, power-distribution-camera, studio-build, handheld-build, build-modes, v-mount, b-mount, gold-mount, d-tap, battery-shipping]
level: practitioner
status: draft
description: "Configure studio, handheld and gimbal camera builds and power them: battery mounts and capacity, distribution and D-tap, block batteries, charging rotation and shipping rules."
sources:
  - "https://www.arri.com/en/camera-systems/camera-accessories (ARRI - camera accessories and power distribution)"
  - "https://www.idxtek.com (IDX - V-mount batteries and power)"
  - "https://www.iata.org/en/programs/cargo/dgr/lithium-batteries/ (IATA - lithium battery transport rules)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera builds and power distribution

**Goal:** the camera switches between builds in minutes and never loses power mid-take.

## 1. Build configurations
| Build | Typical components |
|---|---|
| **Studio** | Bridge plate + 15/19 mm studio rods, large matte box with 4x5.65 filter stages, follow focus (wireless motors), large monitor, block battery or mains, top handle |
| **Handheld** | Shoulder pad, handgrips, lightweight rods, clip-on matte box, compact wireless video, rear battery as counterweight |
| **Steadicam/gimbal** | Minimum weight, no rods, clip-on matte box or none, lens motors, wireless everything, power from the sled |
| **Car/crash/remote** | Locked-off, remote record and lens control, armoured housing |
Pre-build each configuration in prep; photograph and label the parts in cases ("handheld kit")
so the change on set takes <5 minutes. Keep the camera's **centre of gravity** in mind
for gimbals - balance changes with lens choice.

## 2. Power sources
- **On-board batteries**: V-mount (most common), Gold-mount (Anton Bauer), **B-Mount**
  (ARRI's newer standard with 24 V) - match camera voltage (12 V vs 24 V) and current draw
  (Alexa 35 with accessories can draw 100+ W).
- Capacity: Wh rating / draw = runtime (a 150 Wh battery at 90 W ~ 1.5 h, less in cold).
- **Block batteries** (on the dolly) or **mains** (AC adaptors) for studio builds -
  continuous power; hot-swap without shutting down.

## 3. Distribution
Power distribution boxes split the battery to accessories via **D-tap**, 2-pin LEMO,
3-pin Fischer. Avoid daisy chains of cheap D-tap splitters. Check accessory voltages
(some motors need 24 V). Label cables.

## 4. Battery management
- Number batteries; rotate: on camera -> charger -> ready. Mark charged ones (tape/ label).
- Keep **two charged per camera at all times**; more in cold or on high-draw builds.
- Cold reduces capacity - keep spares warm.
- Hot-swap: cameras with dual inputs or a hot-swap plate allow battery changes without
  rebooting.

## 5. Shipping and travel
Lithium-ion batteries >100 Wh need airline approval and are limited to two per
passenger (100-160 Wh) in carry-on; >160 Wh require cargo (dangerous goods) shipping.
Check IATA and airline rules; protect terminals.

## Gotchas
- 12 V batteries on a 24 V accessory - fails or underperforms.
- Losing a take to a battery swap because no hot-swap.
- Batteries checked into hold luggage.
- Builds improvised on the day.

## Verify
- [ ] Each build pre-assembled in prep; parts cased and labelled.
- [ ] Battery standard and voltage match camera and accessories; runtime calculated.
- [ ] Rotation and charging system with numbered batteries.
- [ ] Shipping/travel compliance checked for batteries.
