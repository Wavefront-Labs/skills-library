---
id: creative-arts.film-live-action.cinematography.high-speed-cinematography
name: high-speed-cinematography
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, high-speed-cameras, phantom, lighting-for-high-speed, slow-motion, ramping, trigger-modes, flicker-free-lighting, overcranking]
level: practitioner
status: draft
description: "Shoot high-speed slow motion: camera choice (Phantom, high-fps modes), exposure loss and light quantities, flicker-free sources, triggering and buffer modes, and data handling."
sources:
  - "https://www.phantomhighspeed.com (Vision Research Phantom - Flex4K, VEO4K documentation)"
  - "American Cinematographer Manual (ASC, 11th ed.) - high-speed photography"
  - "Harry C. Box, Set Lighting Technician's Handbook (flicker-free lighting)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# High-speed cinematography

**Goal:** clean, flicker-free slow motion at the needed frame rate, with enough light
and a capture workflow that doesn't lose the moment.

## 1. Camera choice
- **Cinema cameras' high-fps modes**: ARRI Alexa 35 (up to ~120 fps), RED V-Raptor
  (up to ~120 fps 8K, higher at reduced resolution), Sony Venice 2 (up to ~120 fps):
  fine for 2-5x slow motion.
- **Dedicated high-speed**: Phantom Flex4K (~1000 fps at 4K), Phantom VEO/TMX (thousands
  fps at lower resolutions); Freefly Ember/Wave for budget high speed.
- Check resolution and sensor crop at each frame rate.

## 2. Exposure and light
Every doubling of frame rate (with same shutter angle) loses one stop. At 1000 fps vs 25
fps that's ~5.3 stops. Plan:
- Big sources: HMIs on flicker-free ballasts, high-output LEDs with high PWM frequency,
  tungsten (inherently flicker-free due to filament inertia - the classic choice for very
  high speed).
- Faster lenses, higher EI within the camera's noise tolerance, narrower shutter only if
  needed for crispness.

## 3. Flicker
AC-powered discharge and LED sources flicker at mains-related rates (100/120 Hz) or PWM
frequencies. At high speed, it becomes visible pulsing. Use tungsten, flicker-free HMI
ballasts in flicker-free mode, or LEDs rated for high-speed (check manufacturer specs at
your fps). Test every source at the shooting frame rate.

## 4. Triggering (Phantom-style cameras)
The camera records continuously into a RAM **buffer** (cine); the **trigger** marks the
event. **Pre-trigger/post-trigger** settings decide how much before/after the trigger is
kept (e.g. 80% pre for an unpredictable event - trigger after it happens). Then **save**
the cine to media (CineMag/ CFast) - takes time; plan resets.

## 5. Data and workflow
Huge data volumes; trim cines to the useful range before saving. Record metadata (fps,
shutter, trigger). Playback speed set to the project frame rate in post.

## Gotchas
- LED flicker discovered in dailies.
- Not enough light: noisy slow motion.
- Trigger mode wrong; the event lost.
- Saving untrimmed cines and running out of media/time.

## Verify
- [ ] Camera and resolution confirmed at the target frame rate.
- [ ] Light budget calculated for stop loss; flicker-free sources tested at fps.
- [ ] Trigger/buffer settings set for the event.
- [ ] Cines trimmed and saved; metadata logged.
