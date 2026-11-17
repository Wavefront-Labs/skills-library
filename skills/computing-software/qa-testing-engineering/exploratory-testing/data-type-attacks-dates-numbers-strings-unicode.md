---
id: computing-software.qa-testing-engineering.exploratory-testing.data-type-attacks-dates-numbers-strings-unicode
name: data-type-attacks-dates-numbers-strings-unicode
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [data-type-attacks, unicode-testing, experience-based-testing, input-validation, internationalization]
level: practitioner
status: docs-checked
description: "Attack inputs by data type: numbers, dates, strings, Unicode normalisation and names, with a reusable attack catalogue (Big List of Naughty Strings)."
sources:
  - https://github.com/minimaxir/big-list-of-naughty-strings
  - https://unicode.org/reports/tr15/
  - https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data type attacks (dates, numbers, strings, Unicode)

**Goal:** each data type has a family of values that break code; try them deliberately and keep them as a reusable catalogue.

## Numbers
Zero, negative, boundaries of the field's type, very large and very small values, many decimal places, locale-specific separators, leading zeros or signs, scientific notation, whitespace.

## Dates and times
Leap days (leap and non-leap years), invalid days of a month, year boundaries, daylight-saving transitions, very early and very late dates, two-digit years, ambiguous day/month formats, time zone offsets, end-of-day times.

## Strings
Empty, only whitespace, very long, leading/trailing spaces, characters meaningful to SQL, HTML or script contexts, format-string tokens, path traversal sequences, newlines and tabs, spreadsheet formula prefixes in exported CSV. Treat these as input-validation probes on systems you own.

## Names
Do not assume a person has exactly one canonical full name; the Kalzumeus essay lists many wrong assumptions systems make about names. Test that a name a user reports as theirs is accepted, rather than rejected as having "invalid characters".

## Unicode normalisation
- The Unicode standard defines canonical equivalence (sequences representing the same abstract character) and compatibility equivalence. UAX #15 defines four normalisation forms, including NFC and NFKC (NFKC is compatibility decomposition followed by canonical composition), which make it possible to tell whether two strings are equivalent.
- Test that a composed character and its decomposed form (base letter plus combining mark) behave the same in equality, search and uniqueness checks.
- Also try emoji sequences, right-to-left text, zero-width characters and look-alike characters from other scripts in identifiers such as usernames, and check that length limits are counted in the unit the requirement names (bytes, code points or user-visible characters).

## Using it
Keep the catalogue as a data file, starting from the Big List of Naughty Strings (a list of strings with a high probability of causing issues as user input, MIT licensed), feed it into parametrized tests for every free-text field, and use it during exploratory sessions. The list is intended for software you own and manage; its README warns that using such strings against third-party software may be a crime and that it is not a substitute for formal security testing. It advises against the EICAR test string being added to the file because antivirus scanners flag it.

## Gotchas
- Truncation by bytes can split a multi-byte character and corrupt data.
- Round-trip checks matter: store, read back, export, email; corruption often appears downstream.

## Verify
Every free-text and date field is exercised with the catalogue, with no server errors, no corruption on round-trip, and sensible validation messages.

## Checked
2026-11-09. Confirmed in the Big List of Naughty Strings README (purpose, MIT licence, disclaimer, EICAR note), Unicode UAX #15 (canonical and compatibility equivalence, normalisation forms, NFKC definition) and the Falsehoods Programmers Believe About Names essay (names assumptions). Removed all specific numeric and date test values, MySQL utf8/utf8mb4 and UTF-16 claims, Turkish/German case-mapping examples, and the specific code-point examples, because none are stated on the fetched pages. "Whittaker's input attacks" attribution removed.
Method: documentation only; no commands were run.
