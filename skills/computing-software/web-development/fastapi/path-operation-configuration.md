---
id: computing-software.web-development.fastapi.path-operation-configuration
name: path-operation-configuration
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, path-operation, tags, summary, description, docstring, deprecated, response-description]
level: intro
status: docs-checked
description: "Configure FastAPI path operation decorators: status_code, tags (with Enum), summary, description from docstring, response_description and deprecated."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/path-operation-configuration.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path operation configuration

These parameters go on the decorator, not the function.

- `status_code`: an `int` such as `404`, or constants from `fastapi.status` (same as `starlette.status`). Added to the OpenAPI schema.
- `tags`: a list of `str`. For big apps, store tags in an `Enum` to keep related operations on the same tag.
- `summary` and `description`: strings for the docs.
- Docstring: the function docstring becomes the description; Markdown is interpreted with docstring indentation taken into account.
- `response_description`: describes the response specifically (`description` is for the operation). If omitted, FastAPI generates "Successful response", since OpenAPI requires one.
- `deprecated=True`: keeps the operation but marks it deprecated in the interactive docs.

## Verify
Check the interactive docs for the tag group, text and deprecation marking.

## Checked

Every claim above was read in the FastAPI path operation configuration tutorial page. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
