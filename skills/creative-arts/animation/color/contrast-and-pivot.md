---
id: creative-arts.animation.color.contrast-and-pivot
name: contrast-and-pivot
category: creative-arts
field: animation
product: color
tags: [contrast-pivot, contrast, pivot, primary-grading, s-curve, resolve, acescct, log-grading, mid-grey]
level: practitioner
status: draft
description: "Set grade contrast with the contrast and pivot controls in a log space: choose the pivot at mid-grey, avoid hue shifts and clipping, and compare with curves."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://docs.acescentral.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contrast and pivot

**Goal:** expand or reduce tonal contrast around a chosen grey point so the image gains punch without moving its
overall exposure.

## How it works

Contrast scales values away from (or toward) the **pivot**: values above the pivot get brighter, below get darker,
the pivot itself does not move. In a log space (ACEScct) this behaves like changing film gamma, which is why
colourists grade contrast in log.

- **Resolve Primaries:** *Contrast* (1.0 neutral) and *Pivot* (default 0.435 in Resolve's log-style default, which
  is near ACEScct mid-grey 0.4135 for 18% grey). Set pivot to the subject's key tone, often the face or the
  character's main colour value.
- ACEScct 18% grey is 0.4135; use that as the default pivot when grading ACEScct.

## Workflow

1. Balance exposure first (Offset), then contrast.
2. Raise contrast in small steps (1.05-1.2 for most shots); watch the waveform so highlights do not clip and shadows
   do not crush (see `creative-arts.animation.color.video-scopes-waveform`).
3. Use **Shadow/Highlight** or a soft-clip curve to roll off the ends instead of hard clipping.
4. Check saturation: contrast in RGB increases saturation. Resolve's *Luminance Mix* and *Sat* controls compensate;
   or apply contrast on luminance only (a Lum-only curve or YRGB Y-only mode).

## Contrast vs curves

Contrast+pivot is a straight-line (in log) S-curve with two numbers, easy to copy between shots and to match.
Custom curves give shaped toe/shoulder but are harder to match numerically; use them on a later node for style.

## Stylized note

Cel-shaded renders have few tonal steps; heavy contrast can merge the shadow tone with the line colour. Check the
shadow band separation against the colour model (`creative-arts.animation.art-direction.master-palette-specification`).

## Verify

Toggle the contrast node: the pivot-tone patch value is unchanged, highlights stay below the legal/peak line and
the darkest important detail stays above black.
