---
id: creative-arts.animation.blender.custom-ocio-config
name: custom-ocio-config
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, ocio, custom-ocio-config, ocio-config, ocio-environment]
level: practitioner
status: docs-checked
description: "Use a custom OpenColorIO config in Blender via the OCIO environment variable: required roles, studio configs, checking it loaded, and keeping farm nodes consistent."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/opencolorio.html
  - https://docs.blender.org/api/current/bpy.types.ColorManagedViewSettings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# custom-ocio-config

Goal: run Blender with a studio OCIO config so it matches other tools in the pipeline.

## How Blender loads OCIO

- Blender ships a standard OpenColorIO configuration with its display devices and view transforms.
- Blender reads the standard **`OCIO`** environment variable to use another configuration. The manual recommends `OCIO` for compatibility with other software.
- **`BLENDER_OCIO`** changes the configuration for Blender only; use it when a config has incompatibilities that make sharing across applications difficult.

```bash
export OCIO=<PIPELINE_DIR>/ocio/studio-config/config.ocio
blender shot.blend
```
On Windows set the variable (`set OCIO=<PIPELINE_DIR>\ocio\config.ocio`) before launching, or use a launcher script.

## Roles Blender reads

`scene_linear` (rendering, compositing, all float images in memory), `data` (non-colour data), `aces_interchange` (ACES2065-1, used for blackbody chromaticities), `cie_xyz_d65_interchange` (intermediate display-linear space), `color_picking`, `default_sequencer` (falls back to scene_linear), `default_byte` (falls back to texture_paint), `default_float` (falls back to scene_linear).

## Writing configs for Blender

- Use OpenColorIO v2 `display_colorspaces` and `view_transforms` with a `cie_xyz_d65_interchange` space; without it display emulation is disabled and wide-gamut/HDR display will not work well, and saving colour space metadata also depends on it.
- Give every display a view transform without tone mapping, named `Standard` or `Un-tone-mapped`, or set the config-wide `default_view_transform`.
- Add Color Interop Forum IDs as colour space aliases; the `icc_profile_name` attribute is supported for embedding ICC profiles; mark HDR displays with `encoding: hdr-video`; name HDR views with `HDR 500 nits`, `HDR 1000 nits`, `HDR 2000 nits` or `HDR 4000 nits`.
- Copy a studio config and adapt the copy rather than editing the original.

## Checks

- Run Blender from a terminal and watch for OCIO errors at startup.
- The Color Management dropdowns should list the config's displays, views and colour spaces.
- `bpy.context.scene.view_settings.view_transform` shows the active view.

## Farm consistency

Every render node must set the same `OCIO` (or `BLENDER_OCIO`) variable and see the same config; a node without it uses Blender's default configuration and gives different colour.

## Verify

Render a colour chart on a workstation and on a farm node; output pixel values must match.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/color_management/opencolorio (OCIO and BLENDER_OCIO environment variables, roles list, guidelines for writing configurations) and Python API ColorManagedViewSettings.view_transform. Removed unconfirmed default install path, the claim about a role named XYZ, AgX-fallback behaviour and Flamenco-specific advice.
Method: documentation only; no commands were run.
