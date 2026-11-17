---
id: creative-arts.film-live-action.cinematography.green-screen-and-vfx-plate-photography
name: green-screen-and-vfx-plate-photography
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, dp, director-of-photography, vfx-supervisor, green-screen, greenscreen, blue-screen, bluescreen, chroma-key, keying, spill, spill-suppression, vfx-plates, plates, plate-photography, clean-plate, background-plate, tracking-markers, tracking, matchmove, hdri, chrome-ball, grey-ball, macbeth-chart, colour-chart, lens-grids, distortion-grid, camera-data, lens-data, focus-distance, sensor-height, nodal, motion-control, set-survey, lidar, witness-camera, frame-rate-for-vfx, shutter-for-vfx, 4444, raw-for-vfx, led-volume, virtual-production, lighting-green-screen, screen-evenness, green-screen-exposure, spill-control-on-set, screen-distance, spill-suppression-lighting, marker-placement, marker-spacing, set-survey-vfx, hdri-capture, chrome-ball-reference, vfx-reference, clean-plate-shooting, element-plates, plate-list, led-volume-shooting, virtual-production-camera, frustum, vfx-data-sheet, lens-data-for-vfx, camera-metadata-vfx]
level: practitioner
status: draft
description: "Shoot for VFX: even screen 1-2 stops under key, separation and spill control, tracking markers, clean plates, HDRI and chrome/grey balls, lens grids, and the per-shot camera data VFX needs."
sources:
  - "American Cinematographer Manual, 10th ed. - Visual effects photography; Greenscreen and bluescreen"
  - "https://www.vfxv.org/ (Visual Effects Society - VES Handbook of Visual Effects, on-set data chapters)"
  - "https://www.netflixstudios.com/ (Netflix VFX on-set data capture best practices)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Green screen and VFX plate photography

**Goal:** footage that keys in one pass, tracks without fighting, and comps with the
right light - because every corner cut on set costs ten times more in a VFX bid.

## 1. Choose the screen
- **Green** for most digital work (sensor green channel is cleanest, least noise), **blue**
  when the subject wears green, for night/dark scenes (less spill luminance), or for
  blond/fine hair in some pipelines. Ask the VFX supervisor.
- Material: painted cyc (Rosco Digicomp/ Chroma Key paint) or fabric; keep it matte,
  wrinkle-free, and large enough with margin for the frame and any camera move.
- Only cover what the shot needs; a full-stage green when a 12x12 behind a window would
  do adds spill and cost.

## 2. Light the screen, then the subject - separately
- **Screen**: even, soft, ~1-2 stops **under** the subject's key (not "as bright as
  possible"). Use tubes/space lights/Skypanels in green (or white) from both sides;
  check with false colour or a waveform: the screen should be a flat band, within ±1/3
  stop across the keyed area. Even is more important than bright.
- **Subject** 3-6 m from the screen; flags between screen lights and subject; a slight
  **backlight/rim** (warm or magenta-ish to counter green spill) to separate hair.
- **Spill**: negative fill (black) on the floor and sides; keep the subject's key off the
  screen; a minus-green on the rim if needed. Hair, motion blur and reflective props are
  where spill lives.
- Match the final environment: if the comp is a sunset exterior, light the subject with a
  low warm hard key and sky-blue fill now. "Fix it in comp" lighting is the second most
  expensive sentence on a set.

## 3. Camera settings for keying
- **4:4:4 or RAW** (ProRes 4444/XQ, ARRIRAW, R3D, BRAW) - 4:2:2 loses chroma edges.
- Lowest noise: base ISO, no high-EI. No or minimal diffusion filters. Sharp focus on the
  edge you need to key.
- Shutter 180° for normal motion blur (VFX can add blur, can't remove it cleanly). Frame
  rate per delivery; if plates must retime, agree it.
- No in-camera sharpening; log, as always.

## 4. Tracking and plates
- **Tracking markers** on the screen when the camera moves: small X's or dots in tape,
  a contrasting shade of the screen colour (darker green on green), spaced evenly,
  *not* behind hair/edges, and a few at known measured distances. Static lock-off shots
  don't need them.
- **Clean plates**: the same shot without actors, same lens/exposure/move. Always, for
  every setup with a moving camera and most lock-offs - costs a minute.
- **Background plates** for live-action backgrounds: shoot the real environment with the
  intended lens, height, tilt and exposure; a locked tripod or motion control for moves;
  also shoot wider than needed for reposition.
- **Reference**: after each setup, a **chrome ball + grey ball** (and a Macbeth chart) in
  the subject position, turned to camera, for lighting direction and colour; **HDRI**
  (bracketed 360 panorama from the subject position) for CG lighting; stills of the set.
- **Lens grids** (distortion chart) shot once per lens/focal length/focus distance on the
  show camera; VFX undistorts with them.

## 5. Camera data (write it down per shot)
Camera body, sensor mode, resolution, codec, lens make and focal length, **T-stop, focus
distance**, filters, **lens height** and tilt, distance to subject and to screen, frame
rate, shutter, white balance, LUT. Plus a set survey (tape measures or LiDAR) and
witness-camera reference where there's interaction. Most of this comes from the VFX
data wrangler; the camera department enables it.

## 6. LED volumes (virtual production)
Different rules: the wall is the key and the background; exposure to the wall's content
brightness; moiré from pixel pitch vs focal length/distance (test); colour calibration
between wall and camera; frustum tracking needs the camera tracked. Plan with the volume's
engineers; it's not a green screen with pictures.

## Gotchas
- Screen hotter than the subject -> spill and fringing on hair.
- Markers behind an actor's head.
- Forgetting the clean plate after the last take of the setup.
- 4:2:2 ProRes for a hair key.
- Lens changed mid-setup without recording the focal length and distance.

## Verify
- [ ] Screen flat within ±1/3 stop on waveform, 1-2 stops under key; subject 3+ m away.
- [ ] Rim/negative fill in place; spill checked on the monitor at 100% zoom on hair.
- [ ] Clean plate, chrome/grey ball, chart and HDRI captured per setup.
- [ ] Lens grids shot; per-shot camera data sheet filled.
