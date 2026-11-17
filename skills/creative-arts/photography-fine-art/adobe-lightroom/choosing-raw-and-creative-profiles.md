---
id: creative-arts.photography-fine-art.adobe-lightroom.choosing-raw-and-creative-profiles
name: choosing-raw-and-creative-profiles
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, raw-profile-choice, lightroom-develop, camera-profile, creative-profiles, dcp-profile, lightroom-classic]
level: practitioner
status: draft
description: "Choose a Lightroom Classic raw profile (Adobe Color, Neutral, Camera Matching, custom DCP) and use creative profiles with the Amount slider as a starting look."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Adjust image tone and color; Profiles)", "https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/apply-presets.html", "https://helpx.adobe.com/photoshop/digital-negative.html (DNG Profile Editor)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing raw and creative profiles

The profile is the first interpretation of raw data: it sets the base tone curve and colour rendering that every slider then acts on. Choose it **first**.

## Raw profiles (Basic panel > Profile, or the Profile Browser grid icon)
- **Adobe Color**: default, moderate contrast, good general start.
- **Adobe Neutral**: low contrast, flat; best for high-dynamic-range scenes and for building your own curve.
- **Adobe Standard**: older default, used by many presets built before 2018.
- **Adobe Landscape / Portrait / Vivid / Monochrome**: style variants; Monochrome is a better B&W base than desaturating.
- **Camera Matching** (Camera Standard, Camera Faithful, Camera Flat, etc.): emulate the in-camera JPEG look. Use when clients approved the back-of-camera look.
- **Custom DCP** from a colour target (Calibrite/X-Rite ColorChecker Camera Calibration software or DNG Profile Editor) for reproduction-accurate colour; install to the CameraProfiles folder and restart.

## Creative profiles (Artistic, B&W, Modern, Vintage)
- Apply a look via a 3D LUT on top of the current settings without moving sliders. The **Amount** slider (0-200) scales the effect.
- They work on raw and rendered files; raw profiles appear only for raw.

## Workflow
1. Hover over profiles in the browser to preview; star favourites so they appear in the dropdown.
2. For a series, use the same profile on every frame; mixing profiles is a common cause of inconsistent colour.
3. Set the profile in an import develop preset so new files start on it.

## Gotchas
- Changing the profile after editing shifts every adjustment; re-check whites/blacks.
- Monochrome profiles enable the B&W mix sliders; switching back to a colour profile restores colour.

## Verify
- [ ] Every image in a sequence shows the same profile name in the Basic panel.
