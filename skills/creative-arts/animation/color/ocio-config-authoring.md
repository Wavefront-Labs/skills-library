---
id: creative-arts.animation.color.ocio-config-authoring
name: ocio-config-authoring
category: creative-arts
field: animation
product: color
tags: [ocio-config, opencolorio, ocio, colour-management, color-management, roles, displays-views, file-rules, ociocheck, aces]
level: advanced
status: draft
description: "Author and edit an OpenColorIO v2 config for an animation show: roles, colour spaces, displays/views, file rules and looks, validated with ociocheck."
sources:
  - https://opencolorio.readthedocs.io/en/latest/guides/authoring/overview.html
  - https://opencolorio.readthedocs.io/en/latest/configurations/aces_studio.html
  - https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Authoring an OCIO config

**Goal:** one `config.ocio` that every DCC, renderer, compositor and review tool on the show loads via `$OCIO`, so
a pixel means the same thing everywhere.

## Start from a reference, do not write from scratch

OCIO 2.2+ ships built-in configs addressable by URI: `ocio://cg-config-latest` (small, CG-oriented ACES) and
`ocio://studio-config-latest` (adds camera input transforms). Export one to disk and trim it:

```
python -c "import PyOpenColorIO as o; open('config.ocio','w').write(o.Config.CreateFromFile('ocio://cg-config-latest').serialize())"
```

or download the matching release from the OpenColorIO-Config-ACES repository.

## Anatomy (OCIO v2)

```yaml
ocio_profile_version: 2.1
environment: {SHOW_LUTS: <SHOW_ROOT>/color/luts}
search_path: "luts:${SHOW_LUTS}"
roles:
  scene_linear: ACEScg
  rendering: ACEScg
  compositing_log: ACEScct
  color_timing: ACEScct
  texture_paint: sRGB - Texture
  data: Raw
  default: Raw
  aces_interchange: ACES2065-1
  cie_xyz_d65_interchange: CIE-XYZ-D65
file_rules:
  - !<Rule> {name: exr, extension: exr, pattern: "*", colorspace: ACEScg}
  - !<Rule> {name: Default, colorspace: sRGB - Texture}
displays:
  sRGB - Display: [!<View> {name: ACES 1.0 - SDR Video, view_transform: ACES 1.0 - SDR Video, display_colorspace: sRGB - Display}]
  Rec.1886 Rec.709 - Display: [...]
active_displays: [sRGB - Display, Rec.1886 Rec.709 - Display]
looks: [...]   # see ocio-looks-per-shot
```

Required interchange roles (`aces_interchange`, `cie_xyz_d65_interchange`) let OCIO convert between configs; keep them.

## Editing rules

- Add show colour spaces (e.g. a stylized "Toon - Texture" sRGB space) by copying an existing one and changing only
  name and transforms; give each a `family` so menus group cleanly.
- Use `active_displays`/`active_views` to hide options artists must not pick.
- Put LUT files on `search_path`, never absolute paths; use `environment` variables for per-show roots.
- Version the config in git with the show; changing a config mid-show changes every render, so treat it like code.

## Validate

`ociocheck --iconfig config.ocio` must report no errors and resolve every file in the search path. Then
`ocioconvert` a known test EXR to the display and compare against the previous config's output.

## Verify

Blender, Nuke/Natron, Krita and the review player all list the same displays and views with `OCIO` set, and a
reference frame looks identical in each (see `creative-arts.animation.color.look-development-for-color-pipelines`).
