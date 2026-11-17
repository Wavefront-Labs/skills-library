---
id: computing-software.systems-network-administration.frigate.frigate-recording-retention
name: frigate-recording-retention
category: computing-software
field: systems-network-administration
product: frigate
tags: [recording, continuous-retention, motion-retention, alert-retention, pre-capture, post-capture, exports]
level: practitioner
status: docs-checked
description: "Configure Frigate recording retention for continuous, motion, alert and detection video, plus pre/post capture and exports."
sources: ["https://docs.frigate.video/configuration/record/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recording and retention

Recordings are written from the camera stream without re-encoding to `/media/frigate/recordings` as `YYYY-MM-DD/HH/<camera_name>/MM.SS.mp4` in UTC. Segments land in cache first and are only moved if they pass a validation check and match the retention policy. H.265 recordings play in Chrome 108+, Edge and Safari only. To keep a specific clip, export it; exports are stored separately and never removed by retention.

Retention keys under `record`: `continuous.days`, `motion.days`, `alerts.retain` and `detections.retain` (each with `days` and `mode` of `all`, `motion` or `active_objects`; `motion` is the default).

Presets from the docs:
- Most conservative: `continuous.days: 3`, `motion.days: 7`, alerts and detections 30 days with mode `all`.
- Reduced storage: no continuous, `motion.days: 3`, alerts and detections 30 days with mode `motion`.
- Minimum: `continuous.days: 0` and alerts retained 30 days with mode `motion`.

`alerts.pre_capture` and `post_capture` (and the same for `detections`) set the seconds of video included around a review item (default 5 seconds each, pre-capture maximum 60). They define a window, but only segments that also match the retention mode are kept.

## Checked

2026-11-04. Confirmed against the Recording page: path layout in UTC, cache validation, export advice, H.265 browser support, retention keys, the three presets, pre/post capture defaults and interaction with retention mode. Added the missing active_objects mode and the pre/post capture default and maximum.
Method: documentation only; no commands were run.
