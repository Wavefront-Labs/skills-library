---
id: creative-arts.film-live-action.cinematography.flicker-free-shooting-and-screens-in-shot
name: flicker-free-shooting-and-screens-in-shot
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, flicker-free, mains-flicker, flicker-calculator, shooting-screens, monitor-flicker, screen-sync, shutter-angle-flicker, 50hz-60hz, screen-replacement, led-walls]
level: practitioner
status: draft
description: "Avoid flicker from mains lighting, LEDs and screens: safe frame rate and shutter combinations for 50/60 Hz, flicker calculators, and shooting TVs, monitors and phones in shot."
sources:
  - "https://www.arri.com/en/learn-help (ARRI - flicker-free frame rates and shutter angles / ARRI Photometrics and Frame Rate tools)"
  - "American Cinematographer Manual (ASC, 11th ed.) - flicker and HMI frame rates"
  - "https://www.cinematography.net (CML - Cinematography Mailing List discussions of screen sync)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flicker-free shooting and screens in shot

**Goal:** no pulsing lights or rolling bars - by choosing safe frame-rate and shutter
combinations and handling screens properly.

## 1. Why flicker happens
Discharge lamps (fluorescent, HMI on magnetic ballasts, sodium, some LEDs) pulse at
**twice mains frequency**: 100 Hz in 50 Hz countries (UK/EU), 120 Hz in 60 Hz countries
(US). If each exposure doesn't capture a whole number of pulses, brightness varies
frame to frame.

## 2. Safe combinations
The exposure time should be a whole multiple of the pulse period (1/100 s or 1/120 s):
- 50 Hz mains: **1/50 s** or **1/100 s** exposure. At 25 fps -> 180 degree (1/50) is safe.
  At 24 fps in a 50 Hz country, 180 degree = 1/48 s - **not safe**; use **172.8 degree**
  (= 1/50 s).
- 60 Hz mains: **1/60 s** or **1/120 s**. At 24 fps, 180 degree (1/48) works in
  practice because 120/24 = 5 whole pulses per frame interval (each frame starts at the
  same phase) - but any mains frequency drift beats slowly, so 144 degree (1/60) is the
  fully safe setting; at 30 fps 180 degree (1/60) is safe.
- The general rule: safe if the exposure time is a whole number of pulse periods, or the
  pulse rate divided by the frame rate is a whole number (phase repeats) on stable power.
Use a **flicker calculator** (ARRI Frame Rate Calculator, Cine Meter app, pCAM) for
off-speed and unusual combinations. Cameras with shutter in degrees can enter 172.8.
Tungsten is effectively flicker-free.

## 3. LEDs and practicals
LED drivers use PWM at varying frequencies; some flicker at certain shutter settings
or dimming levels. Test the actual fixture and dimming level at your frame rate and
shutter on a monitor; look for banding on the waveform. Replace bad practicals with
film-grade LED bulbs or tungsten.

## 4. Screens in shot (TVs, monitors, phones, LED walls)
- **Rolling bars/banding** come from the screen's refresh rate vs the camera's shutter.
  Set the camera shutter to match the refresh (e.g. 1/60 for 60 Hz screens) or set the
  screen's refresh to match the frame rate when possible.
- **Playback/screen replacement**: video playback operators feed content at the right
  frame rate/sync, or screens are left blank/green for VFX replacement (with tracking
  markers if moving).
- **Moire** on screens: defocus slightly, change angle or distance.
- **Exposure**: screens are bright; dim them to sit 1-2 stops over key, add ND film if needed.
- LED volumes/walls need genlock between the wall processor and the camera.

## Gotchas
- 24 fps 180 degree in a 50 Hz country with fluorescents - visible flicker.
- Testing at one dimming level, shooting at another.
- Phone screens set to auto-brightness changing between takes.
- Moire discovered in the edit.

## Verify
- [ ] Mains frequency known; shutter set to a safe value (e.g. 172.8 degree at 24 fps / 50 Hz).
- [ ] All LEDs/practicals tested at shooting fps, shutter and dimming level.
- [ ] Screens matched to camera or planned for replacement; brightness controlled.
- [ ] Flicker calculator used for off-speed shots.
