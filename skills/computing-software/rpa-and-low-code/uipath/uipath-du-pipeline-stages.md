---
id: computing-software.rpa-and-low-code.uipath.uipath-du-pipeline-stages
name: uipath-du-pipeline-stages
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-document-understanding, uipath-du-pipeline-stages]
level: advanced
status: draft
description: "Digitize, classify, extract and validate documents."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build the DU pipeline
**Goal:** Digitize, classify, extract and validate documents.

- Stages: taxonomy, digitize (OCR), classify, extract, validate (human in the loop via Action Center), train and export.
- Use ML models, generative models and rule-based extractors as fits.
- Output to a DataTable or queue.

## Gotchas
- OCR quality drives extraction accuracy; test with real scans.

## Self-check
Sample invoices extract with fields and confidence.
