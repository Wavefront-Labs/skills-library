---
id: creative-arts.animation.blender.text-objects
name: text-objects
category: creative-arts
field: animation
product: blender
tags: [blender, text-object, text-objects, fonts, 3d-text, typography, titles, text-on-curve, extrude-bevel, convert-to-mesh, lower-thirds, motion-graphics]
level: practitioner
status: verified
description: "Make 3D titles and labels with Blender text objects: fonts, Object Font, spacing, extrude/bevel geometry, text on a curve, scripted content, converting to curve or mesh."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/texts/index.html
  - https://docs.blender.org/manual/en/5.2/modeling/texts/introduction.html
  - https://docs.blender.org/manual/en/5.2/modeling/texts/properties.html
  - https://docs.blender.org/manual/en/5.2/modeling/texts/editing.html
licence: Apache-2.0
version: 6
updated: 2026-11-17
aliases: []
---

# text-objects

Goal: typeset readable 3D text that renders cleanly, animates where needed, and can be handed off as mesh.

## What a text object is

Text objects belong to the same family as curves and surfaces: fonts are vector data. By default letters are flat filled surfaces like closed 2D curves; like curves they can be extruded and can take modifiers (for example the Curve modifier). Blender supports PostScript Type 1, OpenType and TrueType fonts, a built-in font (Bfont), and even existing objects as letters. The manual gives a limit of 50,000 characters per text object; assigning `body` a 60,000-character string from Python was accepted in 4.5.14, so do not rely on the API to enforce it. The more characters, the slower it responds.

## Editing

`Tab` enters and leaves Edit Mode (no tab character is inserted). Most mesh Edit Mode shortcuts do not exist for text. Use the 3D Viewport header **Text** menu (Cut, Copy, Paste, Paste File, To Uppercase, To Lowercase, Insert Unicode, Special Characters, Toggle Bold/Italics/Underline/Small Caps, Kerning, Delete). `Ctrl A` selects all; `Shift` with cursor keys selects. See text-to-mesh for details.

## Fonts (Properties > Data > Font)

- Four style slots (Regular, Bold, Italic, Bold & Italic); Blender uses whatever font you load into each. Load with the Load buttons; see text-fonts-loading.
- **Size** (whole text), **Shear** (inclination, not italics), **Small Caps Scale**, underline position and thickness.
- **Object Font**: renders characters with objects. Name objects with a common prefix plus the character (for example `ft.a`, `ft.b`), enable Instancing Vertices on the text object, and enter the prefix in the Object Font field. Objects are placed with their centre at the lower right corner of the character.
- **Text on Curve**: select a curve for the text to follow. The manual's tip says the Curve modifier gives more control and is the standard way to do this in modern Blender.

## Paragraph and spacing

Horizontal and vertical alignment, Character/Word/Line Spacing and Offset X/Y: see text-paragraph. Frames and overflow modes: see text-boxes.

## Geometry (making it 3D)

Offset, Extrude, Taper and Bevel: see text-extrude-bevel and the curve skills. In the Shape panel the 5.2 manual recommends the **Delaunay** Fill Solver for text (4.5.14 has no solver property on `Curve`), because most font files contain self-intersecting curves; Fill Rule (Even-Odd, Non-Zero) applies to Delaunay. **Fast Editing** shows only outlines in Edit Mode.

## Scripted content

`ob.data.body = "text"` sets the displayed string, so a frame-change handler or similar script can drive counters or labels. Size, spacing and similar numeric properties can be keyed like other properties.

## Converting

Object Mode > Object > Convert > **Curve** (outlines; in 4.5.14 the result has Bezier splines, 3 for the text `Hi`) or **Mesh** (defined resolution is used; closed and extruded faces are kept). The topology of the result is usually messy; use Limited Dissolve or a Remesh modifier. Duplicate the text first if you want to keep it editable.

## Gotchas

- Overlapping letters (script fonts, tight kerning) can fill incorrectly with Sweep Line; switch Fill Solver to Delaunay.
- Offset can quickly cause artifacts.
- Bold and Italic toggles only change which slot's font is used.
- Truncate (text boxes) only truncates in Object Mode.

## Verify

- The title renders cleanly at the intended resolution (raise Resolution Preview/Render U if outlines look faceted).
- Converted mesh: Face Orientation overlay shows consistent normals.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Text introduction, Text Properties, Editing and Selecting Text, Object > Convert) and 5.2 source for the `body` property. Confirmed: supported font formats and Bfont, 50,000 character limit, Tab behaviour and Text menu entries, Object Font procedure, Text on Curve tip, Fill Solver recommendation, convert behaviour. Corrected: Ctrl B/I/U and Ctrl Backspace shortcuts are not documented; "Fill Mode Both default", Preview U default 12, bevel resolution advice, "variable fonts and colour emoji unsupported", ligature and RTL statements, the Typewriter add-on, String to Curves and Alembic/USD export statements were removed as unconfirmed.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: `Curve` of type FONT has `body`, `size` (1.0), `shear`, `small_caps_scale` (0.75), `underline_position`, `underline_height`, `font`, `font_bold`, `font_italic`, `font_bold_italic` (all Bfont Regular), `align_x`, `align_y`, `overflow` (NONE, SCALE, TRUNCATE), `space_character/word/line`, `offset_x/y`, `text_boxes`, `follow_curve`, `family`, `use_fast_edit`; doubling `size` doubled the width, `space_character` 2.0 widened the text, `shear` 0.5 shifted it; `extrude` 0.1 gave z from -0.1 to 0.1; `body` accepts newline and tab characters; Convert to Curve gave 3 Bezier splines and Convert to Mesh kept the extruded faces; the Curve modifier can be added to a text object; Text menu operators exist (`style_toggle` BOLD, ITALIC, UNDERLINE, SMALL_CAPS, `case_set`, `text_insert_unicode`, `text_paste_from_file`). Fixed: Convert to Curve gives Bezier, not Poly, splines. Unrun (UI or 5.x only): Tab handling and shortcuts, Object Font workflow, Text on Curve, Fill Solver and Fill Rule, the 50,000 limit, Truncate behaviour.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
