---
id: creative-arts.animation.color.input-transforms-for-sources
name: input-transforms-for-sources
category: creative-arts
field: animation
product: color
tags: [input-transform, idt, colour-space-tagging, texture-colour-space, file-rules, ocio, aces, camera-log, reference-footage]
level: practitioner
status: draft
description: "Assign the right input transform to every source in an animation pipeline: textures, HDRIs, camera plates, client logos and reference video, using OCIO file rules."
sources:
  - https://opencolorio.readthedocs.io/en/latest/guides/authoring/rules.html
  - https://docs.acescentral.com/
  - https://opencolorio.readthedocs.io/en/latest/configurations/aces_studio.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input transforms for camera and texture sources

**Goal:** each incoming image is linearised and converted to the working space exactly once, with the right
assumption about how it was encoded.

## Source table

| Source | Input transform |
|---|---|
| Painted textures, logos, design PNG/JPG | sRGB - Texture (sRGB EOTF, Rec.709 primaries) |
| Data maps (normal, roughness, masks) | Raw / data; never colour-converted |
| HDRI from bracketed photos | Linear Rec.709 (sRGB primaries) unless captured otherwise |
| Live-action plates (hybrid shows) | the camera's log/gamut, e.g. ARRI LogC4/AWG4, Sony S-Log3/S-Gamut3.Cine, RED Log3G10/RWG; ACES studio config provides them |
| Rec.709 reference video | Rec.1886 Rec.709 display (inverse output) or "Utility - Rec.709 - Camera"; choose deliberately |
| Previously graded deliverables | the display space they were graded for, through an inverse output transform |

## Automate with file rules

OCIO v2 `file_rules` assign spaces by path pattern or extension, so artists do not choose:

```yaml
file_rules:
  - !<Rule> {name: data_maps, pattern: "*_{normal,rough,metal,height,mask}*", extension: "*", colorspace: Raw}
  - !<Rule> {name: exr_renders, pattern: "*", extension: exr, colorspace: ACEScg}
  - !<Rule> {name: Default, colorspace: sRGB - Texture}
```

Glob braces are supported by OCIO's pattern syntax; test patterns with `ociocheck` and a sample of file names.
DCCs honour file rules in different degrees (Nuke, Houdini, Maya support them; Blender assigns per image node), so
also tag in the DCC.

## Inverse output transforms

Bringing display-referred material (a client logo graded in sRGB, a Rec.709 video) through the inverse output
transform makes it round-trip exactly to the same display values, which is usually what clients expect. Using
the sRGB texture input instead makes it behave as a reflectance under the tone curve and look darker/flatter.

## Verify

Load each source type in the compositor with the show view: logos match the brand hex on screen, camera plates
match the camera manufacturer's LUT preview, data maps read raw values.
