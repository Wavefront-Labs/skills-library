---
id: computing-software.general-digital-literacy.office-suites.spreadsheet-text-functions
name: spreadsheet-text-functions
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, formulas, functions, text-functions, concat, textsplit, trim]
level: practitioner
status: docs-checked
description: "Clean and combine text in Excel and Google Sheets with TRIM, PROPER, LEFT, RIGHT, MID, LEN, FIND, CONCAT, TEXTJOIN, TEXTSPLIT, SUBSTITUTE and TEXT."
sources:
  - https://support.microsoft.com/en-us/office/textjoin-function-357b449a-ec91-49d0-80c3-0e8fc845691c
  - https://support.microsoft.com/en-us/excel/functions/textsplit-function
  - https://support.microsoft.com/en-us/excel/functions/trim-function
  - https://support.microsoft.com/en-us/excel/functions/search-function
  - https://support.google.com/docs/table/25273
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/01/func_textbefore.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Text functions

## Combine
- `=A2&" "&B2` or `=CONCAT(A2," ",B2)` gives "Sam Lee".
- `=TEXTJOIN(", ",TRUE,A2:A10)` joins a range; TRUE for the second argument ignores empty cells
  (Excel 2019 and later).
- Numbers keep formatting only via `TEXT`: `="Due "&TEXT(C2,"d mmm yyyy")`,
  `=TEXT(D2,"£#,##0.00")`.

## Split and extract
- `=LEFT(A2,3)`, `=RIGHT(A2,4)`, `=MID(A2,5,2)` (start, length).
- First name: `=LEFT(A2,FIND(" ",A2)-1)`; `=TEXTBEFORE(A2," ")` / `=TEXTAFTER(A2," ")` also exist in
  LibreOffice 25.8+.
- `=TEXTSPLIT(A2,",")` spills parts into columns (Microsoft 365, Excel 2024, LibreOffice 25.8+);
  Sheets: `=SPLIT(A2,",")`.
- `=LEN(A2)` counts characters (use to spot trailing spaces).

## Clean
- `=TRIM(A2)` removes extra spaces but not the non-breaking space CHAR(160) common in web data:
  `=TRIM(SUBSTITUTE(A2,CHAR(160)," "))`.
- `=CLEAN(A2)` strips the first 32 non-printing characters (codes 0-31).
- `=PROPER(A2)`, `=UPPER()`, `=LOWER()` fix case.
- `=SUBSTITUTE(A2,"-","")` removes dashes; `=VALUE(A2)` turns "123" text into a number.

## Workflow
Build the formula in a helper column, fill down, then copy, Paste Special, Values over the
original and delete the helper.

## Gotchas
- FIND is case-sensitive (and takes no wildcards); SEARCH is not.
- TEXTBEFORE, TEXTAFTER and TEXTSPLIT are not in the Google Sheets function list; use SPLIT or
  REGEXEXTRACT there.

## Verify
- [ ] `=LEN()` of cleaned values matches what you see; no stray spaces.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft TEXTJOIN (Excel 2019 and later, ignore_empty), TEXTSPLIT (Microsoft 365 and Excel 2024), TRIM and cleaning guidance (TRIM does not remove character 160; CLEAN covers codes 0-31), FIND vs SEARCH (case sensitivity); Google Sheets function list (TEXTJOIN, CONCAT, SPLIT, REGEXEXTRACT present; TEXTBEFORE, TEXTAFTER, TEXTSPLIT absent); LibreOffice help source (TEXTBEFORE, TEXTSPLIT from 25.8).
Method: documentation only; no commands were run.
