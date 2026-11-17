---
id: computing-software.general-digital-literacy.office-suites.xlookup-and-vlookup
name: xlookup-and-vlookup
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, functions, xlookup, vlookup, lookup-functions, index-match, exact-match, na-error]
level: intro
status: docs-checked
description: "Look up a value in another table with XLOOKUP or VLOOKUP (exact match), avoid the classic VLOOKUP mistakes and handle not-found results."
sources:
  - https://support.microsoft.com/en-us/office/xlookup-function-b7fd680e-6d10-43e6-84f9-88eae8bf5929
  - https://support.microsoft.com/en-us/office/vlookup-function-0bbc8083-26fe-4963-8ab8-93a18ad188a1
  - https://support.microsoft.com/en-us/excel/functions/ifna-function
  - https://support.google.com/docs/table/25273
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/01/func_xlookup.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# XLOOKUP and VLOOKUP

**Goal:** pull a price, name or code from a reference table by its key.

## XLOOKUP (Excel 365/2021/2024, Google Sheets, LibreOffice 24.8+; not in Excel 2016 or 2019)
`=XLOOKUP(A2, Products!A:A, Products!C:C, "Not found")`
= find A2 in column A of Products, return the matching value from column C, show "Not found"
otherwise. Exact match by default (match_mode 0); without the fourth argument a miss gives `#N/A`.
The lookup and return ranges are separate arguments, so the key need not be in the first column.

## VLOOKUP (works everywhere)
`=VLOOKUP(A2, Products!$A$2:$D$500, 3, FALSE)`
- 2nd argument: the table, **key in its first column**. Lock it with `$` before filling down.
- 3rd: which column of the table to return (3 = the third column of the range).
- 4th: **FALSE** (or 0) for exact match. If you leave it out the default is TRUE, an approximate
  match, which needs sorted data and can return wrong answers silently.

## Not found
`#N/A` means the key isn't there. Wrap: `=IFNA(VLOOKUP(...),"Not found")`. Common causes:
- Trailing spaces (`"AB12 "`): clean with `=TRIM()`.
- Number vs text (`123` vs `'123`): convert one side (`=VALUE()` or `=TEXT()`).

## Gotchas
- VLOOKUP's column number is hard-coded; inserting a column in the table shifts results. Prefer
  XLOOKUP or `INDEX(C:C, MATCH(A2, A:A, 0))`.
- Duplicate keys: only the first match is returned. Check with `COUNTIF(A:A,A2)>1`.

## Verify
- [ ] Manually check three looked-up values, including the last row of the table.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft XLOOKUP and VLOOKUP pages (Excel 365, 2021, 2024; XLOOKUP not in 2016 or 2019; XLOOKUP match_mode default 0 exact, if_not_found default #N/A; VLOOKUP range_lookup defaults to approximate, lookup value must be in the first column), IFNA page (added in Excel 2013), Google Sheets function list (XLOOKUP, IFNA present), LibreOffice help source func_xlookup.xhp (available from 24.8).
Method: documentation only; no commands were run.
