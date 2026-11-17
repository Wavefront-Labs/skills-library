---
id: creative-arts.film-live-action.davinci-resolve.lut-management-and-writing-dctls
name: lut-management-and-writing-dctls
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, lut-folders, lut-management, lut-installation, dctl-writing, dctl-code, ofx-plugins, cube-lut, dctl, lut-browser]
level: practitioner
status: draft
description: "Manage LUTs in Resolve (folders, install paths, LUT browser, applying at node/clip/output) and write simple DCTLs, plus installing and managing OFX plugins."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - LUTs, DCTL, ResolveFX/OFX)"
  - "Blackmagic DCTL developer documentation (DaVinciCTL readme, shipped in the Resolve Developer folder)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LUT management and writing DCTLs

**Goal:** a tidy, shared LUT library that every suite resolves identically - and custom
colour math as DCTLs when no built-in tool fits.

## 1. Where LUTs live
- *Project Settings > Color Management > Lookup Tables > Open LUT Folder* reveals the
  LUT directory (system-wide on each OS, under the Resolve support folder, `LUT/`).
- Organise subfolders: `SHOW_NAME/`, `CAMERA_MFR/`, `CREATIVE/`, `TECHNICAL/`. Resolve
  shows the folder hierarchy in LUT menus.
- After copying files, click **Update Lists** (same settings page) - no restart needed.
- Formats: `.cube` (most common), `.3dl`, `.dat`, `.ilut/.olut`; 33-point cubes are a
  common sweet spot (65 for high precision).

## 2. Applying LUTs
- **Node LUT** (right-click node > LUT, or drag from the **LUT Browser** in the Color
  page): place the LUT in the right spot in the tree (usually after balance nodes for a
  creative LUT, or at the end as an output transform).
- **Clip/Media Pool** input LUT (right-click clips) - for camera conversions per clip.
- **Output/monitor LUTs** in Project Settings (Output, Video monitoring, Scopes) - display
  only or render-affecting depending on where.
- Share: for multi-suite/remote work keep an identical LUT folder (synced via shared storage
  or a script). Missing LUTs show an error on clips - fix before rendering.

## 3. DCTL basics
DCTL (DaVinci Color Transform Language) is a C-like language running on the GPU. A
simple **transform** DCTL:
```c
__DEVICE__ float3 transform(int p_Width, int p_Height, int p_X, int p_Y,
                            float p_R, float p_G, float p_B)
{
    const float gain = 1.1f;
    return make_float3(p_R * gain, p_G * gain, p_B * gain);
}
```
- Save as `MyGain.dctl` into the LUT folder; *Update Lists*; apply like a LUT or through
  the **DCTL** ResolveFX (which also exposes UI sliders defined with `DEFINE_UI_PARAMS`).
- Use for custom colour-space transforms, film-density models, false colour, utility
  checks. Validate on charts; compare against reference LUTs.
- **Encrypted DCTL** (`.dctle`) for distributing without source.

## 4. OFX plugins
Third-party OFX (Dehancer, FilmConvert, Sapphire, Neat Video): install with the vendor
installer into the system OFX folder; they appear in the Effects library. Manage licences
per machine; render nodes and remote suites need the same plugins/versions.

## Gotchas
- Different LUT folder contents between suites - renders differ.
- Applying a camera LUT twice (clip input + node).
- DCTL syntax errors silently failing - check the node shows the DCTL loaded.
- OFX missing on the render machine.

## Verify
- [ ] LUT folders organised and synced across suites; lists updated.
- [ ] Each LUT applied once at the intended point.
- [ ] DCTLs tested on charts; distribution format decided.
- [ ] OFX and licences identical on all machines.
