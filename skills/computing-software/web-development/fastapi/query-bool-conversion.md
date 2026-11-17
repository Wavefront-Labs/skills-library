---
id: computing-software.web-development.fastapi.query-bool-conversion
name: query-bool-conversion
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, query-parameters, bool, type-conversion, validation-error]
level: intro
status: docs-checked
description: "Which query string values FastAPI converts to True or False for a bool parameter, and which ones return a 422 validation error."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bool query parameters

Goal: predict how a `bool` query parameter parses.

## Accepted
- True: `1`, `True`, `true`, `on`, `yes`, and any other case variation (uppercase, first letter uppercase).
- False: `0`, `false`, `off`, `no`, including case variations.
- Omitted: the declared default is used (the docs example defaults to `False`).

## Rejected
An empty value (`?short=`) or an unrecognised value (`?short=maybe`) produces a `422` validation error.

## Verify
Call `/items/foo?short=yes` and `/items/foo?short=maybe`; the docs say the first gives `True` and the second a 422.

## Checked

Every value list and the 422 rule were read in the Query Parameters tutorial page (Query parameter type conversion section).

Method: docs-only read of cited pages, 2026-11-08
