---
id: computing-software.rpa-and-low-code.uipath.uipath-excel-read-write-range
name: uipath-excel-read-write-range
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-excel-read-write-range]
level: practitioner
status: draft
description: "Use workbook activities appropriately."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Read and write Excel at scale
**Goal:** Use workbook activities appropriately.

- Excel Application Scope (classic) and Use Excel File (modern) with Read Range and Write Range; Workbook activities work without Excel installed.
- Specify header handling and use AddHeaders option.
- Close Excel processes in exception handling.

## Gotchas
- Orphaned Excel processes block unattended runs; kill in finally.

## Self-check
Output file opens and shows the data.
