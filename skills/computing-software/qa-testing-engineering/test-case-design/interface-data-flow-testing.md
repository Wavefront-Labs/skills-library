---
id: computing-software.qa-testing-engineering.test-case-design.interface-data-flow-testing
name: interface-data-flow-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [interface-data-flow-testing, end-to-end-data-flow, data-mapping, integration-testing, istqb-ta]
level: practitioner
status: draft
description: "Trace a business record end to end across interfaces: field mapping sheets, transformation checks, truncation and encoding loss, and reconciliation counts."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# End-to-end data flow and interface testing

**Goal:** a value entered in system A arrives in systems B, C and the report with the right meaning, format and precision.

## Method
1. **Draw the flow:** UI, API, queue, ETL, warehouse, report. Name each hop's format (JSON, CSV, DB column).
2. **Mapping sheet** per hop: source field, target field, type, length, transformation, default, nullability. Most defects sit where the sheet says "TBD".
3. **Trace records:** create records with recognisable marker values (`QA-TRACE-0001`) and follow each through every hop with queries.
4. **Probe the conversion risks per field:**
   - Length: 255-char name into a VARCHAR(100) target: truncated silently or rejected?
   - Encoding: `Zoë Ünal 李` and emoji; look for `?` or mojibake (`Ã«`).
   - Precision: 10.005 through float hops; dates with timezones (23:30 local on the last day of a month).
   - Null vs empty string vs missing key.
   - Enumerations: a new value added in A that B's mapping does not know.
5. **Reconcile volumes:** row counts and sums of amounts per batch at each hop. Record rejects with reasons.

## Gotchas
- Asynchronous hops: poll with timeout, never fixed sleeps.
- Test the error path: what happens to a record B rejects, is it retried, dead-lettered or lost?

## Verify
Every mapped field has one trace record checked at every hop, and counts and sums reconcile for a full batch.
