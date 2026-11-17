---
id: creative-arts.animation.blender.vse-text-styling
name: vse-text-styling
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, text-strip, vse-text-styling, text-strip-font, text-shadow]
level: practitioner
status: docs-checked
description: "Style VSE text strips: font loading, size, colour, shadow and outline, box background, location and anchor, wrap width, and keyframing for animated titles."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/text.html
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/preview/display/overlays.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-text-styling

Goal: clean titles, lower thirds and captions in the edit.

## Text strip, Sidebar > Effect Strip

- **Style presets** in the header: Subtitle, Main Title and Title Corner are included. (Blender 4.5.14 text strips have `alignment_x`, `anchor_x/y`, `location`, `wrap_width`, `font`, `font_size`, colours, shadow, outline and box properties, but no line spacing or vertical alignment property, so those two controls and the presets are 5.x.)
- **Text**: multi-line, UTF-8. Edit in the field or directly in the Preview: press **Tab** over the preview to enter text edit mode and Tab again to leave (Ctrl C, Ctrl V, Ctrl X, Ctrl A, arrow keys, Home and End work there).
- **Wrap Width**: percentage of the frame width, 0 disables wrapping.
- **Style**: **Font** (a font data-block with Bold and Italic toggles), **Size**, **Line Spacing** (factor of text size, or absolute pixels via the toggle), **Color**.
- **Outline**: Color and Width. **Shadow**: Color, Angle (0 degrees right, 90 below), Offset and Blur. **Box**: Color, Margin (a factor of image width) and Roundness (factor of box height).
- **Layout**: **Location X, Y**, **Alignment X, Y** (left, centre, right) and **Anchor X, Y** (the origin of the text relative to the location).

## Lower third recipe

Text strip with Box on a dark colour, anchored at the lower left, with Location set near the lower left corner. Fade in and out with strip Opacity keys (Sidebar > Strip > Compositing > Opacity).

## Animation

Properties can be keyframed: hover and press I. Slide-in titles: key Location.

## Subtitles

All Text strips in a sequence can be exported as a SubRip (.srt) file (Export Subtitles operator), which suits Text strips used as subtitles.

## Gotchas

- Check titles against the safe areas: the Preview Overlays popover and the Sidebar View tab both have **Safe Areas**.
- Text appearance depends on the scene resolution, so verify at the final resolution.

## Verify

Render a frame at final resolution and check the title is crisp, inside the safe areas and readable on a small screen.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Text strip fields (presets, Text, Wrap Width, Font with Bold and Italic, Size, Line Spacing, Color, Outline, Shadow, Box, Location, Alignment, Anchor), Tab text editing in the Preview, SubRip export, Safe Areas overlay and Sidebar entry. Removed the pixel-size, 0 to 1 location, font packing and recipe numbers, which the manual does not state.
- Run note, 2026-11-01, Blender 4.5.14 LTS headless: a TEXT effect strip has `text` (multi-line and non-ASCII text accepted), `font_size` (default 60), `color`, `shadow_color/angle/offset/blur`, `outline_color/width`, `box_color/margin/roundness`, `use_shadow/outline/box/bold/italic`, `alignment_x` (LEFT, CENTER, RIGHT), `anchor_x` and `anchor_y`; `sequencer.export_subtitles` exists.
Method: documentation checked against the manual and API pages; part of the claims were run headless in Blender 4.5.14 (see the run note), but other claims describe Blender 5.x features that 4.5.14 does not have, so the status stays docs-checked.
