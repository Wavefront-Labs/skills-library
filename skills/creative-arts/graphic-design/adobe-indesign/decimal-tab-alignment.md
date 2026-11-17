---
id: creative-arts.graphic-design.adobe-indesign.decimal-tab-alignment
name: decimal-tab-alignment
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-tables, decimal-tab-alignment, align-on-decimal, tabs-panel, tabular-lining-numerals, figure-space, financial-tables, number-alignment]
level: practitioner
status: draft
description: "Align numbers in InDesign tables and tabbed text on the decimal point: Align to Decimal tabs in cells, tabular figures, figure spaces, negative numbers and currency."
sources:
  - https://helpx.adobe.com/indesign/using/tabs-indents.html
  - https://helpx.adobe.com/indesign/using/formatting-tables.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aligning numbers on decimal tabs

**Goal:** columns of figures where units, tens and decimals line up so readers can compare at a glance.

## Use tabular figures first
Proportional figures (often default in text faces) have different widths; even right-aligned columns wobble.
Apply **tabular lining figures** (OpenType `tnum` + `lnum`) in the table paragraph style (see figures skill).

## In table cells
1. Select the column cells. Open Tabs panel (Shift+Ctrl/Cmd+T); click the magnet to align it to the frame.
2. Choose **Align to Decimal** tab (fourth icon); set "Align On" character - `.` or `,` for European decimals.
3. Click on the ruler to place the tab within the cell.
4. A decimal tab stop in the cell's paragraph aligns the number without typing a tab character (Adobe:
   "you don't usually need to press Tab"). To insert a literal tab inside a cell use Type > Insert Special
   Character > Other > Tab. Put the tab stop in the table-number paragraph style so it applies to all cells.
Alternative: right-align cells when all numbers have the same decimal places - simpler and equally neat.

## Tabbed (non-table) text
Price lists and menus: Text `Item^tPrice`; set a right or decimal tab with an optional leader (`. `) at the right edge.

## Tricky cases
- **Negative numbers in parentheses** (accounting): `(1,234)` vs `1,234` - add a **figure space** or a punctuation
  space after positive numbers so digits align with the closing parenthesis; or align on decimal with a
  hidden decimal.
- **Minus signs:** use the true minus (U+2212), the same width as plus in most fonts.
- **Currency symbols:** put them in the column header (`EUR m`) rather than every cell, or align them with a tab.
- **Footnote markers** after figures push alignment - use superscript markers in a separate tab position or hang them.

## Verify
- [ ] Decimal points align vertically in every numeric column at 400% zoom.
- [ ] Tabular figures active; negatives and totals align with other rows.
