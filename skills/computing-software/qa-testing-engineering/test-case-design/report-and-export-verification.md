---
id: computing-software.qa-testing-engineering.test-case-design.report-and-export-verification
name: report-and-export-verification
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [report-testing, export-verification, csv-export, pdf-report, reconciliation]
level: practitioner
status: docs-checked
description: "Verify reports and file exports: reconcile totals against source queries, check filters, sorting, formats, encoding, large volumes and Excel/CSV quirks."
sources:
  - https://www.rfc-editor.org/rfc/rfc4180
  - https://owasp.org/www-community/attacks/CSV_Injection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Report and export verification

**Goal:** the numbers in a report or exported file match the source data for every filter, and the file opens correctly in the tools users use.

## Reconcile numbers
- Write an independent SQL query per report figure from the requirement, then compare totals, counts and group subtotals for several filter combinations (date range edges, empty result, single record).
- Check inclusive vs exclusive date boundaries and the timezone of the cut-off.
- Grand total equals the sum of displayed subtotals (rounding per row vs on the total).

## File format checks
- CSV per RFC 4180: fields with commas, quotes and newlines are quoted, quotes doubled. Open it in the spreadsheet tool users use and check leading zeros, long numbers and dates survive.
- Encoding: open the file in each target consumer and check accented characters survive; decide on a BOM per consumer.
- **CSV injection** (OWASP): a cell starting with `=`, `+`, `-`, `@`, tab or carriage return may be evaluated as a formula by a spreadsheet. OWASP notes the commonly suggested mitigations (prefixing a single quote, wrapping in double quotes) may not be reliable in Excel, so test the real import.
- PDF: page breaks inside tables, repeated headers, embedded fonts, selectable text, accessibility tags if required.
- Excel exports: number cells are numbers not text, correct column types, valid sheet names.

## Volume and performance
Export the maximum row count. Look for silent truncation (spreadsheet row limits), timeouts, and that async exports notify on completion.

## Verify
For three filter sets the export row count and totals equal the SQL oracle, and the file round-trips through the target importer without loss.

## Checked

2026-10-28. Confirmed: RFC 4180 (CSV rules); OWASP CSV Injection page: trigger characters =, +, -, @, tab, carriage return; quote-prefix and double-quote mitigations are noted as unreliable in Excel. Removed: Excel row-limit figure, Excel BOM and leading-zero claims, and the "prefix a quote" fix as a sure mitigation.

Method: documentation only; no commands were run.
