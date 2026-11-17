---
id: creative-arts.animation.editorial.reel-breaks-and-balancing
name: reel-breaks-and-balancing
category: creative-arts
field: animation
product: editorial
tags: [reel-breaks, reel-balancing, picture-lock, feature-editorial, conform, mix-reels, act-breaks, ad-breaks]
level: advanced
status: draft
description: "Split a feature or long special into reels at clean break points, balance reel lengths for mix and conform, and map broadcast act breaks for series."
sources:
  - https://www.routledge.com/Producing-Animation/Winder-Dowlatabadi-Miller-Zarneke/p/book/9781138479937
  - https://partnerhelp.netflixstudios.com/hc/en-us
  - https://www.focalpress.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reel breaks and reel balancing

**Goal:** a feature cut divided into reels (typically 5-7 reels of up to about 20 minutes, 2000 ft of 35 mm) that
departments can work on in parallel, and which join back seamlessly.

## Why reels still exist

Mix stages, conform, colour and QC all work reel by reel; a change in reel 3 is turned over as a reel 3 update
without touching the rest. Each reel gets its own timeline starting at hour timecode (reel 1 at 01:00:00:00, reel
2 at 02:00:00:00 ...) so a timecode identifies the reel instantly.

## Picking a break

- **Never** mid-dialogue, mid-music cue or on a continuous sound; music cues and ambience crossing a break are the
  classic mix headache.
- Best: a hard scene change with a silent or near-silent frame, a fade to black, or a cut where sound changes
  completely.
- Avoid a break inside a dissolve or a shot with sound prelapping across it.

## Balancing

- Keep reels within a few minutes of each other so the mix schedule has even days per reel.
- After every recut, check reel lengths; a recut that grows reel 2 by four minutes may mean moving a break, which
  ripples timecodes in every department. Move breaks rarely and announce them in a change list
  (see `creative-arts.animation.editorial.editorial-change-lists`).

## Series equivalent: act breaks

For broadcast series, map **act breaks** (ad insertion points) at story-mandated places, with black or a fade and
a clean audio out; streaming deliveries often still want act-break timecodes in metadata. Netflix and others
specify where commercial black is allowed; check the platform's spec.

## Joining reels

The final assembly (long play) joins reels with no gaps; verify sync across each join with a 2-pop/tail-pop check
(see `creative-arts.animation.editorial.leaders-and-two-pops`).

## Verify

The reel list (reel, start TC, end TC, duration, break description) is published with the lock, and the joined long
play has no dropped or repeated frames at any break.
