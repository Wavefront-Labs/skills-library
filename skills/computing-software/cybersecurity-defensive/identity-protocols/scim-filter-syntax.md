---
id: computing-software.cybersecurity-defensive.identity-protocols.scim-filter-syntax
name: scim-filter-syntax
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [scim-filter-syntax, scim-filtering-paging, scim-filter, eq, co, sw, pr, valuepath, and-or-not, identity-protocols]
level: practitioner
status: docs-checked
description: "Write SCIM filter expressions with eq, ne, co, sw, ew, pr, gt, ge, lt, le, and, or, not, parentheses and valuePath brackets, with escaping rules."
sources:
  - https://www.rfc-editor.org/rfc/rfc7644#section-3.4.2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filter operators and grouping

Goal: query users precisely.

Operators: `eq ne co sw ew pr gt ge lt le`; logical `and`, `or`, `not(...)`; evaluation order is grouping, then logical operators (`not` before `and` before `or`), then attribute operators; group with `( )`. Complex multi-valued: `emails[type eq "work" and value co "@example.com"]`. Date comparisons: `meta.lastModified gt "2011-05-13T04:42:34Z"` (chronological for dateTime).

Request: `GET /Users?filter=userName eq "bjensen"` (percent-encode the URL; the RFC examples are not encoded).

Gotchas:
- Attribute names and operators are case insensitive; string value matching follows the attribute's `caseExact` characteristic (`userName` is case insensitive).
- Comparison values follow JSON: strings quoted, `true`, `false` and `null` unquoted.
- Filtering is optional. Check `filter.supported` and `filter.maxResults` in ServiceProviderConfig. An unrecognised operator must be declined with 400 `invalidFilter`; `gt`, `ge`, `lt`, `le` on Boolean or Binary also give `invalidFilter`.
- A multi-valued attribute matches if any value matches. Filtering on an undefined attribute treats it as having no value.

Verify: run filters for eq, co and pr against a test server.

## Checked
2026-11-02. Confirmed against RFC 7644 section 3.4.2.2 (Tables 3 to 5, ABNF, order of operations, examples) and RFC 7643 sections 2.2, 4.1.1 and 5. Removed: "ISO 8601" wording (RFC 7643 says xsd:dateTime), and the filter-injection and SQL/LDAP parameterisation advice, which neither RFC states.
Method: documentation only; no commands were run.
