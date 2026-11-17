---
id: computing-software.systems-network-administration.frigate.frigate-ptz-autotracking
name: frigate-ptz-autotracking
category: computing-software
field: systems-network-administration
product: frigate
tags: [ptz-autotracking, onvif-connection, autotracking-calibration, movement-weights, return-preset, zoom-factor]
level: advanced
status: docs-checked
description: "Configure Frigate PTZ object autotracking over ONVIF, including required zones, return preset, calibration and zoom modes."
sources: ["https://docs.frigate.video/configuration/autotracking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PTZ autotracking

Autotracking moves an ONVIF PTZ camera to keep a tracked object centred. The camera must support relative pan and tilt movement in its field of view (RelativePanTiltTranslationSpace); many cheaper or older PTZs do not, and Frigate logs an error and disables autotracking. The ONVIF Conformant Products Database FeatureList is a starting point for checking.

Behaviour: once an object is confirmed (not a false positive) and enters a required zone, the camera follows it until it leaves the frame or is lost. After losing it, Frigate scans that region for `timeout` seconds and tracks a new object of the same type if found, then returns to the camera's `return_preset`.

Setup: create a named preset in the camera firmware, then configure `cameras.<name>.onvif` with `host` (prefix `https://` for HTTPS), `port` (default 8000), `user`, `password`, optional `tls_insecure` and `profile` (defaults to the first profile with valid PTZ configuration). Under `onvif.autotracking`:
- `enabled` (default False; also settable over MQTT)
- `track` (default `person`) and `required_zones`
- `return_preset` (default `home`) and `timeout` (default 10 seconds)
- `zooming`: `disabled`, `absolute` or `relative`
- `zoom_factor` 0.1 to 0.75, default 0.3 (higher zooms in more but may lose the object)
- `calibrate_on_startup` and `movement_weights`
Add a motion mask over the camera timestamp and overlay text.

Calibration is optional: set `calibrate_on_startup: True` and restart; Frigate makes small and large moves (about two minutes, the UI and other cameras are unresponsive meanwhile) and writes `movement_weights` to the config. Then set it back to False, or the weights are overwritten at next start. Recalibrate by deleting `movement_weights`, and recalibrate after changing the return preset or enabling zoom.

Advice: 5 fps detect is usually enough (above 10 fps only slows it); use a fast detector, not the CPU; avoid a full-frame required zone, since tracking continues even outside it. Zooming is experimental and uses more CPU.

## Checked

2026-11-04. Confirmed against the Autotracking page: relative movement requirement and RelativePanTiltTranslationSpace, error and disable on unsupported PTZ, FeatureList advice, tracking behaviour, ONVIF and autotracking options with defaults, zoom_factor range, calibration steps and duration, 5 fps and 10 fps advice, fast detector, full-frame required zone warning and experimental zooming. Nothing removed.
Method: documentation only; no commands were run.
