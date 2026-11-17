---
id: computing-software.qa-testing-engineering.exploratory-testing.test-idea-heuristics
name: test-idea-heuristics
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [test-ideas-heuristics, test-heuristics, goldilocks, zero-one-many, crud, exploratory-testing]
level: practitioner
status: draft
description: "Generate test ideas fast with heuristics: Goldilocks, zero-one-many, CRUD, boundaries, interruptions, Some-None-All, beginning-middle-end, and the Test Heuristics Cheat Sheet."
sources:
  - https://testobsessed.com/
  - https://www.satisfice.com/rapid-testing-methodology
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test idea heuristics

**Goal:** never stare at a feature wondering what to try; apply quick heuristics to generate varied, high-yield test ideas (Elisabeth Hendrickson's Test Heuristics Cheat Sheet and RST practice).

## Data heuristics
- **Goldilocks:** too small, too big, just right (file sizes, text lengths, amounts).
- **Zero, One, Many:** no items, one item, lots of items (cart, search results, attachments). Includes pluralisation and pagination.
- **Some, None, All:** select some, none, all (filters, permissions, checkboxes).
- **Boundaries:** at, just below, just above limits; also implicit ones (32-bit int, date range limits).
- **Beginning, Middle, End:** position of an item in a list or text (delete first/last row, cursor at start/end).
- **Violate data types and formats:** letters in numbers, unicode, emoji, leading/trailing spaces, very long words.

## Action heuristics
- **CRUD:** create, read, update, delete every entity; then repeat in different orders and concurrently.
- **Interrupt:** cancel, back button, refresh, close tab, lose network, lock screen mid-operation.
- **Repeat and rapid fire:** double-click submit, rapid toggles, same request twice.
- **Undo/redo and navigation:** browser history, deep links, bookmarks to states that no longer exist.
- **Follow the data:** enter it, then see where else it appears (reports, emails, exports).
- **Configurations:** permissions, locale, timezone, feature flags, screen size.

## Use
Pick 3-5 heuristics per session charter; note which you applied so coverage is explainable.

## Verify
Session notes list the heuristics used per charter, and bugs found can be traced back to the heuristic that produced them.
