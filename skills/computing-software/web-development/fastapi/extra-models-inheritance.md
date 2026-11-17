---
id: computing-software.web-development.fastapi.extra-models-inheritance
name: extra-models-inheritance
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, pydantic, models, inheritance, union, anyof, model-dump, password-hash]
level: practitioner
status: docs-checked
description: "Split FastAPI models into input, output and database variants with a shared base class, return Union, list or dict response types, and unpack model_dump."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/extra-models.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple related models

Goal: one entity, several states, no duplicated fields.

## Pattern
- User example: input model has a password, output model has none, database model has a hashed password. Never store plaintext passwords; store a secure hash.
- `user_in.model_dump()` returns a dict; `UserInDB(**user_in.model_dump(), hashed_password=hashed_password)` unpacks it and adds the extra keyword.
- Reduce duplication with a `UserBase` model and subclasses that add only the differences. Validation and docs still work.

## Unions, lists, dicts
- A response can be a `Union` of models; OpenAPI describes it as `anyOf`. Put the most specific type first, e.g. `Union[PlaneItem, CarItem]`.
- Passing it as the `response_model` argument needs `Union` even in Python 3.10, because `A | B` in an assignment would be an invalid operation between classes (the `|` form only works in annotations).
- A list response uses `list[Model]`; an arbitrary dict response uses `dict` with key and value types, useful when field names are unknown.

## Caution
The doc's fake hasher and fake save functions give no real security.

## Verify
Compare the response against the documented model for each variant.

## Checked

Every claim above was read in the FastAPI extra models tutorial page. Removed the unstated /docs schema claim from Verify.

Method: docs-only read of cited pages, 2026-11-08
