---
id: computing-software.data-engineering.data-quality.dq-assessment-and-baselining
name: dq-assessment-and-baselining
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, dq-assessment, profiling, baselining, critical-data-elements]
level: advanced
status: draft
description: "Run a data quality assessment: scope critical data elements, profile, measure per dimension, establish baselines, find root causes and report results to owners."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://books.google.com/books?vid=ISBN9780128180150
  - https://docs.soda.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DQ assessment and baselining

**Goal:** an evidence-based picture of current data quality for important data, used as the baseline for improvement targets.

## 1. Scope
- Pick a business process (order-to-cash, customer onboarding) and its **critical data elements** (CDEs): the few dozen fields that drive decisions, money or compliance.
- Identify system of record, owners and consumers for each.

## 2. Profile
Per CDE: row counts, null/blank rates, distinct counts, patterns (regex classes for emails, phones, IDs), min/max/outliers, value frequency, cross-field consistency, duplicates on business keys, orphan references. Tools: SQL, ydata-profiling, Soda/GX profiling, warehouse data metric functions.

## 3. Measure against dimensions
| Dimension | Example metric |
|---|---|
| Completeness | % rows with non-null `tax_id` for business customers |
| Validity | % emails matching format and domain MX |
| Uniqueness | duplicate customer records per 1,000 |
| Consistency | % orders where country matches billing address country |
| Accuracy | % sampled records matching an authoritative source |
| Timeliness | lag between event and availability |
Accuracy usually needs sampling against a reference (manual verification of 200 random records).

## 4. Baseline
Store results with date and method, per CDE and dimension: this is the baseline. Repeat with the same queries later (automate them as DQ checks).

## 5. Root causes
For the worst gaps: interview data entry owners, inspect forms/integrations; classify causes (no validation at entry, integration mapping error, missing reference data, process gap).

## 6. Report
Scorecard per CDE (current vs proposed target), top issues with impact, recommended fixes and owners. Keep it short; attach query details.

## Verify
Assessment queries are saved and re-runnable, and the baseline numbers are reproducible by someone else.
