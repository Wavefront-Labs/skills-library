---
id: computing-software.software-engineering.api-design.filtering-and-sorting-syntax
name: filtering-and-sorting-syntax
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, pagination, api-filtering, api-sorting, aip-160, query-parameters, odata]
level: practitioner
status: docs-checked
description: "Design list filtering and sorting parameters: simple field params vs a filter expression language (AIP-160, OData), order_by syntax and validation."
sources:
  - https://google.aip.dev/160
  - https://google.aip.dev/132
  - https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html
  - https://jsonapi.org/format/#fetching-filtering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtering and sorting syntax for list endpoints

Only add filtering or ordering when there is an established need: AIP-132 notes it is always possible to add them later, but removing them is a breaking change.

## Option 1: simple field parameters
```
GET /orders?status=open&customer_id=cus_42&sort=-created_at,id
```
- One parameter per filterable field. Easy to validate, document in OpenAPI and index.
- Sorting in the JSON:API style: `sort=age,name`, ascending unless a field is prefixed with a minus (`sort=-created,title`) which makes it descending.

## Option 2: filter expression language
AIP-160 recommends one `string filter` field with a structured syntax, because filtering needs evolve and a string field can change without client updates. Its grammar is formally defined by an EBNF in the AIP.
```
GET /v1/books?filter=author = "Le Guin" AND published > "1970-01-01T00:00:00Z" AND NOT status = "draft"&order_by=published desc, title
```
- Operators: `AND`, `OR`, `NOT` or `-`, `=`, `!=`, `<`, `>`, `<=`, `>=` (for strings, numbers, timestamps and durations, but not booleans or enums), `.` traversal (`a.b.c = "foo"`), and `:` has (`r:42` for repeated fields, `m:foo` for map keys, `r:*` for presence). `*` wildcards are supported in string equality (`a = "*.foo"`).
- **OR binds tighter than AND**, unlike most languages: `a AND b OR c` means `a AND (b OR c)`. Docs should encourage parentheses.
- The left side of a comparison must be a field name; the right side takes literals.
- Value types: enums use the case-sensitive string form, timestamps are RFC 3339, durations are a number with an `s` suffix (`20s`), booleans are `true`/`false`.
- Whitespace-separated bare literals are a fuzzy AND (`Victor Hugo` is roughly `Victor AND Hugo`); AIP-160 says list filters have fuzzy matching characteristics, and points to CEL for deterministic evaluation.
- A service may add limits (for example, cap the number of logical operators to avoid "queries of death") but must document them, and may define extra functions as `call(arg...)` which must be documented.
- `order_by` (AIP-132): comma-separated fields, ascending by default, `desc` suffix for descending (`"foo desc, bar"`), spaces insignificant, subfields with `.`. Natural comparators apply unless documented otherwise.
- OData uses a different syntax: `$filter=Name eq 'Milk' and Price lt 2.55`, plus `$orderby` and `$top` system query options.

Use an expression language when clients need arbitrary combinations; it costs a parser, a grammar to document, and harder query planning (this trade-off is the author's judgement, not from the sources).

## Implementation rules
- Validate: a non-compliant or schematically invalid filter (unknown field, value of the wrong type, invalid enum value, malformed timestamp) should return `INVALID_ARGUMENT` (HTTP 400); traversal to an undefined field also errors. Document any relaxed validation.
- Never build SQL from field names or expression text; map to columns through an allow-list and use bind parameters (general practice, not stated in the sources).
- When paginating, all other parameters (filter and order) must match the call that produced the page token (AIP-132).
- Pagination is stable only if the sort is fully determined; add a unique tiebreaker such as `id` (author's practice).

## Verify
- [ ] Negative tests: unknown field, malformed expression and SQL metacharacters all return 400.
- [ ] Check each supported filter and sort combination against an index on production-sized data.

## Checked
2026-11-08. Read in full: AIP-160 and AIP-132. Read in part only: the OData URL Conventions document (confirmed `$filter` with `eq`, `and`, `or`, `lt`, and the `$orderby` and `$top` options by searching) and the JSON:API format page (confirmed the `sort` parameter and minus-prefix rule). Removed: `_before/_after` and `min_/max_` suffix conventions, repeated-versus-comma-separated value advice, RSQL/FIQL, named parser libraries (CEL-go, aip-go), and the claim that changed filters return 400 citing AIP-158 (not read). Corrected: the draft's `published > "1970-01-01"` timestamp literal is now RFC 3339, and the missing OR-over-AND precedence rule was added.
Method: documentation only; no commands were run.
