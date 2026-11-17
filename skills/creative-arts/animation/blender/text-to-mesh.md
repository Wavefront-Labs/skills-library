---
id: creative-arts.animation.blender.text-to-mesh
name: text-to-mesh
category: creative-arts
field: animation
product: blender
tags: [blender, text-object, text-to-mesh, text-to-curve, text-edit-mode, special-characters, convert]
level: practitioner
status: docs-checked
description: "Edit Blender text in place (Tab, cursor keys, Text menu, special characters, Insert Unicode) and convert it with Object > Convert to Curve or Mesh, with cleanup tips."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/texts/editing.html
  - https://docs.blender.org/manual/en/5.2/modeling/texts/selecting.html
  - https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/convert.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# text-to-mesh

Goal: type and fix text quickly, then convert it when you need geometry-level control.

## Edit mode text editing

- `Tab` enters and leaves Edit Mode (it does not insert a tab character). Most mesh Edit Mode shortcuts do not exist for text.
- Cursor and selection: arrows, `Ctrl Left/Right` by word, `Home/End` line start/end, `PageUp/PageDown` ten lines, `Shift Ctrl Home/End` to the top/bottom, `Shift` plus a cursor key selects, `Ctrl A` selects all.
- 3D Viewport header **Text** menu: Cut (`Ctrl X`), Copy (`Ctrl C`), Paste (`Ctrl V`), **Paste File** (a UTF-8 text file), To Uppercase, To Lowercase, **Insert Unicode** (type a hexadecimal code point), **Special Characters** (a limited character map), Toggle Bold/Italics/Underline/Small Caps, Kerning, Delete (previous/next character or word).
- Accented characters can be composed: type the main character, press `Alt Backspace`, then the modifier character (for example `A`, `Alt Backspace`, `~`).
- The text buffer is in sync with the desktop clipboard; formatting is copied when pasting within Blender.
- A text data-block can be converted to a 3D object from the Text editor: Edit > Text to 3D Object (One Object, or One Object per Line).
- Python: `ob.data.body = "NEW TITLE"` sets the text of a text object.
- A text object is limited to 50,000 characters.

## Convert (Object Mode > Object > Convert)

- **Curve**: converts text to curve outlines, preserving the shape (the result is a Poly curve by default).
- **Mesh**: converts the text to a mesh; the defined resolution is taken into account, and faces from closed and extruded curves are kept.
- Duplicate the object first if you want to keep editable text.

## Cleanup after conversion

The topology is usually messy: use a Limited Dissolve deletion or a Remesh modifier.

## Gotchas

- A converted object no longer has a font link; keep the original text object for edits.

## Verify

After conversion the Outliner shows a Curve or Mesh object instead of Text; resolution matches the text's Preview/Render U.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Editing Text Objects, Selecting Text, Object > Convert) and 5.2 source for the `body` property. Confirmed: Tab behaviour, cursor/selection keys, Text menu entries and shortcuts, accent composition, Text to 3D Object, Convert > Curve/Mesh scope, cleanup tip, 50,000 character limit. Removed as unconfirmed: per-letter animation recipe (Separate by Loose Parts, origins), Keep Original for this conversion, export format claims, and the Geometry Nodes String to Curves alternative.
Method: documentation only; no commands were run.
