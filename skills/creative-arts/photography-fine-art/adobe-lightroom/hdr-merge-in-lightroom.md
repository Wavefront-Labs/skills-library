---
id: creative-arts.photography-fine-art.adobe-lightroom.hdr-merge-in-lightroom
name: hdr-merge-in-lightroom
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, hdr-merge, photo-merge, deghost, hdr-dng, lightroom-classic]
level: practitioner
status: draft
description: "Merge exposure brackets to an HDR DNG in Lightroom Classic: auto align, auto settings, deghost amount, overlay checks, and editing the 32-bit result."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Merge photos to HDR)", "https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/hdr-output.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HDR merge in Lightroom

Lightroom's HDR merge produces a **floating-point raw DNG** (not a tone-mapped image), so you edit it with normal Develop sliders and with an extended Exposure range (+/-10 EV).

## Steps
1. Select the bracket (raws, ideally 3-5 frames at 1-2 EV spacing). Remove lens/Upright edits first or keep them identical across frames.
2. Photo > Photo Merge > **HDR** (Ctrl/Cmd+H). Shift+click the menu (Ctrl/Cmd+Shift+H) to merge headless with last settings.
3. Options:
   - **Auto Align**: on for handheld brackets.
   - **Auto Settings**: applies an Auto tone as a starting point; safe to leave on, edits remain adjustable.
   - **Deghost Amount**: None/Low/Medium/High for moving elements (leaves, people, water). Tick **Show Deghost Overlay** to see the areas taken from a single frame.
   - **Create Stack** groups the result with its sources.
4. Merge. Output: `*-HDR.dng` in the same folder.

## Editing
- Pull Highlights down and lift Shadows moderately; use masks for skies rather than extreme global sliders, to avoid the flat "HDR look".
- Merged DNG supports Denoise and masks like any raw.

## Gotchas
- Deghost High can create noise-mismatched patches from the darkest frame; prefer Low/Medium.
- Brackets with different white balance or lens settings produce odd colour; sync WB before merge.
- HDR merge output is a scene-referred file; "HDR output" (HDR display editing) is a separate feature.

## Verify
- [ ] Highlights show detail at -2 EV and shadows clean at +2 EV in the merged file; no ghost edges on moving subjects at 100%.
