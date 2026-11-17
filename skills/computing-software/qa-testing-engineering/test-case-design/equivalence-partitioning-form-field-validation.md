---
id: computing-software.qa-testing-engineering.test-case-design.equivalence-partitioning-form-field-validation
name: equivalence-partitioning-form-field-validation
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [form-field-validation, input-field-testing, equivalence-partitioning, boundary-value-analysis, ui-testing]
level: practitioner
status: docs-checked
description: "Apply equivalence partitioning to form field validation: client vs server checks, type, length, format, required and cross-field rules, with expected messages."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation
  - https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Applying EP to form field validation

**Goal:** systematic tests for every input field without testing every value.

## Per field, partition along
| Dimension | Partitions |
|---|---|
| Presence | empty (required?), whitespace only |
| Type | valid type, wrong type (letters in a number field) |
| Length | below min, within, above max (and the `maxlength` attribute) |
| Format | matches pattern, violates pattern (email, postcode, phone per country) |
| Value set / range | valid range, below, above |
| Business state | e.g. username taken vs free, date in past vs future |
| Character set | ASCII, accented/Unicode, emoji, RTL, HTML/script characters |

## Two layers
Test each invalid partition **both** in the browser (HTML5 `required`, `pattern`, `min/max`, JS) and directly against the API (bypassing the UI with curl or API tests). Client-side validation is UX; server-side validation is the real control.

## Cross-field rules
Partitions over field pairs: end date before/after start date, password confirmation matches or not, country -> postcode format. Use a decision table when several fields interact.

## Expected results
Each invalid partition has a specified message, field highlight and focus behaviour; check the message text, that it is programmatically associated with the field and that valid data is preserved after the error.

## Example: quantity field 1-20, integer
Partitions: empty, non-numeric, decimal, <= 0, 1-20, > 20, leading zeros "05", very long digit string. Boundaries from BVA: 0, 1, 20, 21.

## Gotchas
- Paste and autofill bypass keystroke filters; test them.
- `maxlength` is a browser-side limit only; the server must still check length.
- Trimming rules: does " bob " equal "bob"? Specify and test.

## Verify
A field-by-partition table with UI and API results and the expected message for every invalid partition.

## Checked

2026-10-28 Confirmed against: MDN form validation (required, pattern, minlength/maxlength, min/max attributes; client-side validation); OWASP Input Validation Cheat Sheet (validate on the server even when the browser checks, length limits). Removed or generalised: `aria-describedby` (not on the fetched pages) and the claim that maxlength truncates silently.

Method: documentation only; no commands were run.
