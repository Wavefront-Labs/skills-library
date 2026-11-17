---
id: creative-arts.animation.blender.text-fonts-loading
name: text-fonts-loading
category: creative-arts
field: animation
product: blender
tags: [blender, text-object, fonts, text-fonts-loading, load-font, font-variants, bold-italic]
level: practitioner
status: docs-checked
description: "Load fonts into Blender text objects: Regular/Bold/Italic/Bold Italic slots, applying styles to characters, the built-in Bfont, packing fonts and the Not a valid font error."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/texts/properties.html
  - https://docs.blender.org/manual/en/5.2/modeling/texts/editing.html
  - https://docs.blender.org/manual/en/5.2/files/blend/packed_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# text-fonts-loading

Goal: the right typeface (and its bold/italic cuts) on 3D text, portable to other machines.

## Font slots (Properties > Data > Font)

- Four font style data-block menus: Regular (Normal), Bold, Italic, Bold & Italic. The built-in font is always present and is listed as **Bfont**.
- Click one of the **Load** buttons and pick a font file. The File Browser marks valid fonts with a capital "F" icon; an unsupported file gives the error `Not a valid font`. Blender supports PostScript Type 1, OpenType and TrueType fonts.
- Blender does not care what font you load into the Bold or Italic slots: they are placeholders, so load real Bold and Italic files of the family there. The same font applies to all characters of the same style, and a separate font is needed for each style.
- Apply a style to characters with the **Bold**, **Italic**, **Underline** and **Small Caps** toggles in the Font panel, or in Edit Mode with the Text menu > Toggle Bold/Italics/Underline/Small Caps, with the characters selected (or before typing for new text).
- Selecting text: hold `Shift` with the arrow keys; `Ctrl A` selects all.

## Portability

- File > External Data > **Pack Resources** marks eligible external files as packed; actual packing happens on the next save. A single file can be packed with the gift-box icon next to its path. Automatically Pack Resources does this for every external file.

## Gotchas

- Changing the Regular slot changes every character not marked bold or italic.
- Characters styled Bold but with no Bold font loaded use whatever the Bold slot holds (by default the built-in font).

## Verify

In Edit mode bold characters display the loaded Bold face; after saving with packing enabled, the font shows the packed icon.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Text Properties > Font, Editing Text Objects, Packed Data). Confirmed: four style slots and Bfont, Load buttons, supported formats, "Not a valid font" error, placeholder warning, style toggles, Pack Resources behaviour. Removed as unconfirmed: Ctrl B/I/U shortcuts, variable-font and non-Latin shaping statements, relative-path and Report Missing Files claims, licensing advice, duplicate `font.001` note and the Python `packed_file` check.
Method: documentation only; no commands were run.
