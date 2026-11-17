---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.new-comic-file-settings-bleed-trim-base-frame
name: new-comic-file-settings-bleed-trim-base-frame
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-comic-project, csp-page-management, csp-new-comic-settings, bleed, trim, base-frame, binding, expression-color]
level: practitioner
status: draft
description: "Create a comic file in Clip Studio Paint with correct finished (trim) size, bleed, base frame, resolution, expression colour, binding side and page count, and save it as a preset."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://www.clipstudio.net/en/functions/
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# New comic file settings: bleed, trim, base frame

**Goal:** a CSP comic file whose guides match the printer/publisher spec from page one.

## File > New, choose the comic use type
Key fields (names per the CSP user guide; layout differs slightly by version):
| Field | Set to |
|---|---|
| Finished size (canvas/trim) | the trim, e.g. 6.625 x 10.25 in for US comics, B5/A4 etc. |
| Bleed width | printer spec, e.g. 0.125 in / 3 mm (manga manuscripts often 3-5 mm) |
| Base frame (inner frame) | the live/safe panel area; panels and text inside it |
| Resolution | 600 dpi for monochrome/line art (some use 1200); 350-600 for colour |
| Basic expression colour | Monochrome (B/W with tones), Gray, or Color, per output |
| Binding point | Left binding (Western) or Right binding (manga) |
| Start page / spreads | whether page 1 starts left or right; enable spread handling if needed |
| Multiple pages | number of pages for a story file (page counts above a small limit need the EX edition) |
| Story info / page numbers | title, author, page number (nombre) display if wanted |

## Why expression colour matters
Monochrome files output true black-and-white with tones as dots; Gray/Color keep
greys. Pick Monochrome for traditional manga/B&W print, Color for colour books.

## Save a preset
After filling in, register the settings as a preset (the preset button in the New
dialog) named for the publisher format, e.g. "US comic 6.625x10.25 bleed 0.125".

## Gotchas
- Setting the canvas to trim + bleed manually as finished size doubles the bleed.
- 350 dpi monochrome output can render tones and thin lines badly; use 600+.
- Binding set wrong reverses spreads in the page manager.

## Verify
- [ ] Trim, bleed and base frame guides match the spec sheet numbers.
- [ ] Binding and start page correct; preset saved.
