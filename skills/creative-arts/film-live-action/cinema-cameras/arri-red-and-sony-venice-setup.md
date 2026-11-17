---
id: creative-arts.film-live-action.cinema-cameras.arri-red-and-sony-venice-setup
name: arri-red-and-sony-venice-setup
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, arri-setup, alexa-menus, arri-recording, red-setup, redcode-settings, red-menus, venice-setup, sony-menus, arriraw, redcode, x-ocn, ei, sensor-modes]
level: practitioner
status: draft
description: "Set up ARRI Alexa, RED and Sony Venice cameras on prep day: sensor modes, codecs (ARRIRAW/ProRes, REDCODE quality, X-OCN), EI, look files, monitoring and timecode."
sources:
  - "https://www.arri.com/en/learn-help (ARRI ALEXA 35 / Mini LF user manuals)"
  - "https://docs.red.com (RED V-RAPTOR / KOMODO operation guides)"
  - "https://pro.sony/ue_US/products/digital-cinema-cameras/venice2 (Sony VENICE 2 operation manual)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ARRI, RED and Sony Venice setup

**Goal:** each camera configured in prep to the agreed pipeline - same rate, format,
look and timecode on every body - with the menus you'll need on set at your fingertips.

Common checklist for any body: project frame rate, sensor mode/resolution, codec and
quality, EI and white balance, shutter, look/LUT for monitoring (and whether it's baked or
metadata only), frame lines, timecode source and rate, reel/clip naming, audio inputs.

## 1. ARRI Alexa (35, Mini LF)
- **Sensor modes** (Alexa 35: 4.6K 3:2 open gate, 4K 16:9, 3.3K, 2K etc.; Mini LF: LF open
  gate, LF 16:9, S35 crop) - each sets the image circle needed.
- **Codecs**: ARRIRAW (.ari/.mxf) or ProRes (422 HQ, 4444, 4444 XQ - license may be
  needed). Recording media: Codex Compact Drives.
- **EI**: base 800 on many models; Alexa 35 has Enhanced Sensitivity modes at high EI.
- **Looks**: ARRI Look Files (ALF4 on Alexa 35 with Textures; ARRI Reveal colour science);
  monitoring output LUT per SDI/EVF; "Record with look" only for ProRes when baking.
- **Frame lines** created in ARRI Frame Line Composer and loaded via media.
- Menus via the home screen; **User buttons** for EI/WB/shutter shortcuts.

## 2. RED (V-Raptor, Komodo)
- **Format/resolution** (8K VV, 6K S35 crop, etc.) and **REDCODE RAW quality**: HQ, MQ,
  LQ (R3D) - HQ for VFX/heavy grading, MQ common for drama, LQ for long-form/doc.
- **ISO/EI**, **Kelvin**, **tint** are metadata; IPP2 output transform and creative 3D LUTs
  for monitoring; set **image pipeline** to IPP2.
- Projects frame rate vs **sensor frame rate** (for over/undercranking).
- Media: CFexpress (V-Raptor), CFast (Komodo). Use RED Control app for setup over Wi-Fi.
- Sensor **calibration** (black shading) per RED docs.

## 3. Sony Venice / Venice 2
- **Imager mode**: 8.6K/6K full frame, S35 crop, anamorphic modes.
- **Recording**: **X-OCN** (ST, LT, XT quality - Sony's compressed RAW) to AXS cards via
  the AXS-R7 or internal on Venice 2, or XAVC/ProRes.
- **Base ISO** dual: 800 and 3200 (Venice 2 8K) - switch with the Base ISO setting;
  **EI** on top.
- Internal **ND** filters 0.3-2.4 in 1-stop steps.
- **Look**: S-Log3/S-Gamut3.Cine with s709 or a custom 3D LUT for monitoring.
- Menus via the side panel and the full menu; **Assignable buttons**.

## 4. Make it repeatable
Save each camera's setup file (see maintenance skill); photograph key menu pages; send
format and naming to the DIT and post for their sign-off. Shoot a **test day** with the
full pipeline: through dailies to the editor's timeline.

## Gotchas
- One body in a different sensor mode (different crop) - mismatched coverage.
- Baked look on ProRes when post expected log.
- RED project rate and sensor rate confused.
- Venice base ISO left at 3200 for a day exterior - noisier highlights handling.

## Verify
- [ ] Sensor mode, codec/quality, rate and EI set identically across bodies.
- [ ] Monitoring LUT/look loaded; baked vs metadata agreed with post.
- [ ] Frame lines, timecode and naming configured.
- [ ] Test day through the full pipeline signed off.
