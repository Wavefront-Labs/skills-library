---
id: creative-arts.animation.blender.display-device-hdr
name: display-device-hdr
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, display-device, hdr-display, display-p3, rec2020]
level: practitioner
status: docs-checked
description: "Set the Color Management display device: sRGB, Display P3, Rec.1886, Rec.2020 and HDR displays on recent versions, and match monitor, viewer and delivery."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
  - https://docs.blender.org/manual/en/latest/render/color_management/system_configuration.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# display-device-hdr

Goal: what you see on screen matches what the audience sees.

## Render Properties > Color Management > Display

Per the manual, the display is the colour space of the display that images and video are being created for.
- SDR: **sRGB** (basic, supported everywhere), **Display P3** (wide gamut for Apple and other modern displays), **Rec.1886** (many older TVs), **Rec.2020** (wider gamut than P3).
- HDR: **Rec.2100 PQ** (Rec.2020 gamut, up to 10000 nits) and **Rec.2100 HLG** (HDR TVs, up to 1000 nits). Separate views exist for 500, 1000, 2000 and 4000 nits.
- Wide gamut works best with the ACEScg or Linear Rec.2020 working space.

## Display emulation (System Configuration)

- **Automatic**: previews how the image will look when saved for the chosen display; colours are clipped to that display's gamut and HDR range. Blender integrates with operating-system colour management and saves colour space metadata.
- **Off**: outputs what OpenColorIO produces; the chosen display must match the system and monitor, otherwise results are inaccurate.
- Emulation is not supported with older OpenColorIO configurations.

## Enabling wide gamut and HDR

A capable monitor is required. macOS: any Apple Silicon device. Linux: Wayland with the Vulkan backend. Windows: enable "Automatically manage color for apps" for wide gamut and "Use HDR" for HDR, plus the Vulkan backend.

## Saving

- Wide-gamut images can be written as PNG, JPEG, WebP, AVIF, TIFF and JPEG 2000; HDR images as AVIF or PNG (203 nits diffuse white).
- HDR video: display Rec.2100 PQ or HLG, codec H.265 or AV1, bit depth 10 or 12; written with 100 nits diffuse white. The manual suggests 10-bit PQ as the most compatible default.
- Blender does not currently apply automatic HDR tone mapping; it clips colours beyond the display. 100 nits is reference white, so a 1000-nit view needs 10x headroom (lower the display brightness to gain headroom).

## Gotchas

- Agree on one display setting in the shot template when a team mixes monitors.
- On Windows and Linux monitors may map sRGB to their wider gamut by default, making colours more vibrant; enabling OS colour management or a good display profile corrects it.

## Verify

Preview with Display Emulation set to Automatic while switching the display between sRGB and Display P3, then check the saved files on the target device.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/color_management/displays_views (Displays: SDR and HDR lists, wide gamut and HDR notes, Save as Render formats, HDR video requirements) and system_configuration (display emulation, enabling wide gamut/HDR per OS, reference white 100 nits, no automatic HDR tone mapping). Replaced the unconfirmed ICC statement and delivery table.
Method: documentation only; no commands were run.
