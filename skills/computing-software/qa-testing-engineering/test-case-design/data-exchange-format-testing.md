---
id: computing-software.qa-testing-engineering.test-case-design.data-exchange-format-testing
name: data-exchange-format-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [data-exchange-testing, interoperability-testing, csv, xml, edi, file-import]
level: practitioner
status: docs-checked
description: "Test interoperability of data exchange formats (CSV, XML, JSON, EDI): schema validation, partner sample files, encodings, delimiters and round-trip fidelity."
sources:
  - https://www.rfc-editor.org/rfc/rfc4180
  - https://www.w3.org/TR/xmlschema11-1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data exchange format interoperability testing

**Goal:** files and messages we produce are accepted by partners, and partner files are read without loss.

## Collect the contract
Schema (XSD, JSON Schema), implementation guide (EDI X12/EDIFACT segment usage), and real anonymised sample files from each partner. Samples beat the spec: partners deviate.

## Producer side
- Validate every generated file against the schema in CI (XSD or JSON Schema).
- EDI: run through the partner's or a translator's validator; check envelope control numbers and trailer counts against the partner's implementation guide.
- Round-trip: export, import into the partner tool (or a reference parser), compare field by field.

## Consumer side probes
- Encodings: UTF-8 with and without BOM, Windows-1252, UTF-16.
- Line endings CRLF vs LF; missing trailing newline.
- CSV dialect: delimiter `;` in European locales, quoted fields with embedded delimiters and newlines, header row present/absent, extra columns, reordered columns.
- Numbers and dates in locale formats (`1.234,56`, `03/04/2026`).
- XML namespaces and prefixes differing, optional elements absent, unknown elements present (should be ignored rather than fail).
- Empty file, header-only file, very large file, duplicate records.

## Verify
Every partner sample imports with zero unexpected rejects, generated files pass schema validation, and a round-trip leaves values unchanged.

## Checked

2026-10-28. Confirmed: RFC 4180: records end with CRLF, the last record may omit it, an optional header line may appear first. Removed: The xmllint and ajv commands and the EDI ISA/GS envelope detail (not in the sources).

Method: documentation only; no commands were run.
