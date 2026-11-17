---
id: creative-arts.animation.color.printer-lights-offset-grading
name: printer-lights-offset-grading
category: creative-arts
field: animation
product: color
tags: [printer-lights, offset, log-grading, acescct, primary-grading, resolve, exposure-balance, colour-grading]
level: advanced
status: draft
description: "Balance shots with printer-light style offset grading in a log space (ACEScct): what a printer point is, why offset in log equals exposure, and Resolve controls."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://docs.acescentral.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Printer lights and offset grading in log

**Goal:** make exposure and colour-balance corrections that behave like changing light on the scene, by adding
offsets in a logarithmic working space.

## Why offset in log is exposure

In a log encoding, multiplying linear light by k becomes adding log(k). So an Offset (add) of the same amount to R,
G and B in ACEScct is a pure exposure change; offsetting one channel is a colour-temperature-like filter change.
This is how film printing worked: printer lights changed red/green/blue printing light in fixed steps.

**Printer point:** traditionally 0.025 log exposure, so 12 points is one stop. In ACEScct one stop is
1/17.52 = 0.057 code values in the log segment, so one printer point is about 0.0048.

## In Resolve

- Set timeline colour space and grade in ACEScct (Project Settings > Color Management, ACEScct, or a
  Colour Space Transform node pair); Offset only behaves as exposure in log.
- **Offset wheel / Offset values** in Primaries: master offset for exposure, the wheel for balance.
- **Printer lights:** Resolve maps keyboard shortcuts (with *Color > Printer Lights* or the numeric keypad on a
  supported layout) to step R/G/B/master offsets; the step size is set in Project Settings > Color (printer light
  calibration). Colourists use these for repeatable, numbered corrections ("up 2 red, down 1 blue").

## Workflow

1. First node: Offset for exposure/balance only, using the waveform and parade
   (see `creative-arts.animation.color.video-scopes-waveform`, `creative-arts.animation.color.rgb-parade-balancing`).
2. Only then contrast and look nodes (see `creative-arts.animation.color.grade-node-tree-structure`).
3. Write numbers in the shot notes; the same offset applied to a matching shot gives the same result.

## Animation note

CG renders are usually well exposed already; offset grading is mostly used for shot-to-shot matching where lighting
differed, and to push whole sequences warmer/cooler per the colour script
(`creative-arts.animation.art-direction.color-script`).

## Verify

Apply +12 points master offset in ACEScct: a mid-grey patch measures one stop brighter in linear (double the linear
value) through a colour picker set to scene-linear.
