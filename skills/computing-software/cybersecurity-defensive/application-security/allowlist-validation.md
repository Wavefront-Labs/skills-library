---
id: computing-software.cybersecurity-defensive.application-security.allowlist-validation
name: allowlist-validation
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [allowlist-validation, input-validation, positive-validation, canonicalisation, pydantic, bean-validation]
level: practitioner
status: docs-checked
description: "Validate input with allowlists: syntax and semantics, per-field rules, safe parsing with limits, whole-value regex matching, and why validation is not the injection defence."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html", "https://owasp.org/www-project-application-security-verification-standard/", "https://cwe.mitre.org/data/definitions/20.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allowlist input validation

Define what the application accepts and reject everything else. Do not try to recognise every malicious
string; blocking apostrophes, for example, rejects legitimate names without making a query safe.

## Two levels
- **Syntactic**: expected type and format.
- **Semantic**: sensible for the operation (a booking's end date is after its start date).

## Per-field rules
- Fixed choices: exact membership in the allowed set, including drop-down values.
- Numbers and dates: type, format, minimum and maximum.
- Strings: length limits and required characters or structure.
- Objects: allowed fields, required fields, null handling. Arrays: min/max item counts and validation of every
  item, including nested objects.
- Free-form comments: an allowlist can permit broad Unicode text while limiting length.

## Rules
1. Validate server-side; client-side checks are for immediate feedback only.
2. Apply request size limits before buffering or parsing, and parser limits such as nesting depth. Use a
   maintained parser, handle failures, validate the resulting values.
3. Converting text to an integer establishes a type, not an acceptable quantity.
4. Decode according to the protocol before checking, validate the representation that will actually be used,
   and avoid decoding again downstream (inconsistent decoding can invalidate earlier checks, per CWE-20).
5. For JSON schemas, configure required and additional properties explicitly: listing a property neither
   requires it nor rejects unknown fields. Bind only intended fields to objects (mass assignment).
6. Regex only for simple structured fields: require a match of the entire value (for example Python
   `fullmatch`), bound input length first, avoid heavy backtracking, treat a timeout as failure.
7. Reject invalid requests with a clear error; do not continue with partially validated data and do not
   "clean" input by stripping characters.
8. Validate data from internal APIs, queues and stored records when it crosses a trust boundary.
9. User-authored HTML needs a maintained sanitisation library, not regexes.

## Validation is not the injection defence
Use parameterised queries for SQL and context-aware output encoding for XSS, and check authorisation
separately: a valid account identifier does not mean the caller may access that account.

## Verify
Per-field tests with rejected ranges, missing fields, invalid nested items and oversized arrays, not just
malformed syntax.

## Checked
2026-11-01. Confirmed against the OWASP Input Validation Cheat Sheet (all rules above). Removed: framework
code samples (Pydantic, Bean Validation, Zod), the Ruby anchor note, `realpath` and NFC/NFKC advice, and the
example encoded-traversal string, none of which the cheat sheet states.
Method: documentation only; no commands were run.
