---
id: creative-arts.design-for-form-and-experience.figma.figma-export-settings
name: figma-export-settings
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [export-settings, figma-export, slices, png-svg-pdf, export-scales, asset-export, image-export, figma]
level: practitioner
status: docs-checked
description: "Export from Figma correctly: slices, batch export, and the REST images endpoint with its format, scale and SVG options, for dev handoff and production."
sources:
  - https://help.figma.com/hc/en-us/articles/360040028114-Export-from-Figma-Design
  - https://developers.figma.com/docs/rest-api/file-endpoints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Figma export settings

## In the app
- Choose the file format and settings in the **Export** section of the right sidebar (the Help Center links to a separate article listing formats and settings; read it for current options).
- The **Slice** tool (Region tools dropdown) defines an export region: click and drag, then move and resize. Only content inside the slice is exported. Slices give fixed padding, unlike padding computed from shape bounds, which changes when the shape resizes.
- Bulk export shortcut: Shift+Ctrl+E on Windows, Shift+Cmd+E on Mac.
- **Batch export:** Main menu > File > Export lists every selection on the page that has export settings; uncheck what you do not want, then click Export.
- Set export settings on library components (icons, illustrations) so everyone exports the same way.

## REST API: GET /v1/images/:key
- `key` is the file key or branch key; `ids` (required) is a comma-separated list of node IDs.
- `scale`: number from 0.01 to 4. `format`: `jpg`, `png`, `svg` or `pdf`.
- SVG options: `svg_include_id` (default `false`; adds the layer name to each element's `id`), `svg_simplify_stroke` (default `true`).
- `use_absolute_bounds` (default `false`) uses the node's full dimensions, useful for text that would be cropped. `contents_only` (default `true`) excludes content that overlaps the node.
- Images up to 32 megapixels are supported (larger are scaled down); image URLs expire after 30 days; a node that fails to render is `null` in the response.
- Link to automation in CI: `creative-arts.design-for-form-and-experience.figma.figma-rest-api-file-access`.

## Practice (convention)
- Align layers to whole pixels and export from frames of exact size.
- Compress images after export, and optimise SVGs (`creative-arts.design-for-form-and-experience.design-systems.optimising-and-delivering-svg-icon-libraries`).

## Verify
- [ ] Correct format and scale per platform.
- [ ] SVG options appropriate; outputs optimised.
- [ ] Assets named consistently.

## Checked
2026-11-01. Confirmed on the Figma Help Center Export page (slice, shortcut, batch export) and the REST API file endpoints page (images endpoint parameters, limits). Removed: format-by-format advice, scale lists and platform scale tables, suffix rules, SVG outline-text option, Contents-only UI label, JPG quality figure, File > Export frames to PDF, the Assets panel claim, none stated on pages read.
Method: documentation only; no commands were run.
