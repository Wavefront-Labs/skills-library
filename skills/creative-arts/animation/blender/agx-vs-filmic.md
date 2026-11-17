---
id: creative-arts.animation.blender.agx-vs-filmic
name: agx-vs-filmic
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, agx, filmic, view-transform, agx-vs-filmic, standard-transform]
level: practitioner
status: verified
description: "Choose a Blender view transform: Standard, AgX, Filmic (deprecated), ACES 1.3/2.0, Khronos PBR Neutral, Filmic Log, False Color and Raw, with the manual's description of each."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
  - https://docs.blender.org/manual/en/latest/render/color_management/color_spaces.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# agx-vs-filmic

Goal: pick the view transform that matches the deliverable and keep it the same through the project.

## Render Properties > Color Management > View Transform

| Transform | What the manual says | Use it for |
|---|---|---|
| **Standard** | No extra conversion besides the display conversion | Non-photorealistic work, video editing where a look is already baked in |
| **AgX** | Tone mapping that improves on Filmic, 16.5 stops of dynamic range, desaturates highly exposed colours like film | Photorealistic results |
| **Filmic** | Tone mapping for high dynamic range; deprecated and superseded by AgX (better handling of saturated colours) | Matching an older approved look |
| **ACES 1.3** / **ACES 2.0** | ACES view transforms (listed in the 5.2 manual; the stock Blender 4.5.14 view list has none, so expect them only in newer versions or a custom OCIO config); 2.0 has a more neutral look, less mid-tone contrast, gentler highlight rolloff and improved gamut mapping | ACES pipelines (see aces-workflow) |
| **Khronos PBR Neutral** | Keeps sRGB output matching the input sRGB base colour under grey-scale lighting | Product photography, well-exposed scenes |
| **Filmic Log** | Converts to the Filmic log colour space | Export to grading applications, or inspecting very dark/light areas |
| **False Color** | Heat map of image intensities for exposure checks | Lighting checks |
| **Raw** | No colour space conversion | Inspecting only, not final export |

## Rules

- Blender converts textures and colours to scene linear whatever the view; the view changes only the display and render output.
- Exact brand colours: Standard avoids tone mapping; AgX desaturates highly exposed colours by design.
- Looks (see look-contrast) are chosen per view transform. In 4.5.14 AgX offers None, AgX - Punchy, AgX - Greyscale and AgX - Very High / High / Medium High / Base / Medium Low / Low / Very Low Contrast; False Color has the same set with a False Color prefix; Standard, Khronos PBR Neutral, Filmic, Filmic Log and Raw offer None and Very High to Very Low Contrast (no Base, Punchy or Greyscale).
- AgX Log and Filmic Log are also listed as colour spaces; the View Inverse colour spaces (for example AgX Base sRGB) let a background image bypass the view transform.

## Gotchas

- Do not switch the view transform mid-production without re-approving lighting.
- False Color maps linear values to colours: 16% to 22% is grey, 5% to 16% green-cyan, 80% to 97% red, high clip white.

## Verify

Render with False Color and check that key surfaces sit in the intended bands, then switch back to the chosen view.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/color_management/displays_views (Views list and descriptions, False Color table, Filmic deprecated) and color_spaces (AgX Log and Filmic Log colour spaces, View Inverse). Removed unconfirmed default-view, clipping, hue-skew, Raw/log claims and the Filmic-project-keeps-Filmic claim; added ACES 1.3/2.0, corrected Filmic Log vs AgX Log.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): the Scene view_settings.view_transform enum is Standard, Khronos PBR Neutral, AgX, Filmic, Filmic Log, False Color, Raw (no ACES entries); looks list per view transform printed; colour spaces include AgX Log, Filmic Log, AgX Base sRGB, Khronos PBR Neutral sRGB; the display devices are sRGB, Display P3, Rec.1886, Rec.2020; factory-startup scene reads Raw only because read_factory_settings(use_empty) was used. Not run (confirmed from the manual only): stop counts, the descriptions of each transform, the False Color percentage bands and the ACES 1.3/2.0 behaviour.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
