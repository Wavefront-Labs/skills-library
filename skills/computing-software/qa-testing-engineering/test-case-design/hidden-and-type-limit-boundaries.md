---
id: computing-software.qa-testing-engineering.test-case-design.hidden-and-type-limit-boundaries
name: hidden-and-type-limit-boundaries
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [hidden-boundaries, integer-overflow-boundaries, boundary-value-analysis, buffer-boundaries, implementation-boundaries]
level: practitioner
status: docs-checked
description: "Find boundaries the spec does not state: integer type limits, numeric column precision, safe-integer limits, proxy body size, batch sizes, timeouts and cache sizes."
sources:
  - https://cwe.mitre.org/data/definitions/190.html
  - https://www.postgresql.org/docs/current/datatype-numeric.html
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER
  - https://nginx.org/en/docs/http/ngx_http_core_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hidden boundaries

**Goal:** test the boundaries introduced by the implementation, where many real defects hide.

## Where to look
- **Integer types**: PostgreSQL `smallint` is 2 bytes, -32768 to +32767; `integer` is 4 bytes, -2147483648 to +2147483647; `serial` runs 1 to 2147483647. A counter, id or amount in cents stored in a 4-byte integer tops out at 2147483647 (about 21.4 million in a currency, when the value is cents). Overflow and wraparound is catalogued as CWE-190, Integer Overflow or Wraparound.
- **JavaScript numbers**: `Number.MAX_SAFE_INTEGER` is 9007199254740991 (2^53 - 1); test ids and amounts at that value and one above.
- **Numeric columns**: `NUMERIC(precision, scale)` rounds a value with too many fractional digits to the declared scale, then raises an error if the digits left of the decimal point exceed precision minus scale. `NUMERIC(10,2)` therefore holds up to 99999999.99; check each column's declaration in the schema (`\d table` in psql).
- **Buffers and chunks**: find the chunk size your code reads in and test inputs of chunk size, size + 1 and multiples.
- **Batch and page sizes**: for an API processing in batches of N, test N-1, N, N+1, 10N and 10N+1 records.
- **Limits in config**: nginx `client_max_body_size` defaults to 1m; a request body above it gets a 413 (Request Entity Too Large) and a value of 0 disables the check. Also look at request header buffers, rate limits, connection pool sizes and queue lengths.
- **Timeouts**: operations taking timeout minus a second and timeout plus a second.
- **Cache sizes and TTLs**: item count at eviction size; access just before and after TTL expiry.
- **Retry counts**: failure on the last allowed retry versus one more.
- **Third-party limits**: message length caps and maximum payment amounts are set by the provider; read the provider's current documentation for the figure.

## Finding them
Ask developers "what is the max size of X in code, DB or config?", read schemas and config, and search the source for limit constants (names like `MAX_`, `LIMIT`, `BATCH_SIZE`, `PAGE_SIZE`).

## Gotchas
- Limits differ between layers (UI, API, database): test at each layer's boundary.
- Defaults vary by product and version; confirm the default in the documentation of the version you run.

## Verify
A list of discovered implementation limits with tests at each, and any inconsistent limits between layers raised as defects.

## Checked
2026-11-08. Checked against PostgreSQL numeric types page (`smallint`, `integer`, `serial` ranges, `NUMERIC(precision, scale)` rounding and overflow rule), the psql reference (`\d`), MDN `Number.MAX_SAFE_INTEGER`, the nginx core module page (`client_max_body_size` default 1m, 413, 0 disables), and the CWE-190 title. Removed (not confirmed): SMS length figures, `VARCHAR(255)`, the 4096/8192 chunk sizes, and the grep command. The 99999999.99 bound and the 21.4 million figure are arithmetic from the stated rules. The ISTQB advanced-level source returned a server error and was dropped.

Method: documentation only; no commands were run.
