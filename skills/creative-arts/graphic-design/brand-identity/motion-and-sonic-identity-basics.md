---
id: creative-arts.graphic-design.brand-identity.motion-and-sonic-identity-basics
name: motion-and-sonic-identity-basics
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, identity-system, motion-identity, sonic-identity, logo-animation, easing, motion-principles, audio-logo, lottie, after-effects]
level: practitioner
status: draft
description: "Define a motion and sonic identity: logo animation, easing and timing principles, transitions, a sonic logo brief, and delivery formats like Lottie, MP4 and WAV."
sources:
  - https://m3.material.io/styles/motion/overview
  - https://airbnb.io/lottie/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Motion and sonic identity basics

**Goal:** a brand that moves and sounds consistently across video, app, social and events, because more
brand impressions are now animated than printed.

## Motion principles
- Derive motion from brand attributes: "precise" = short, linear-ease-out moves, no bounce; "playful" =
  overshoot and springy easing.
- Specify: **durations** (e.g. 150 ms small UI, 300 ms panels, 600-1000 ms brand moments), **easing curves**
  (cubic-bezier values, e.g. `cubic-bezier(0.2, 0, 0, 1)`), directions, and choreography (stagger 30-50 ms).
- Respect `prefers-reduced-motion`: provide reduced alternatives (fades instead of moves).

## Logo animation
- 2-4 second reveal for video ends and app launch; a short 1 s version for social; a loop if needed.
- Build from the logo's construction (lines drawing, shapes assembling), ending on the static logo exactly.
- Deliver: After Effects project, MP4 (H.264) on white and dark, transparent ProRes 4444 or WebM with alpha,
  and **Lottie JSON** (via Bodymovin) for apps and web.

## Transitions and kinetic type
- Rules for how text appears (line by line, words), how brand devices wipe or frame, and caption styling.
- Templates in After Effects or Premiere (Motion Graphics templates .mogrt) for in-house editors.

## Sonic identity
- **Sonic logo (audio mnemonic):** 1-3 seconds, recognisable melody or sound; brief a sound designer with
  brand attributes, references, and uses (app open, ad end, phone hold).
- Extended palette: notification sounds, hold music, event stings in the same instrumentation and key.
- Deliver WAV 48 kHz 24-bit masters plus compressed MP3/AAC; loudness for broadcast (e.g. -23 LUFS EBU R128).

## Gotchas
- Motion done separately by many vendors drifts; publish the motion guide with example files.
- Lottie supports only part of After Effects features (no some effects or expressions); test early.
- Sound must be licensed or owned outright; check composer agreements for full buyout.

## Verify
- [ ] Motion spec with durations and easing values; animated logo files in all formats.
- [ ] Sonic logo delivered with usage rules and loudness-normalised masters.
