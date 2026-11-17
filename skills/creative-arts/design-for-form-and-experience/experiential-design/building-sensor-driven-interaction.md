---
id: creative-arts.design-for-form-and-experience.experiential-design.building-sensor-driven-interaction
name: building-sensor-driven-interaction
category: creative-arts
field: design-for-form-and-experience
product: experiential-design
tags: [sensor-interaction, sensor-driven-installations, interactive-sensing, presence-detection, motion-tracking, immersive-installations]
level: advanced
status: draft
description: "Build sensor-driven interaction for installations: choose sensors by task, map data to media, filter and calibrate, handle reliability, privacy and failures."
sources:
  - "TouchDesigner documentation (derivative.ca)"
  - "OpenCV documentation (opencv.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sensor-driven interaction

Interactive installations respond to visitors through sensors. The challenge is robust sensing in a real, crowded, unpredictable environment.

## Choose the sensor by the question
- **Presence or entry:** PIR sensors, pressure mats, break-beam, time-of-flight or mmWave radar.
- **Position and tracking:** depth cameras, lidar scanners, overhead cameras with computer vision (OpenCV), or ultrasonic sensors.
- **Touch:** capacitive touch sensors, touch frames, buttons; **proximity** with capacitive or IR.
- **Gesture and pose:** depth cameras with body tracking, or camera-based pose estimation software.
- **Sound:** microphones and level analysis.
Availability of particular products changes (some consumer depth cameras have been discontinued), so check what is supported before design.

## Pipeline
1. **Capture** with the sensor; wire with correct cable length and shielding, or network connections.
2. **Process:** filter noise (smoothing, thresholds with hysteresis), track blobs or skeletons, define zones.
3. **Map** to media parameters (position to light, proximity to volume), with easing so responses look fluid; use OSC, MIDI or serial to send to your media software.
4. **Calibrate** on site at the same lighting and floor as the show; define what happens with many people and with none.
5. **Fail safe:** a default idle loop if sensors fail; watchdogs and logging.

## Constraints
- Sunlight and reflective surfaces disturb infrared and camera sensors.
- Latency makes interaction feel broken; aim to keep it low and test (a delay beyond about 100 ms is noticeable for direct manipulation).
- **Privacy and consent:** cameras capture people; process locally, avoid storing identifiable video, and post notices (check local law).

## Verify
- [ ] The installation behaves sensibly with zero, one and many visitors.
- [ ] Idle mode runs if a sensor drops.
- [ ] No identifiable footage is stored unless disclosed and lawful.
