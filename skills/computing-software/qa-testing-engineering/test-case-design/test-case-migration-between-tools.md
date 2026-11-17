---
id: computing-software.qa-testing-engineering.test-case-design.test-case-migration-between-tools
name: test-case-migration-between-tools
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-case-migration, test-management-tools, testrail, xray, zephyr, data-migration]
level: practitioner
status: draft
description: "Migrate test cases between test management tools (e.g. TestRail to Xray): inventory, field mapping, cleanup, CSV/API import, history decisions and verification."
sources:
  - https://docs.getxray.app/
  - https://support.testrail.com/
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migrating test cases between tools

**Goal:** move the test repository to a new tool without losing structure, traceability or trust, and without carrying junk across.

## Plan
1. **Inventory:** count cases per area, last executed date, automation status, attachments, custom fields, shared steps.
2. **Clean up first:** archive cases not run in 12+ months or obsolete; merge duplicates. Migration is the cheapest moment to prune.
3. **Decide on history:** usually migrate cases and the latest results only; archive old runs as exports (CSV/PDF) for audit rather than importing them.
4. **Field mapping sheet:** source field, target field, transformation (TestRail sections to Xray test repository folders, priority values, custom fields, references to Jira requirement links, separated steps to Xray manual steps).

## Execute
- Export: TestRail CSV/XML export or API (`get_cases`); Zephyr/Xray via REST.
- Transform with a script (Python/pandas) to the target import format: Xray Test Case Importer CSV, or Xray REST `import/test/bulk` (cloud).
- Shared steps: expand or map to call-test/precondition features.
- Attachments: separate API upload step; check size limits.
- Automated tests: re-link by key or name to the new tool (Xray test keys in JUnit or Cucumber tags).
- Pilot with one area, review with its owners, then run in batches.

## Verify
Counts per folder match after cleanup, a random sample of 30 cases matches field by field including steps and links, requirement coverage reports show equivalent coverage, and automation results land on the right cases.
