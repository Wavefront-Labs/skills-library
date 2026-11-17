---
id: computing-software.systems-network-administration.frigate.frigate-license-plate-recognition
name: frigate-license-plate-recognition
category: computing-software
field: systems-network-administration
product: frigate
tags: [license-plate-recognition, lpr, known-plates, plate-format-regex, replace-rules, plate-enhancement, dedicated-lpr-camera]
level: advanced
status: docs-checked
description: "Enable Frigate license plate recognition, match known plates, filter by length and format, normalise OCR errors and debug captured plate text."
sources: ["https://docs.frigate.video/configuration/license_plate_recognition/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# License plate recognition

LPR adds recognized text as `recognized_license_plate`, or a known name as `sub_label`, on tracked `car`, `motorcycle` and similar objects. Results show in Review, Explore details, filters and MQTT (`frigate/events` and `frigate/tracked_object_update` with `name` and `plate`). Models download once; afterwards it runs offline. It works best with a clearly visible plate and keeps refining while a vehicle moves.

Models: a Frigate+ or custom model that detects `license_plate` natively needs it in the tracked objects; otherwise a lightweight YOLOv9 plate detector runs on CPU or GPU and you should not define `license_plate`. In default mode a vehicle must be detected first; a dedicated, zoomed-in LPR camera can run without that (see the docs). OCR is PaddleOCR.

Enable globally with `lpr.enabled: True`; disable per camera with `cameras.<name>.lpr.enabled: False`. Camera-level options are only `enabled`, `min_area` and `enhancement`. It runs on the `detect` stream.

Settings and defaults:
- Detection: `detection_threshold` 0.7, `min_area` 1000 pixels (area, roughly 32x32), `device` auto (CPU, GPU or device number), `model_size` small (Latin and Chinese characters) or large (Latin only).
- Recognition: `recognition_threshold` 0.9, `min_plate_length`, and `format` a regex such as `^[A-Z]{2}[0-9]{2} [A-Z]{3}$`; non-matching plates are discarded.
- Matching: `known_plates` maps a name to plate patterns (wildcards such as `J*N-*234`), and `match_distance: 1` tolerates one missing or wrong character.
- `enhancement` 0 to 10 (default 0); raise only when plates are readable by eye but misread.
- `replace_rules`: global ordered regex rules to normalise OCR (for example `O` to `0`, `I` to `1`, `(\w{3})(\w{3})` to `\1-\2`); changes appear in the LPR debug log.
- `debug_save_plates: True` saves text crops to `/media/frigate/clips/lpr/<camera>/<event_id>`.

## Checked

2026-11-04. Confirmed against the License Plate Recognition page: recognized_license_plate and sub_label fields, MQTT topics, YOLOv9 detector and PaddleOCR, vehicle-first default mode and dedicated LPR cameras, global enable and per-camera disable, camera-level options, defaults (0.7, 1000 pixels, 0.9), model sizes, format regex, known_plates wildcards, match_distance, enhancement 0 to 10, replace_rules and debug_save_plates path. Nothing removed.
Method: documentation only; no commands were run.
