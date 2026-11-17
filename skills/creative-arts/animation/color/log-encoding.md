---
id: creative-arts.animation.color.log-encoding
name: log-encoding
category: creative-arts
field: animation
product: color
tags: [log-encoding, scene-linear, linear-workflow, acescct, acescc, logc, cineon, grading-space, log-to-lin, ocio]
level: advanced
status: draft
description: "When and how to move CG renders into log encodings (ACEScct, LogC, Cineon) for grading or interchange, and back, without clipping or shifting colour."
sources:
  - https://opencolorio.readthedocs.io/en/latest/
  - https://www.arri.com/en/learn-help/learn-help-camera-system/image-science/log-c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log encoding

**Goal:** use a log curve where it helps (grading controls that behave like film exposure,
compact 10/12-bit interchange) without losing the linear data's range or colour.

## Why log for grading

In linear, an offset of +0.01 is huge in shadows and invisible in highlights. In log, equal code
steps are equal exposure stops, so lift/offset/printer-light controls feel even across the range.
That is why ACES specifies ACEScct as the grading space and Resolve's colour-managed ACES projects
grade in it.

## Common log spaces

| Space | Use |
|---|---|
| ACEScct | ACES grading; linear toe so shadows grade like video lift |
| ACEScc | pure log; awkward shadow behaviour, mostly replaced by ACEScct |
| ARRI LogC3/LogC4 | camera footage; sometimes used as a show's log interchange |
| Cineon/ADX | legacy film scans |

## Moving CG into a log grade

Resolve, ACES managed: set the timeline space to ACEScct and the input transform of EXRs to
ACEScg (the render's working space). Resolve converts automatically.

Manually with OCIO (e.g. making a log DPX/ProRes for a grading facility):
```bash
oiiotool shot.%04d.exr --colorconvert ACEScg ACEScct -d uint16 -o shot_cct.%04d.tif
```
Log 10-bit or 12-bit holds the full scene range; linear values above 1.0 map below log 1.0.
Check the curve's ceiling (ACEScct encodes up to about 65504 linear; LogC about 55).

## Back to linear

The grade outputs either display-referred (through the ODT) or, for VFX round trips, linear via
the inverse log. Apply exactly the inverse; mixing ACEScc with ACEScct gives a shadow shift.

## Gotchas

- Viewing log images without a transform looks flat and grey; that is correct, not a problem.
- Do not composite (blur, merge, defocus) in log: edges and glows go wrong. Comp in linear.
- Label log files clearly in name and metadata; an untagged log file will be mistaken for video.

## Verify

Round trip: linear EXR to ACEScct 16-bit TIFF and back; difference against the original is
below 1e-3 for values in 0-16 and highlights above 1.0 survive.
