---
id: computing-software.general-digital-literacy.office-suites.basic-spreadsheet-formulas
name: basic-spreadsheet-formulas
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, formulas, basic-formulas, operator-precedence, arithmetic, percentage-formula, formula-bar, show-formulas]
level: intro
status: docs-checked
description: "Write spreadsheet formulas with + - * / ^, operator precedence and brackets, percentages and cell references in Excel, Google Sheets and LibreOffice Calc."
sources:
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/office/display-or-hide-formulas-f7f5ab4e-bf24-4efc-8fc9-0c1b77a5356f
  - https://support.microsoft.com/en-us/office/set-rounding-precision-e5d707e3-07a8-4df2-810c-218c531eb06a
  - https://support.microsoft.com/en-us/excel/functions/round-function
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Basic spreadsheet formulas

**Goal:** calculate with cell references so results update when data changes.

## Rules
- A formula starts with `=`. Refer to cells, not typed numbers: `=B2*C2`, not `=12*3.5`.
- Operators: `+ - * /`, `^` power, `&` joins text (`=A2&" "&B2`).
- **Precedence:** brackets, then `^`, then `* /`, then `+ -`. `=10+5*2` is 20; `=(10+5)*2` is 30.
- Point and click: type `=`, click a cell, type an operator, click the next cell, `Enter`.

## Everyday formulas
| Need | Formula |
|---|---|
| Line total | `=B2*C2` |
| Add VAT 20% | `=B2*1.2` or `=B2*(1+$F$1)` with the rate in F1 |
| Percentage of total | `=B2/B$10` then format as % |
| Percentage change | `=(C2-B2)/B2` |
| Days between dates | `=C2-B2` |

## Check your work
- The **formula bar** shows the formula behind the selected cell.
- Show all formulas in Excel: `Ctrl+`` (grave accent) or Formulas › Show Formulas.
- `F2` edits the active cell.

## Gotchas
- A number stored as text is ignored by maths; convert it with `=VALUE(A2)`.
- Rounding: the display rounds, the stored value doesn't. Use `=ROUND(B2*C2,2)` for money that must
  add up exactly.

## Verify
- [ ] Change an input: every dependent result updates.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft display-or-hide-formulas page (Ctrl+` and Formulas, Show Formulas), keyboard shortcuts (F2 edits the active cell), Set rounding precision (display formatting does not change the stored value; use ROUND). Arithmetic precedence examples computed by hand.
Method: documentation only; no commands were run.
