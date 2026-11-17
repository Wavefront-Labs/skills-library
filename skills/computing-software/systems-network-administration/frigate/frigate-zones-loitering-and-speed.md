---
id: computing-software.systems-network-administration.frigate.frigate-zones-loitering-and-speed
name: frigate-zones-loitering-and-speed
category: computing-software
field: systems-network-administration
product: frigate
tags: [zones, required-zones, loitering-time, zone-inertia, speed-estimation, zone-coordinates]
level: advanced
status: docs-checked
description: "Define Frigate zones, tie alerts to required zones, set loitering time and inertia, and estimate object speed with a four-point ground-plane zone."
sources: ["https://docs.frigate.video/configuration/zones/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zones in Frigate

A zone is a polygon on a camera image. Presence is evaluated on the bottom center of an object's bounding box. Zone names cannot equal a camera name, and cameras that cover the same area can use the same zone name. Zones can be toggled off without deleting them; disabled zones are ignored. Create them in Settings, Camera configuration, Masks / Zones, or in YAML: `cameras.<cam>.zones.<name>.coordinates: 0.123,0.456,...` (relative coordinates) with an optional `friendly_name`.

Alerts per zone: set `review.alerts.required_zones` (for example `entire_yard`) so an object must enter that zone to count as an alert, and `review.detections.required_zones` for a secondary area.

`loitering_time` (seconds) makes a zone hold a review item open: a person in a loitering zone keeps the item active until they leave even if stationary; other objects keep it active until the time is met, after which a stationary object ends it. `inertia` is the number of consecutive frames an object must be inside before counting as in the zone (default 3), guarding against slightly wrong boxes.

Speed estimation needs a zone of exactly four points aligned to the ground plane and `distances` listing the real-world distance between consecutive points (meters or feet per `ui.unit_system`, metric giving km/h). Place the zone away from where objects enter and exit, because estimation needs a minimum number of tracked frames; the docs suggest decreasing the zone's inertia from the default of 3 (their example uses 1). A `speed_threshold` can then be applied.

## Checked

2026-11-04. Confirmed against the Zones page: bottom-center presence, camera-name restriction, toggling zones, coordinates and friendly_name, required_zones for alerts and detections, loitering behaviour, inertia default 3, speed estimation with exactly four points, distances, unit_system and speed_threshold. Reworded the inertia advice to match the page.
Method: documentation only; no commands were run.
