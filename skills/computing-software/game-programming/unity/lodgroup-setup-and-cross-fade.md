---
id: computing-software.game-programming.unity.lodgroup-setup-and-cross-fade
name: lodgroup-setup-and-cross-fade
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-graphics, lodgroup, level-of-detail, lod-cross-fade, lod-bias, rendering-performance, game-programming]
level: practitioner
status: docs-checked
description: "Set up a Unity LOD Group: transition screen heights, Fade Mode and cross-fade settings, Object Size, LOD Bias, and the LODGroup API (ForceLOD, SetLODs)."
sources: ["https://docs.unity3d.com/Manual/class-LODGroup.html", "https://docs.unity3d.com/ScriptReference/LODGroup.html", "https://docs.unity3d.com/ScriptReference/QualitySettings-lodBias.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LODGroup setup and cross-fade

**Goal:** swap to cheaper meshes as an object gets smaller on screen, without visible pops. Unity 6000.x docs.

## Inspector reference
- **LOD Group selection bar**: coloured boxes for LOD 0, LOD 1, LOD 2 and Culled. A box shows the percentage of screen
  height at which that level becomes active (50% means the object fills half the camera view height). Drag a boundary to
  change it; drag the camera icon to preview a level in the Scene view. Disable Preferences > Scene View > Enable
  Filtering While Editing LOD Groups to avoid the grey-out while previewing.
- **Renderers panel** (select a LOD box): **Transition (% Screen Size)** (with the camera distance in metres beside it),
  **Set to Camera**, **Fade Transition Width**, and the **Renderers** list for that level.
- **Object Size** (metres): changing 1 to 0.6 makes a 100% screen-height object count as 60%, so transitions to less
  detailed levels happen closer to the camera. **Reset Object Size** returns it to 1 while keeping transition distances.
- **Recalculate Bounds**: use after modifying a LOD, for example changing the Scale of a LOD renderer's Transform.
  **Recalculate Lightmap Scale** updates Scale in Lightmap on all Mesh Renderers from the new boundaries.
- **Global Illumination LOD**: which LOD is used for GI (default LOD0, or None); only applies when Default Light Baker is
  Unity Compute Light Baker.

## Fade
- **Fade Mode**: None (switch without transition), Cross Fade (cross-fades the model between current and next LOD), Speed
  Tree (interpolates vertex positions; only for SpeedTree models with .spm and .st extensions).
- **Animate Cross-fading** (Cross Fade or Speed Tree): one transition time for all LODs, applied after the threshold is
  reached. In script, `LODGroup.animateCrossFading` with the static `LODGroup.crossFadeAnimationDuration` in seconds
  (throws ArgumentException for zero or negative values).
- **Fade Transition Width**: only with Cross Fade and Animate Cross-fading off. A smaller value delays the start and
  shortens the transition; 0.4 on LOD0 means the transition to LOD1 occurs over 40% of the LOD0 range.

## Global bias
`QualitySettings.lodBias` is a global multiplier on LOD transition thresholds for all LOD Groups, minimum 0.1. Higher keeps
detailed LODs visible longer (better visuals, higher cost); lower transitions sooner (cheaper, worse visuals). It affects
only LOD Groups, not mesh LOD or other systems.

## Script API (LODGroup)
Properties: `animateCrossFading`, `enabled`, `fadeMode`, `lastLODBillboard` (last level is a BillboardRenderer),
`localReferencePoint`, `lodCount`, `size`. Methods: `GetLODs`, `SetLODs` (removes any existing LODs first),
`ForceLOD` (pass a negative value to return to automatic selection), `RecalculateBounds` (can be slow; call
infrequently).

## Checked
Date: 2026-11-07.
Read in full: "LOD Group component reference", `LODGroup` script reference and `QualitySettings.lodBias` (6000.6 docs).
The linked "Make LOD transitions smooth" and "Import or create LOD levels" pages were not opened.
Corrected: the draft said transitions use "bounds height / screen height" and that `lodBias` above 1 scales them; the page
states the minimum is 0.1 and describes the effect without a formula.
Removed as unconfirmed: auto-creation from `_LOD0`/`_LOD1` model names, `QualitySettings.maximumLODLevel`, the URP LOD
Cross Fade asset setting, the `LOD_FADE_CROSSFADE` keyword and `LODFadeCrossFade(positionCS)` HLSL, the `GetLODs` /
`screenRelativeTransitionHeight` snippet, FOV-dependent selection and scope advice, SetPass and first-person weapon
gotchas, and the invented Verify checklist.
Method: documentation only; no commands were run.
