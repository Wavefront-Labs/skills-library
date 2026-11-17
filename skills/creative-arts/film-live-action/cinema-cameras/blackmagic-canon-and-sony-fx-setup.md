---
id: creative-arts.film-live-action.cinema-cameras.blackmagic-canon-and-sony-fx-setup
name: blackmagic-canon-and-sony-fx-setup
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, blackmagic-setup, braw-settings, ursa-menus, canon-setup, canon-menus, canon-raw, fx-setup, sony-menus, cinema-raw-light, s-cinetone, constant-quality-braw]
level: practitioner
status: draft
description: "Set up Blackmagic (BRAW), Canon Cinema EOS (Cinema RAW Light/XF-AVC) and Sony FX cameras: codecs and quality, log/gamut, base ISO, LUTs, timecode and the menu traps."
sources:
  - "https://www.blackmagicdesign.com/support (Blackmagic URSA Cine / Pocket Cinema Camera manuals)"
  - "https://www.usa.canon.com/support (Canon EOS C70/C300 Mark III/C500 Mark II instruction manuals)"
  - "https://pro.sony/ue_US/products/cinema-line-cameras (Sony FX3/FX6/FX9 help guides)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blackmagic, Canon and Sony FX setup

**Goal:** these widely-used indie and doc cameras configured to a pro pipeline - right
codec, log, base ISO and timecode - avoiding the defaults that trip up post.

## 1. Blackmagic (URSA Cine, URSA Mini Pro, Pocket 6K)
- **Blackmagic RAW**: **Constant Bitrate** (3:1, 5:1, 8:1, 12:1) or **Constant Quality**
  (Q0, Q1, Q3, Q5); Q0/3:1 for heavy VFX, 5:1/Q3 typical drama.
- ISO, white balance and look are **metadata** in BRAW (adjust in Resolve).
- **Gamut/gamma**: Blackmagic Design Film Gen 5 (or "Wide Gamut" on newer); monitoring
  LUT - built-in film-to-Extended Video or a custom 3D LUT (.cube) loaded via the LUT menu.
- Dual native ISO on many models (e.g. 400/3200 on Pocket 6K) - the camera switches
  automatically above a threshold.
- Media: CFast/SD/USB-C SSD; **project frame rate vs sensor frame rate** for off-speed.

## 2. Canon Cinema EOS (C70, C300 Mk III, C500 Mk II, C400)
- **Recording**: **Cinema RAW Light** (HQ/ST/LT) or **XF-AVC** (Intra/Long GOP) 10-bit
  4:2:2.
- **Custom Picture**: Canon Log 2 (more DR) or Canon Log 3 (easier, slightly less DR),
  Cinema Gamut; view assist / LUTs on outputs.
- **Dual Gain Output** sensors: base ISO 800 (and 3200 on some modes) - stay at the
  recommended ISO for maximum DR.
- Built-in ND (2/4/6/8/10 stops on C300 III/C500 II; C70 has ND too).
- Timecode in/out via BNC (or adapter on C70); set Rec Run/Free Run.

## 3. Sony FX (FX3, FX6, FX9)
- **Shooting mode**: **Cine EI** (log, base ISO 800 and high base 12800 on FX6/FX3 S-Log3)
  for fixed-exposure log workflows, or **Custom** mode (S-Cinetone or log with ISO
  changes).
- **Codec**: XAVC S-I (Intra) 4:2:2 10-bit or XAVC S (Long GOP); FX6/FX9 support RAW out
  to external recorders (ProRes RAW).
- FX6/FX9 electronic variable ND; FX3 needs external ND.
- Monitoring LUT: s709 or loaded 3D LUT; "MLUT" on outputs only.
- FX3 needs the XLR handle for timecode/audio inputs (or external timecode via adapter).

## 4. Common traps
- **File naming / reel IDs**: set camera ID and reel numbering so A and B cameras don't
  produce duplicate clip names.
- Long GOP codecs heavy for editing - transcode or plan proxies.
- Auto settings (AF, auto ISO, auto WB) left on for drama.
- Variable frame rate modes making non-standard rates.

## Verify
- [ ] Codec/quality and log/gamut chosen and identical across bodies.
- [ ] Base ISO set for maximum DR; ND plan.
- [ ] Monitoring LUT on outputs only; timecode and naming configured.
- [ ] Auto functions off; test footage through post.
