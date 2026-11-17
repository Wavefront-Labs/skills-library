---
id: creative-arts.animation.vector-graphics.inkscape-cli-batch-export
name: inkscape-cli-batch-export
category: creative-arts
field: animation
product: vector-graphics
tags: [inkscape-cli, vector-export, svg-export, inkscape, batch-export, export-id, export-dpi, plain-svg, pdf-export, actions]
level: practitioner
status: docs-checked
description: "Batch-export SVG artwork with the Inkscape 1.x command line: PNG at set sizes/DPI, per-object IDs, plain SVG and PDF, actions, and scripting over folders."
sources:
  - https://www.mankier.com/1/inkscape
  - https://wiki.inkscape.org/wiki/Using_the_Command_Line
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inkscape command-line batch export

**Goal:** export hundreds of SVG assets (props, UI, title elements, per-frame drawings) to PNG/SVG/PDF without
opening the GUI, with consistent sizes. Syntax below is Inkscape 1.x.

## Common commands

```bash
# PNG at a fixed width in pixels
inkscape icon.svg --export-type=png --export-width=1024 --export-filename=icon_1024.png
# PNG at DPI, whole drawing instead of page
inkscape prop.svg --export-type=png --export-dpi=300 --export-area-drawing --export-filename=prop.png
# a single object by its id (e.g. a layer group named "logo")
inkscape sheet.svg --export-id=logo --export-id-only --export-type=png --export-filename=logo.png
# plain SVG (no sodipodi:/inkscape: namespaces, no RDF metadata) and PDF with text as paths
inkscape art.svg --export-plain-svg --export-filename=art_plain.svg
inkscape art.svg --export-type=pdf --export-text-to-path --export-filename=art.pdf
```

Background of exported PNG: `--export-background` (colour) and `--export-background-opacity`.
`--export-id-only` is ignored without `--export-id`. The default PNG resolution is 96 dpi.

## Batch over a folder

```bash
for f in assets/*.svg; do
  inkscape "$f" --export-type=png --export-width=2048 --export-filename="png/$(basename "${f%.svg}").png"
done
```
If `--export-filename` is omitted, the output reuses the input file's name. The Inkscape command-line wiki
shows `--export-type` applied to a list of input files; test on two files first.

## Actions (advanced)

`--actions` calls actions with an optional single parameter; the `export-do` action forces an export at any
point. List all actions with `inkscape --action-list` (very long) and take action names from that list.

## Gotchas

- Text renders with fonts installed on the exporting machine; `--export-text-to-path` converts text to paths for
  PS, EPS, PDF and SVG export.
- `--export-area-page` is the default for SVG, PNG, PDF and PS; `--export-area-drawing` exports the drawing's
  bounding box. Choose deliberately, or sizes vary per asset.

## Verify

Check output pixel sizes with an image tool: all at the expected width; spot-check transparency and an asset with
text.

## Checked

2026-11-01. Confirmed against the Inkscape 1.4.4 man page (mankier.com) and the Inkscape command-line wiki:
`--export-type`, `--export-width`, `--export-filename` (default reuses input name), `--export-dpi` (96 default),
`--export-area-drawing`, `--export-area-page` default, `--export-id`, `--export-id-only`, `--export-plain-svg`,
`--export-text-to-path`, `--export-background`, `--export-background-opacity`, `--actions`, `--action-list`,
`export-do`. Removed: the `select-by-id` / `export-id-only` / `export-filename` action example and chain,
`inkscape.com` on Windows, the 0.92 flags remark, filter rasterisation note, `--export-background-opacity=1`
value, the claim that PNG is transparent by default, and the `magick identify` check.
Method: documentation only; no commands were run.
