---
id: creative-arts.photography-fine-art.art-photography.colour-target-and-camera-profile
name: colour-target-and-camera-profile
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, color-temperature, color-checker, dcp-profile, camera-profile-creation, calibrite, art-reproduction, dng-profile-editor]
level: practitioner
status: draft
description: "Shoot a ColorChecker target and build a custom DCP/ICC camera profile for accurate colour in artwork copying and consistent multi-camera series."
sources: ["https://calibrite.com/us/product/colorchecker-classic/", "https://www.adobe.com/support/downloads/detail.jsp?ftpID=4671", "https://helpx.adobe.com/camera-raw/digital-negative.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Colour target and camera profile

## When
Copying artwork, product colour accuracy, matching two camera bodies in one series, odd light
sources (LED, gallery lighting).

## Capture
1. Light the target evenly (two lights at 45 deg for copy work); no glare (check family of angles).
2. Target fills about 1/4-1/3 of the frame, square to the sensor.
3. Expose so the white patch is around 240-245 RGB (not clipped), raw, base ISO.
4. One target frame per lighting setup and camera.

## Build the profile
- **Calibrite/X-Rite ColorChecker Camera Calibration** app: convert raw to DNG, drag in, it
  detects the chart and writes a DCP. Dual-illuminant profile from shots under tungsten and daylight.
- **Lightroom**: Calibrite plugin via File > Export with Preset; restart, choose the profile in the
  Profile browser.
- **Capture One**: use ICC profiles (e.g. from Lumariver, basICColor input or i1Profiler).
- **DNG Profile Editor** (legacy, Adobe) for manual hue tweaks.

## Apply
Set WB with the eyedropper on the second-lightest grey patch, apply the custom profile, sync to the set.

## Gotchas
- Profile is for the light it was shot in; a new light = new profile.
- Target ages: replace roughly every few years (fading/yellowing), keep it in its sleeve.

## Verify
- [ ] Patch values in the processed target match the reference (delta E low; neutral patches neutral).
