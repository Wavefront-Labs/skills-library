---
id: computing-software.systems-network-administration.frigate.frigate-mqtt-topics
name: frigate-mqtt-topics
category: computing-software
field: systems-network-administration
product: frigate
tags: [mqtt-topics, mqtt-events, frigate-available, mqtt-set-topics, camera-status-topics, ptz-mqtt, topic-prefix]
level: advanced
status: docs-checked
description: "Reference for the MQTT topics Frigate publishes and subscribes to, including events, reviews, availability, camera toggles and PTZ commands."
sources: ["https://docs.frigate.video/integrations/mqtt/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Frigate MQTT topics

The default `topic_prefix` is `frigate`. In topics, use the camera, mask or zone ID from the config, not its `friendly_name` (a camera with friendly name "Back Yard" and ID `back_yard` uses `frigate/back_yard/...`).

General topics:
- `frigate/available`: `online` (republished on every broker connection), `stopped` on normal shutdown, `offline` via the broker's Will Message on an unexpected disconnect. Use it as the Home Assistant availability topic.
- `frigate/restart`: makes Frigate exit, so Docker must auto-restart the container.
- `frigate/events`: a message for each changed tracked object with `type` (`new`, `update`, `end`) and `before` / `after` objects holding id, camera, label, sub_label, scores, box, `current_zones`, `entered_zones`, `stationary`, speed fields, recognized plate and more.
- `frigate/tracked_object_update`: metadata updates keyed by event id, for GenAI descriptions, face recognition (`name`, `score`), license plates (`plate`, `plate_box`) and classification results.
- `frigate/reviews`: review item messages (`new`, `update` on severity change, new objects or recognition, then `end`).
- `frigate/stats` (same as `/api/stats`), `frigate/camera_activity` (request with `frigate/onConnect`), `frigate/profile/set` and `state`, and `frigate/notifications/set` (`ON` or `OFF`, not persisted across restarts).

Camera topics: `frigate/<camera>/status/<role>` reports `online`, `offline` or `disabled` for each of audio, detect, record and record_sub (the state of Frigate's process, not camera reachability); `frigate/<camera>/<object>` and `/active` publish object counts, with `all` as a wildcard name; `frigate/<camera>/<object>/snapshot` publishes a JPEG.

Control topics take a `/set` suffix, usually `ON` or `OFF` (`motion_threshold` and `motion_contour_area` take integers), and report on `/state`: `enabled`, `detect`, `audio`, `recordings`, `snapshots`, `motion`, `improve_contrast`, `motion_threshold`, `motion_contour_area`, `review_alerts`, `review_detections`, `birdseye`, `notifications` and `ptz_autotracker`. Masks and zones have `motion_mask/<name>`, `object_mask/<name>` and `zone/<name>` equivalents. `birdseye_modes/set` takes uppercase types such as `MOTION,ALERTS`. PTZ commands go to `frigate/<camera>/ptz`: `preset_<name>`, `MOVE_UP|DOWN|LEFT|RIGHT`, `ZOOM_IN|OUT` and `STOP`. `enabled/set` persists across restarts.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/integrations/mqtt (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Corrected the control-topic wording: most take ON or OFF but motion_threshold and motion_contour_area take integers; named the full object snapshot topic.
