---
id: computing-software.systems-network-administration.frigate.frigate-masks-and-motion-tuning
name: frigate-masks-and-motion-tuning
category: computing-software
field: systems-network-administration
product: frigate
tags: [motion-masks, object-filter-masks, motion-threshold, contour-area, lightning-threshold, improve-contrast, skip-motion-threshold]
level: advanced
status: docs-checked
description: "Choose between zones, motion masks and object filter masks, and tune Frigate's motion threshold, contour area, lightning threshold and skip-motion options."
sources: ["https://docs.frigate.video/configuration/masks/", "https://docs.frigate.video/configuration/motion_detection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Masks and motion detection tuning

Masks are narrow fine-tuning tools, not a way to hide an area. Which tool:
- Alert only on activity in areas you care about: a zone with `required_zones`.
- Stop a stubborn false positive at a fixed spot (a tree base seen as a person): an object filter mask for that object type; it uses the bottom center of the detected object.
- Ignore motion that is obviously not of interest (camera timestamp, sky, flags, treetops): a motion mask.

How motion and detection interact: motion is a first-line check, nearby motion is grouped into motion boxes (red in the debug view), then a square region (green) is built around it for the model, with a margin. If objects look cut off, Frigate reframes the region and runs detection again.

Tuning order: create motion masks for regular unwanted motion using the debug view with Motion Boxes on, then use the Motion Tuner in Settings, Camera configuration. Tune under normal conditions, not a windy sunny day only. Settings:
- `threshold` (luminance change per pixel; higher is less sensitive)
- `contour_area` (minimum size of a motion area; default 10)
- `improve_contrast`
- `lightning_threshold` (default 0.8): large changes such as PTZ moves or IR switching pause object detection and recalibrate, but do not stop motion recordings; raise it for doorbell cameras that miss people walking close.
- `skip_motion_threshold` (0.0 to 1.0, unset by default): ignore all motion in a frame when that fraction changes, which also suppresses recordings, unlike `lightning_threshold`.

## Checked

2026-11-04. Confirmed against the Masks and Motion Detection pages: which-tool guidance, bottom-center rule for object filter masks, red motion boxes and region reframing, tuning advice, threshold, contour_area default 10, lightning_threshold default 0.8 and its effect on recordings, and skip_motion_threshold range 0.0 to 1.0 with unset disabling it. Nothing removed.
Method: documentation only; no commands were run.
