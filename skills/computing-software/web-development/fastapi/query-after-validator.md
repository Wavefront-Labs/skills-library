---
id: computing-software.web-development.fastapi.query-after-validator
name: query-after-validator
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, query-parameters, custom-validation, after-validator, pydantic, annotated]
level: advanced
status: docs-checked
description: "Apply custom validation after type checks in FastAPI by placing Pydantic AfterValidator inside Annotated, and when a dependency is the better tool."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-params-str-validations.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom validators with AfterValidator

Goal: enforce a rule the built-in constraints cannot express.

## Method
- Use Pydantic's `AfterValidator` with a function, inside `Annotated`. The function runs after normal validation (for instance after the value is confirmed to be a `str`).
- The docs example checks that an item ID starts with `isbn-` or `imdb-`, using `value.startswith()` with a tuple of prefixes.
- Pydantic also has `BeforeValidator` and others.
- Requires Pydantic version 2 or above.

## When not to use
For validation needing an external component such as a database or another API, use FastAPI dependencies instead. Custom validators are for rules checkable from the request data alone.

## Verify
Send a value without an allowed prefix and expect a validation error response.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there. Verify step reworded: the page does not name a status code for custom validator failures.
Method: docs-only read of cited pages, 2026-11-08
