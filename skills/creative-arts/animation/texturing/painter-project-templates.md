---
id: creative-arts.animation.texturing.painter-project-templates
name: painter-project-templates
category: creative-arts
field: animation
product: texturing
tags: [painter-template, substance-painter, project-template, shader-settings, normal-map-format, spt, studio-standards, project-configuration]
level: practitioner
status: draft
description: "Create Substance 3D Painter project templates (.spt) for a show: shader, channels, normal format, colour management and default resolution, shared across artists."
sources:
  - https://helpx.adobe.com/substance-3d-painter/project-management/project-templates.html
  - https://helpx.adobe.com/substance-3d-painter/project-management/project-configuration.html
  - https://helpx.adobe.com/substance-3d-painter/project-management/color-management.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Painter project templates

**Goal:** every artist starts a texturing project with the same channels, shader, normal convention,
colour management and resolution, so outputs drop into the pipeline without per-asset fixes.

## What a template stores

- Texture set channel list (and user channels).
- Shader (PBR metal/rough, spec/gloss, or a custom/stylised shader).
- Normal map format (OpenGL vs DirectX), tangent space per fragment setting.
- Default document resolution.
- Environment/lighting presets in the viewport (helps consistency of look approval).

Colour management settings (ACES/OCIO vs legacy) are project/preferences level: set them for the show
and document them with the template (`creative-arts.animation.color.look-development-for-color-pipelines`).

## Making one

1. New project with a representative mesh; configure channels, shader, normal format, resolution.
2. File - Save as Template; store the `.spt` on shared storage (Shelf - add the folder as a shelf
   location so it appears for everyone).
3. Artists choose it in File - New - Template.
4. Pair with a show export preset (`creative-arts.animation.texturing.painter-export-presets`).

## Show choices to decide up front

| Decision | Typical |
|---|---|
| Normal format | renderer-dependent: Blender/Maya Arnold/Unity use OpenGL; Unreal uses DirectX |
| Resolution | hero 4K, secondary 2K, background 1K; set per set later |
| Channels | base colour, roughness, metallic, normal, height, emissive; plus opacity where needed |
| Colour | ACES/OCIO project with the show config, or sRGB legacy for real-time |

## Gotchas

- Changing a template does not update existing projects; version template names (`SHOW_char_v02.spt`).
- A template's mesh-specific settings (bakes) are not reused; bake per asset.
- Custom shaders must exist on every artist's shelf or the project falls back to default.

## Verify

Two artists create projects from the template; Texture Set Settings and Project Configuration are
identical, and a test export matches pipeline naming and formats.
