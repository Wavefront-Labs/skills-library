---
id: computing-software.web-development.fastapi.path-numeric-validations
name: path-numeric-validations
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, path-parameters, numeric-validation, ge-gt-le-lt, annotated]
level: practitioner
status: docs-checked
description: "Use Path with gt, ge, lt and le for numeric validation in FastAPI, why path parameters are always required, and how parameter order is handled."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/path-params-numeric-validations.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path() and numeric constraints

Goal: validate and document path parameters.

## Rules
- Import `Path` and `Annotated`; `Path` takes all the same arguments as `Query` (for example `title`).
- A path parameter is always required because it is part of the URL. Adding `None` to its type does not make it optional, and a parameter declared with `Path` cannot have a default.
- Numeric constraints: `gt` greater than, `ge` greater than or equal, `lt` less than, `le` less than or equal. They work for `int` and `float`, on `Query` and `Path`.
- Float example: `gt=0` accepts `0.5` but rejects `0.0` and `0`.
- Ordering: with `Annotated` you do not need to reorder arguments. Without it, put the no-default parameter first, or pass `*` as the first parameter so the rest are keyword arguments.
- `Query` and `Path` are functions returning instances of classes that subclass `Param`.

## Verify
Call the route with a value just outside the bound and expect a validation error.

## Checked

Every claim above was read in the FastAPI path parameters and numeric validations tutorial page (Path, required path parameters, gt/ge/lt/le, float example, ordering and the `*` trick, Param subclasses). Removed the unstated 422 status code from Verify.

Method: docs-only read of cited pages, 2026-11-08
