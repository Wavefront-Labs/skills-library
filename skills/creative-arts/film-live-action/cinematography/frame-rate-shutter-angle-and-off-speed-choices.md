---
id: creative-arts.film-live-action.cinematography.frame-rate-shutter-angle-and-off-speed-choices
name: frame-rate-shutter-angle-and-off-speed-choices
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, frame-rate-choice, hfr, 24-vs-25, motion-blur, narrow-shutter, shutter-style, undercrank, off-speed, in-camera-ramp, 23-976, project-frame-rate]
level: practitioner
status: draft
description: "Choose frame rate and shutter: 23.976/24/25/29.97 for delivery and territory, HFR, shutter angle as motion style, and under/overcranking and in-camera ramps."
sources:
  - "American Cinematographer Manual (ASC, 11th ed.) - frame rates and shutter"
  - "https://partnerhelp.netflixstudios.com (Netflix Partner Help Center - frame rate requirements)"
  - "Blain Brown, Cinematography - Theory and Practice (shutter angle and motion)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Frame rate, shutter angle and off-speed choices

**Goal:** a project frame rate that suits the deliverables everywhere, and shutter and
speed choices made deliberately for the look.

## 1. Project (base) frame rate
| Rate | Use |
|---|---|
| **23.976** | US/streaming drama and features finished for NTSC-legacy and streaming; most common for streamers |
| **24.000** | Theatrical/DCP features (DCP is 24 fps); many features shoot true 24 |
| **25** | PAL territories' broadcast (UK/EU TV), avoids 50 Hz flicker issues |
| **29.97 / 30** | US broadcast TV, sport-style, some web |
| **48 / 60 / 120 (HFR)** | High frame rate presentations, sports, some VR - a strong "video" look for drama |
Decide with post and the distributor **before** the shoot: every camera, sound recorder
(timecode rate) and slate must match. Mixing 24 and 23.976 causes sync drift (0.1%).
Conversions between 24 and 25 change speed (4%) or require frame blending.

## 2. Shutter angle as style
- **180 degree** (exposure = half the frame interval): "normal" motion blur.
- **Narrow shutter** (45-90 degree): crisp, staccato motion - action (e.g. Saving Private
  Ryan's battle scenes), stress, war, rain/sparks that read as streaks. Costs 1-2 stops.
- **Wide shutter** (270-360 degree): smeary, dreamy motion, extra light; long-lens
  handheld can look "video-ish".
- Keep flicker-safe values in mind (see flicker skill).

## 3. Off-speed
- **Overcranking** (higher fps, played at base): slow motion - 48 fps = 50%, 120 = 20%.
- **Undercranking** (lower fps): speeds action up - fights and car stunts at 20-22 fps for
  extra energy subtly, 12-18 fps for comedy/fast motion. Keep shutter for blur control.
- Sound is MOS or wild for off-speed takes; slate with the fps written.
- **In-camera ramps**: some cameras (RED, ARRI, Sony Venice) ramp fps during a take
  with exposure compensation (shutter or ND/iris) - test; post ramps (optical flow)
  are more flexible but need higher capture rates.
Exposure: doubling fps loses a stop at the same shutter angle.

## Gotchas
- Cameras at 24.000 and sound at 23.976 timecode - sync drift.
- 25 fps project delivered to a 23.976 streamer without a plan.
- Undercranked shots with dialogue.
- Narrow shutter chosen for one scene and forgotten in the next.

## Verify
- [ ] Project rate agreed with post/distributor and set on all devices.
- [ ] Shutter style per scene noted in camera reports.
- [ ] Off-speed takes slated with fps; MOS noted.
- [ ] Exposure compensated for fps and shutter.
