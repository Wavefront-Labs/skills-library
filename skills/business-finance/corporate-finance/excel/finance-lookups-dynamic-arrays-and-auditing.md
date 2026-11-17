---
id: business-finance.corporate-finance.excel.finance-lookups-dynamic-arrays-and-auditing
name: finance-lookups-dynamic-arrays-and-auditing
category: business-finance
field: corporate-finance
product: excel
tags: [excel, microsoft-excel, spreadsheet, xlookup, sumifs, dynamic-arrays, filter, let, spill, spreadsheet-auditing, financial-modelling]
level: practitioner
status: docs-checked
description: "Excel for finance work: XLOOKUP, SUMIFS, FILTER and LET, and a spreadsheet audit routine built on independent recomputation and consistency checks."
sources:
  - https://support.microsoft.com/en-us/office/xlookup-function-b7fd680e-6d10-43e6-84f9-88eae8bf5929
  - https://support.microsoft.com/en-us/office/filter-function-f4f7cb66-82eb-4767-8f7c-4877ad80c759
  - https://support.microsoft.com/en-us/office/let-function-34842dd8-b92b-4d3f-b325-b8b8f9908999
  - https://support.microsoft.com/en-us/office/sumifs-function-c9e748f5-7ea7-455d-9406-611cebce642b
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finance lookups, dynamic arrays and spreadsheet auditing in Excel

**Goal:** write formulas that survive inserted columns and new data, and audit a workbook (yours or someone else's)
systematically. XLOOKUP, FILTER and LET are listed for Microsoft 365 and Excel 2021 or later; check the function's
Microsoft page for older versions before sharing a model.

## 1. Lookups
- **`XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])`**: match mode
  defaults to exact; `if_not_found` returns text you supply instead of `#N/A`; the return column can be on either
  side of the lookup column.
- Prefer lookups that reference the key by column rather than a hard-coded column index, so inserted columns do
  not break them.
- **Duplicates:** check that the key is unique (for example with `COUNTIFS`) before trusting a lookup on a key
  you did not create.

## 2. Aggregation
- **`SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...)`**: the sum range comes
  first, then range and criteria pairs. Operators go inside the criteria text, for example `"<>Bananas"`.
- Store dates as real dates, not text.

## 3. Dynamic arrays and LET
- **`FILTER(array, include, [if_empty])`**: `include` is a Boolean array the same height or width as `array`.
  Without `if_empty`, no matches return `#CALC!`. When FILTER is the final result of a formula it spills into
  neighbouring cells.
- **`LET(name1, name_value1, calculation_or_name2, ...)`** names intermediate results; Excel calculates a named
  expression once instead of each time it is written. The final argument must be a calculation.

## 4. Structure that prevents errors
- Inputs in one place; no hard-coded numbers inside formulas.
- Source data in a consistent table layout so ranges grow with the data.
- Pivot tables for exploration; SUMIFS for reported numbers that must stay stable.

## 5. Audit routine for an inherited workbook
1. **Map it:** list sheets, named ranges, external links, hidden sheets and rows.
2. Scan formulas row by row for one that changes mid-row; look for hard-coded constants inside calculation areas.
3. Trace precedents and dependents of the key outputs, and step through complex formulas.
4. Check for error values, inconsistent formulas and circular references.
5. Recompute key totals independently (a quick SUMIFS or pivot) and compare.

## Gotchas
- Numbers stored as text are ignored by SUM and break lookups.
- Manual calculation mode makes stale numbers.
- Floating-point: round in equality checks.
- Merged cells break sorting, filtering and copying.

## Verify
- [ ] Lookup keys checked for duplicates.
- [ ] No hard-codes in calc areas.
- [ ] Calculation mode Automatic; no unintended circular references or broken links.
- [ ] Key outputs re-derived independently and match.

## Checked

2026-11-01. Confirmed on the Microsoft Support pages for XLOOKUP, FILTER, LET and SUMIFS: syntax, XLOOKUP exact
default and `if_not_found`, left lookup, FILTER `if_empty` / `#CALC!` / spill, LET calculate-once, SUMIFS argument
order and operator criteria, and availability in Microsoft 365 and Excel 2021. Removed because not confirmed from
those pages: VLOOKUP default-match and hard-coded-index claims, INDEX/MATCH, two-key XLOOKUP formula, `#SPILL!`
and `A2#`, UNIQUE/SORT/SORTBY/SEQUENCE, EOMONTH/EDATE/NETWORKDAYS, Power Query, keyboard shortcuts and menu paths,
the Inquire add-in, and the `0.1+0.2` example.
Method: documentation only; no commands were run.
