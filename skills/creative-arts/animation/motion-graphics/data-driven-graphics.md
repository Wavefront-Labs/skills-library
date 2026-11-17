---
id: creative-arts.animation.motion-graphics.data-driven-graphics
name: data-driven-graphics
category: creative-arts
field: animation
product: motion-graphics
tags: [data-driven-graphics, motion-templates, csv, json, after-effects, footage-sourcedata, datakeys, infographics, versioning-at-scale]
level: advanced
status: draft
description: "Drive After Effects graphics from CSV/JSON data: importing data as footage, reading values in expressions, and batch-rendering versions from a spreadsheet."
sources:
  - https://helpx.adobe.com/after-effects/using/data-driven-animation.html
  - https://ae-expressions.docsforadobe.dev/
  - https://ae-scripting.docsforadobe.dev/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data-driven graphics

**Goal:** charts, scoreboards, cast name cards or localised titles generated from a spreadsheet, so a
data change updates every graphic and 200 versions render without manual edits.

## Import data

AE imports `.csv`, `.tsv` and `.json` as footage. Drag into a comp to use as a data layer, or
reference it in expressions directly via `footage()`.

CSV `cast.csv`:
```
name,role,colour
Ana Ruiz,Director,#E85D3A
Lee Park,Producer,#3A8FE8
```

## Read values in expressions

```javascript
// Source Text: row index from a slider on a control layer
var row = Math.round(thisComp.layer("CTRL").effect("Row")("Slider"));
footage("cast.csv").dataValue([0, row]);      // column 0, row n
```
JSON:
```javascript
var d = footage("stats.json").sourceData;   // parsed object
d.teams[0].score;
```
Colour from hex: `hexToRgb(footage("cast.csv").dataValue([2,row]))` on a Fill Color property.

## Batch versions

1. Build one comp reading row N from the CTRL slider.
2. Script (ExtendScript) that loops rows: duplicate the comp or set the slider, add to the Render
   Queue with an output name from the data (`Ana_Ruiz_namecard.mov`), then render.
3. Or render via `aerender` per comp on the farm (`creative-arts.animation.scripting.aerender-cli`).
For Premiere workflows, a mogrt with exposed text plus a CSV merge plugin, or Premiere's own
spreadsheet-driven workflows, do the same on the edit side.

## Gotchas

- Changing the data file outside AE: use File - Reload Footage; expressions read the cached data.
- CSV parsing is simple: commas inside fields must be quoted; non-ASCII names need UTF-8 encoding.
- Data indexing is zero-based in `dataValue([column,row])` with the header excluded; check with a
  test row.

## Verify

Edit one value in the CSV, reload, and confirm the matching graphic updates; batch render 3 rows and
check names and colours against the sheet.
