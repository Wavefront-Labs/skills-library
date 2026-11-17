---
id: computing-software.qa-testing-engineering.test-case-design.test-case-structure-and-naming
name: test-case-structure-and-naming
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-case-structure, test-case-naming, test-case-design, test-management-tools, testrail]
level: practitioner
status: draft
description: "Structure and name test cases consistently in a test management tool: folder hierarchy, title pattern, preconditions, steps vs scenario style, data and traceability fields."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://support.testrail.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test case structure and naming conventions

**Goal:** a test repository people can search, maintain and run, instead of thousands of inconsistent cases nobody trusts.

## Hierarchy
Organise folders/sections by **product area or feature**, not by sprint or release (sprints end, features stay). Use runs/plans/test sets for releases. Two to three levels deep at most.

## Title pattern
`<Feature> - <condition or rule> - <expected outcome>`, e.g. `Checkout - expired card - payment declined with retry option`. Searchable, unique, says what it proves. Avoid "Test 1", "Verify checkout works".

## Fields
- **Preconditions:** state and data required (user role, feature flag, existing order).
- **Steps with expected results,** or a single scenario/charter text for exploratory or BDD-style cases. Choose per case type, and agree team-wide.
- **Test data:** reference a data set or describe the data class; avoid hard-coded IDs that expire.
- **References:** requirement/story IDs and risk IDs for traceability.
- **Priority** (for regression selection), **type** (functional, regression, smoke), **automation status** (manual, automated, candidate) with automated test ID.
- **Owner** and last reviewed date.

## Writing rules
- One objective per case; split long cases at natural checkpoints.
- Steps at the level a new team member can follow, without UI micro-detail that breaks on every redesign ("log in as admin" rather than every click).
- Expected results observable and specific.

## Maintenance
Review cases touched by each feature change; archive (not delete) obsolete ones; reuse via shared steps for repeated flows.

## Verify
A sample of 20 cases follows the title pattern and has references and priority, and a new tester can run them without asking questions.
