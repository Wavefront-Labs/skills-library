---
id: computing-software.systems-network-administration.frigate.frigate-birdseye
name: frigate-birdseye
category: computing-software
field: systems-network-administration
product: frigate
tags: [birdseye, birdseye-modes, activity-types, birdseye-layout, camera-order, inactivity-threshold, custom-icon]
level: intro
status: docs-checked
description: "Configure Frigate's Birdseye combined view, including activity modes, per-camera overrides, dimensions, ordering and the camera cap."
sources: ["https://docs.frigate.video/configuration/birdseye/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Birdseye view

Birdseye is a combined heads-up view of your cameras. Add the "Birdseye" camera to a Camera Group in the Live page (pencil icon in the sidebar) to see it; it can also be used in Home Assistant dashboards and cast to media devices. Each tile is built from the stream with the `detect` role, so its quality matches the detect stream resolution rather than the recording stream.

Modes under `birdseye.mode`:
- `continuous`: all cameras are always included
- `motion`: cameras with motion in the last 30 seconds are included
- `objects`: cameras that tracked an active object in the last 30 seconds are included

The 30 second window is `birdseye.inactivity_threshold` (seconds, default 30).

Per-camera overrides: `cameras.<name>.birdseye.mode` (for example `objects` on a front camera) or `enabled: False` to exclude one.

Layout: `width` and `height` (defaults 1280 and 720) set resolution, which raises quality without affecting layout; changing the aspect ratio does change the layout. `layout.max_cameras` limits how many show at once (the most recently active, with a cooldown). Cameras sort by name unless `birdseye.order` is set per camera. By default it fits two cameras per row and doubles tile size until a suitable layout is found; `layout.scaling_factor` (1.0 to 5.0, default 2.0) tunes that.

A custom background icon: place a 180x180 PNG named `custom.png` with a transparent background in the Frigate media folder; non-transparent pixels display white.

## Checked

2026-11-04. Confirmed against the Birdseye page: how to view it, detect-stream tiles, modes, the 30 second inactivity default, per-camera override, dimensions and defaults, camera order, max_cameras, scaling factor and custom.png. Fixed wrong claims: the key is `birdseye.mode` with values continuous, motion and objects (the draft listed `modes`, `all_objects`, `alerts` and `detections`, which are not on the page).
Method: documentation only; no commands were run.
