---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.creating-custom-sub-tools-and-brushes-in-csp
name: creating-custom-sub-tools-and-brushes-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-brushes, csp-custom-brush, sub-tool-detail, brush-tip, sut-file, inking-brush]
level: advanced
status: draft
description: "Build custom brushes in Clip Studio Paint: duplicate a sub tool, Sub Tool Detail settings (tip, stroke, ink, texture, pressure curves), register brush tips and export .sut files."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating custom sub tools

## Start from a duplicate
- Sub tool palette menu > **Duplicate sub tool** on a close match (e.g. G-pen). Rename it.
- Or **Create custom sub tool** for a new tool from scratch (choose output process: direct draw, etc.).

## Sub Tool Detail (wrench icon)
| Category | Key settings |
|---|---|
| Brush size | size, pressure influence; **pressure curve** (edit graph) |
| Ink | opacity, blending mode, colour mixing for paint brushes |
| Anti-aliasing | for crisp vs soft line |
| Brush tip | circle or **material** tip (register a tip image via Edit > Register material > Image, "use for brush tip shape"), hardness, thickness, direction |
| Stroke | gap/spacing, ribbon, repeat method |
| Texture | paper texture, density, apply to each tip |
| Starting and ending | taper in/out (great for inking) |
| Correction | stabilization, post correction, vector magnet |
- Toggle the eye icon next to a setting to show it in Tool property for quick access.

## Save and share
- Sub tool palette menu > **Export sub tool** saves `.sut`; others import via **Import sub tool** or drag
  the file into the Sub tool palette.
- Register to Clip Studio Assets to publish.

## Global pen pressure
- File > Pen pressure settings (or Preferences > Tablet) adjusts pressure for all tools; tune this first,
  then per-brush curves.

## Gotchas
- Editing the original default sub tool without duplicating loses defaults (reset via Initialize sub tool).
- Texture brushes at large size slow the canvas.

## Verify
- [ ] Brush draws as expected at 100% zoom on the page resolution you use.
- [ ] Exported .sut imports cleanly on another machine.
