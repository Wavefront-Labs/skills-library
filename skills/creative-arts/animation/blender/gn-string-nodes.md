---
id: creative-arts.animation.blender.gn-string-nodes
name: gn-string-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-string-nodes, string-to-curves, value-to-string, join-strings, motion-graphics, counters]
level: practitioner
status: verified
description: "Generate animated text in Geometry Nodes: String to Curves (font, size, alignment, overflow), Value to String counters, Join Strings, Fill Curve plus Extrude, per-letter motion."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/text/string_to_curves.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/text/value_to_string.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/fill_curve.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-string-nodes

Goal: text driven by data — counters, scoreboards, labels per object, per-letter animation. For classic text objects see `text-objects`.

## String to Curves

- Inputs: **String**, **Size**, **Font**, **Align X** (Left, Center, Right, Justify, Flush), **Align Y** (Top, Top Baseline, Middle, Bottom Baseline, Bottom), **Pivot Point**, **Character/Word/Line Spacing**, and the text box (**Overflow** with Overflow, Scale To Fit or Truncate, plus **Text Box Width/Height**).
- Outputs **Curve Instances** (one instance per character; each unique character is converted once and reused), **Remainder** (text that did not fit, Truncate mode only), **Line** (an index field on the Instance domain; 4.5.14 has no Word output, the 5.x manual lists one) and **Pivot Point**.
- Because every character is an instance, animate per letter with Translate/Rotate Instances using Index-based offsets against Scene Time. Realize Instances is needed to process each character as unique geometry.

## Value to String

Float or Integer to String. Float uses **Decimals** (precision); Integer mode in 4.5.14 has only the Value input (the 5.x manual also lists Base and Padding). Counter: Scene Time Frame → Map Range → Value to String (0 decimals) → Join Strings with a prefix and suffix.

## Making it solid

`String to Curves → Realize Instances → Fill Curve (*Mode* N-gons or Triangles; the fill is flat at local Z 0) → Extrude Mesh (Offset Scale = depth) → Set Material`. *Group ID* on Fill Curve keeps curves in separate groups (separate mesh islands).

## Other string nodes

Join Strings (*Delimiter*; order follows the multi-input socket), String Length, Slice String (*Position* from index 0, *Length*; typewriter effect: Length = frame-driven integer), Replace String, Special Characters (Line Break and Tab outputs, for multi-line strings with Join Strings), Float to Integer for counters.

## Gotchas

- Realize Instances too early and every unique character is no longer shared; do per-letter instance animation first.
- Socket inspection (hover the String socket) shows the string value used at the last evaluation.

## Verify

Scrub: counter updates every frame without jitter (set Decimals 0, round the value first); letters animate in order.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the String to Curves, Value to String, Join Strings, Slice String, Special Characters and Fill Curve pages: input and output names, alignment and overflow options, Value to String Decimals/Base/Padding, Fill Curve modes. Removed unconfirmed claims about font packing and kerning differences versus Text objects.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): String to Curves outputs are Curve Instances, Remainder, Line and Pivot Point; Align X (Left, Center, Right, Justify, Flush), Align Y (Top, Top Baseline, Middle, Bottom Baseline, Bottom), Overflow (Overflow, Scale To Fit, Truncate), Pivot Point modes and Text Box Width and Height exist. Value to String of 3.14159 with Decimals 2 gave a 4-character string and 2.5 with Decimals 0 gave 1 character; integer mode shows only Value (no Base or Padding, no Word output in 4.5.14: removed). Fill Curve Mode N-gons gave 1 face and Triangles 30 faces for a 32-point circle. Special Characters has Line Break and Tab outputs. Not run (confirmed from the manual only): Slice String, Replace String and Join Strings details, per-letter animation, Remainder behaviour.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
