---
id: computing-software.general-digital-literacy.office-suites.round-function-and-rounding
name: round-function-and-rounding
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, formulas, functions, round-function, roundup, mround, decimal-places]
level: intro
status: docs-checked
description: "Round numbers properly in Excel and Google Sheets with ROUND, ROUNDUP, ROUNDDOWN, MROUND, CEILING and INT, versus only formatting fewer decimals."
sources:
  - https://support.microsoft.com/en-us/office/round-function-c018c5d8-40fb-4053-90b1-b3e7f61a213c
  - https://support.microsoft.com/en-us/excel/functions/mround-function
  - https://support.microsoft.com/en-us/excel/functions/trunc-function
  - https://support.microsoft.com/en-us/office/set-rounding-precision-e5d707e3-07a8-4df2-810c-218c531eb06a
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ROUND and rounding

**Key idea:** *Decrease Decimal* (formatting) hides digits but calculations still use the full value;
`ROUND` changes the value itself.

| Formula | 2.345 → | Use |
|---|---|---|
| `=ROUND(A2,2)` | 2.35 | Money, reporting |
| `=ROUNDUP(A2,0)` | 3 | Boxes needed, never under-order |
| `=ROUNDDOWN(A2,1)` | 2.3 | Completed units |
| `=ROUND(A2,-2)` on 1,234 | 1,200 | Round to hundreds (negative digits count left of the point) |
| `=MROUND(A2,0.05)` | 2.35 | Nearest 5p/5c |
| `=CEILING(A2,0.25)` | 2.5 | Up to nearest quarter hour |
| `=FLOOR(A2,0.25)` | 2.25 | Down |
| `=INT(A2)` | 2 | Drop decimals (negatives go down: INT(-4.3) = -5) |
| `=TRUNC(A2)` | 2 | Drop decimals toward zero (TRUNC(-4.3) = -4) |

## When to round
- Round each line when the business rounds per line (invoice VAT per item), then sum.
- Otherwise sum unrounded values and round the total; "totals don't add up by 1p" is the classic
  symptom of mixing the two.

## Gotchas
- Excel's *Set precision as displayed* option (File › Options › Advanced) permanently changes stored
  values to the displayed precision and cannot be undone; use ROUND instead.
- Microsoft's ROUND examples show halves rounding away from zero (ROUND(2.15,1) is 2.2,
  ROUND(-1.475,2) is -1.48).
- MROUND with decimal multiples can give surprising results at exact midpoints (Microsoft's
  example: MROUND(6.05,0.1) is 6.0 but MROUND(7.05,0.1) is 7.1).

## Verify
- [ ] Sum of rounded lines vs rounded total: difference explained and acceptable.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft ROUND page (num_digits below 0 rounds left of the decimal point; examples round halves away from zero), MROUND, CEILING, FLOOR, TRUNC and INT pages (TRUNC(-4.3) = -4, INT(-4.3) = -5), Set rounding precision (Set precision as displayed is under File, Options, Advanced and permanently changes stored values to the displayed precision).
Method: documentation only; no commands were run.
