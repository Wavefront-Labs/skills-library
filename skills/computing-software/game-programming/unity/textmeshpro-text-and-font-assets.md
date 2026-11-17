---
id: computing-software.game-programming.unity.textmeshpro-text-and-font-assets
name: textmeshpro-text-and-font-assets
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-ui, textmeshpro, tmp-font-asset, sdf-fonts, rich-text, localization-fonts, game-programming]
level: practitioner
status: draft
description: "Use TextMeshPro well: SDF font asset generation, dynamic vs static atlases, fallback fonts for localisation, material presets, rich text, and allocation-free updates."
sources: ["https://docs.unity3d.com/Packages/com.unity.textmeshpro@3.2/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/TextMeshPro/FontAssetsCreator.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TextMeshPro text and font assets

**Goal:** crisp text at any size, every language renders, no per-frame garbage.

## Font assets
- Window > TextMeshPro > **Font Asset Creator** (or right-click a font > Create > TextMeshPro > Font Asset).
- **Static** atlas: pre-baked character set (ASCII, game-specific list). Use for shipping Latin UI.
- **Dynamic**: glyphs added to the atlas at runtime from the source font. Needed for CJK and user text;
  the source font file must ship. Enable **Multi Atlas Textures** to grow beyond one texture.
- Settings: Sampling Point Size auto, **Padding** about 10% of sampling size (outlines and glow need
  padding), Render Mode SDFAA, atlas 1024-4096.
- **Fallback Font Assets** list (per font, plus global in TMP Settings): base Latin font -> dynamic
  CJK -> emoji/symbols. Missing glyphs show as squares, logged as warnings.

## Materials
- Each font asset has a default material; create **Material Presets** (duplicate material, keep the
  font atlas) for outline, shadow, glow variants. Switching presets keeps batching per material.
- Underlay = drop shadow, Outline thickness needs padding, Face Dilate for bold-ish.
- Different materials break batching; reuse presets.

## Rich text and features
`<b>`, `<color=#ff0>`, `<size=120%>`, `<sprite name="coin">` (Sprite Asset), `<link="id">`
(detect with `TMP_TextUtilities.FindIntersectingLink`), `<nobr>`, `<voffset>`. Disable Rich Text on
user-entered strings (players typing tags). Auto Size is expensive (multiple layout passes); prefer
fixed sizes per resolution class.

## Updating without garbage
```csharp
scoreText.SetText("Score: {0}", score);        // formats without allocating a string
timerText.SetText("{0:1}", seconds);            // one decimal
```
`text = $"..."` allocates every call; only set when the value changes.

## Localisation
- Arabic/Hebrew need RTL handling (`isRightToLeftText`) and shaping (TMP doesn't shape Arabic natively;
  use a shaping plugin or pre-shaped strings).
- Thai/Indic complex scripts also need shaping. Test with real strings early.

## Verify
- [ ] Every shipped language renders with no squares (fallback chain complete).
- [ ] Profiler shows zero GC alloc from HUD text updates.
