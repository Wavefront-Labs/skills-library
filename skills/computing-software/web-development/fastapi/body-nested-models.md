---
id: computing-software.web-development.fastapi.body-nested-models
name: body-nested-models
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, request-body, nested-models, pydantic, list, set, httpurl, dict]
level: practitioner
status: docs-checked
description: "Model nested JSON in FastAPI with typed lists, sets, submodels, HttpUrl, top-level list bodies and arbitrary dict bodies with int keys."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/body-nested-models.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested body models

Goal: describe deep JSON with Pydantic types.

## Building blocks
- A bare `list` attribute does not declare element types; use `list[str]`. Type parameters use the standard Python syntax.
- `set[str]` converts duplicates into unique items on input and output, and is documented that way.
- A submodel (for example `Image`) can be the type of an attribute, or the element type of `list[Image]`, nested to any depth.
- `HttpUrl` from Pydantic checks a string is a valid URL and documents it as such. See Pydantic's type overview for more.

## Other body shapes
- Top-level JSON array: annotate the parameter as `list[Image]`.
- Arbitrary keys: declare a `dict`. JSON keys are always strings, but Pydantic converts them, so `int` keys with `float` values work when the strings are pure integers.

You keep editor support, conversion, validation and docs at every level.

## Verify
Post nested JSON that exercises each level and check the interactive docs show the nested schema.

## Checked

Every claim above was read in the FastAPI nested models tutorial page. Removed the unstated claim about error loc from Verify.

Method: docs-only read of cited pages, 2026-11-08
