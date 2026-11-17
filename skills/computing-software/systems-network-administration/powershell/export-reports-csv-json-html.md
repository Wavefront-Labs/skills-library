---
id: computing-software.systems-network-administration.powershell.export-reports-csv-json-html
name: export-reports-csv-json-html
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-pipeline, export-csv, convertto-json, convertto-html, import-csv, reporting, encoding, csv-import-parsing]
level: practitioner
status: gated
description: "Export PowerShell objects to CSV, JSON and HTML reports that open correctly: encoding, -Depth, flattening arrays, Excel delimiters and an HTML email body."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/export-csv
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertto-json
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/convertto-html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Export reports to CSV, JSON and HTML

Always `Select-Object` the exact columns first: exports serialise every property, and
nested objects become type names like `System.Object[]`.

## CSV
```powershell
$rows | Select-Object Name, Enabled, @{n='Groups'; e={$_.MemberOf -join ';'}} |
  Export-Csv report.csv -NoTypeInformation -Encoding UTF8
```
- Windows PowerShell 5.1 writes a `#TYPE` header unless `-NoTypeInformation`, and defaults
  to ASCII (`José` came out as `Jos?`, byte 3F); `-Encoding UTF8` there adds a BOM (EF BB BF), which Excel needs to show
  accents (gated: unconfirmed, source is paywalled or blocked). PS 7
  defaults to UTF-8 without BOM and no type header (`-Encoding UTF8` is also BOM-less there); `-Encoding utf8BOM` writes
  the BOM and does not exist in 5.1.
- Join arrays into one string; otherwise the cell shows `System.Object[]`.
- Regional Excel that expects `;` delimiters: `-UseCulture` or `-Delimiter ';'`.
- `-Append` requires matching columns: a mismatch is an error naming the missing column; `-Force` appends anyway,
  keeping the file's original header and leaving blanks.
- `-UseQuotes AsNeeded` (PS 7 only) stops quoting every field.
- `Import-Csv` returns every value as a **string**; cast before comparing numbers.

## JSON
```powershell
Get-Service | Select-Object Name, Status, StartType |
  ConvertTo-Json -Depth 5 | Set-Content services.json -Encoding UTF8
```
- Default `-Depth` is 2: deeper objects are flattened to strings (`System.Collections.Hashtable`); PS 7.6.7 prints
  `Resulting JSON is truncated as serialization has exceeded the set depth of 2`, 5.1 is silent. Set it.
- Enums serialise as numbers (`Status` became `1`); add `-EnumsAsStrings` (PS 7 only) or cast to string in `Select-Object`.
- A single object becomes a JSON object, not an array. Force an array with
  `ConvertTo-Json -InputObject @($rows)` or `-AsArray` (PS 7).
- `-Compress` gives one-line output for APIs and logs.

## HTML report / email body
```powershell
$css  = '<style>table{border-collapse:collapse;font-family:Segoe UI}td,th{border:1px solid #ccc;padding:4px}</style>'
$body = $rows | Select-Object Name, FreePct |
  ConvertTo-Html -Head $css -PreContent "<h2>Low disk $(Get-Date -Format yyyy-MM-dd)</h2>" | Out-String
```
- `-Fragment` emits just the `<table>` so several tables can be combined into one page.
- Cell values are HTML-encoded automatically; injecting raw HTML into cells needs post-processing.
- `Send-MailMessage` is marked obsolete on its Microsoft Learn page. For Microsoft 365 send the body with Graph
  `Send-MgUserMail` using `-BodyParameter` with `contentType = 'HTML'` (the Learn page has an HTML example; the Graph
  module is not installed here, so it was not run).

## Verify
- [ ] The CSV opens in Excel with correct columns and accented names intact.
- [ ] `Get-Content services.json -Raw | ConvertFrom-Json` round-trips the same count and fields.

## Checked
Ran on 7.6.7 and 5.1.26100: Export-Csv with a calculated `Groups` column, BOM bytes and `#TYPE` header per edition, default
encoding bytes, `System.Object[]` cells without the join, `-Delimiter`, `-UseCulture`, `-Append` with and without `-Force`,
`-UseQuotes AsNeeded` (7 only), `-Encoding utf8BOM` (7 only), Import-Csv string typing, ConvertTo-Json depth/warning,
enum numbers, `-EnumsAsStrings`, one-element array handling, `-AsArray` (7 only), ConvertTo-Html with `-Head`,
`-PreContent`, `-Fragment` and HTML-encoding of cell values. `Send-MailMessage` obsolescence and the `Send-MgUserMail`
`-BodyParameter` HTML example were read on Microsoft Learn. Excel's handling of BOM-less UTF-8 could not be tested (no Excel here).
