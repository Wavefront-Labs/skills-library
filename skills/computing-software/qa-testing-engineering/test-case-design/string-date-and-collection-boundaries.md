---
id: computing-software.qa-testing-engineering.test-case-design.string-date-and-collection-boundaries
name: string-date-and-collection-boundaries
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [string-length-boundaries, date-boundaries, boundary-value-analysis, collection-size-boundaries, leap-year, timezone-boundaries]
level: practitioner
status: draft
description: "Apply boundary analysis to non-numeric inputs: string lengths, dates and times (month ends, leap years, DST), collection sizes, file sizes and pagination."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.iana.org/time-zones
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Boundaries on strings, dates and collections

**Goal:** find the boundaries that are not written as numbers in the spec.

## Strings
- Length: 0 (empty), 1, max-1, max, max+1. Field "1-50 characters" -> test 0, 1, 50, 51 (+2 and 49 for 3-value).
- Length in what unit? Bytes vs characters vs UTF-16 code units: a 50-char limit with emoji (`😀` is 1 grapheme, 2 UTF-16 units, 4 UTF-8 bytes) or combining accents breaks DB columns sized in bytes.
- Leading/trailing whitespace counted or trimmed?

## Dates and times
- Month ends (28/29/30/31), year end (Dec 31 -> Jan 1), leap day Feb 29 (2024, 2028; 1900 not leap, 2000 leap).
- Age/eligibility "turns 18 today": birthday today vs yesterday vs tomorrow; Feb 29 birthdays.
- Midnight (00:00:00 vs 23:59:59.999), inclusive end dates ("until March 31" ends at which instant?).
- DST transitions: the non-existent hour (spring forward) and the repeated hour (fall back) in the user's zone; scheduled jobs at 02:30 local.
- Time zones: the same instant is a different date in UTC+14 and UTC-12.
- Epoch limits: dates before 1970, the 2038 32-bit limit, far-future expiry dates.

## Collections and sizes
- Lists: 0, 1, many, max allowed, max+1 items.
- Pagination: page size exactly, page size + 1 (second page with 1 item), last page, empty page beyond end.
- Files: 0 bytes, exactly the limit, limit + 1 byte; upload limits at proxy vs app (different!).

## Gotchas
- Tests that use "today" break on the 29th-31st; freeze time (`page-clock-time-control`, freezegun, fake timers).
- Server and client time zones differ in CI.

## Verify
For each date/string/collection input, a boundary table exists and tests run with frozen clocks at the chosen dates.
