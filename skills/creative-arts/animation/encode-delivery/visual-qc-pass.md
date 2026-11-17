---
id: creative-arts.animation.encode-delivery.visual-qc-pass
name: visual-qc-pass
category: creative-arts
field: animation
product: encode-delivery
tags: [visual-qc, encode-quality, qc-report, full-qc, spot-check, timecode-notes, deliverable-qc, broadcast-qc, viewing-conditions]
level: practitioner
status: draft
description: "Run a real-time visual and aural QC pass on a deliverable: viewing setup, what to watch for in animation, logging faults by timecode with severity, sign-off."
sources:
  - https://partnerhelp.netflixstudios.com/hc/en-us
  - https://tech.ebu.ch/publications/r103
  - https://www.thedpp.com/tech/as-11-dpp
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visual QC pass

**Goal:** a human watches the exact deliverable file, start to finish, in proper conditions,
and logs every fault by timecode so it can be fixed or waived. Automated QC
(`creative-arts.animation.encode-delivery.automated-file-qc`) runs first; this pass catches what
machines cannot.

## Setup

- Play the delivery file itself (not the timeline) through a calibrated reference display or a
  calibrated monitor via a clean video output, at 100% scale.
- Audio on decent near-field speakers or closed headphones at a known level; a second pass on
  small speakers for dialogue intelligibility.
- Dim room, no other picture in view. Timecode visible on a separate monitor or player overlay.
- Full QC = every frame in real time. Spot QC = head, tail, each act break, a sample of
  shots: only for re-deliveries where the change is known.

## What to watch for in animation

| Picture | Sound |
|---|---|
| wrong shot version, missing FX/element | missing line, wrong take, clipped word |
| render glitches: flicker, fireflies, popping geometry, intersection | sync drift, lip-sync miss |
| line boil or missing ink lines, paint fill holes | clicks, pops, digital distortion |
| banding, macroblocking, aliasing on line art | level jumps between shots, dropouts |
| text spelling, credits, burned-in text in a textless master | M&E missing effects that were on dialogue track |
| black or frozen frames not in the edit | channel errors (dialogue in surrounds) |

## Logging

One row per fault: `TC in | TC out | category | description | severity | action`.
Severity: **Fail** (must fix), **Warn** (fix if time, or needs client waiver), **Note**
(cosmetic, creative choice). Example:
`01:04:12:08 | 01:04:12:10 | picture | 3-frame texture flicker on door, shot 045 | Fail | re-render 045 v012`.

## Process

1. QC operator logs; production triages with the director/supervisor (creative "faults" may be
   intentional).
2. Fixes go into a new version; re-QC the fixed sections plus 10 s either side, and re-run
   automated QC on the whole file.
3. Sign-off records file name, checksum, QC date and operator.

## Verify

The report names the exact file (with checksum), has no open Fail items, and every Warn is fixed
or has a recorded waiver.
