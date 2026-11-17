---
id: computing-software.web-development.fastapi.body-multiple-params
name: body-multiple-params
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, request-body, body, embed, multiple-body-parameters, singular-values]
level: practitioner
status: docs-checked
description: "Declare several body parameters, singular body values with Body, and a single embedded body key with Body(embed=True) in a FastAPI path operation."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/body-multiple-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple body parameters

Goal: shape JSON bodies with more than one part.

## Rules
- `Path`, `Query` and body parameters mix freely. A body parameter is optional if its default is `None`.
- With two or more Pydantic-model parameters (for example `item` and `user`), FastAPI uses the parameter names as keys, so the body is `{"item": {...}, "user": {...}}`, even though `item` alone would be expected unwrapped.
- A singular value (like an `int`) is assumed to be a query parameter. Use `Body` to make it another body key, e.g. an `importance` key beside `item` and `user`.
- Extra query parameters can sit next to body parameters; a plain `q: str | None = None` is already a query parameter.
- `Body` takes the same validation and metadata arguments as `Query` and `Path`.
- A single model parameter is expected unwrapped. To require a key, declare `item: Annotated[Item, Body(embed=True)]` and the body becomes `{"item": {...}}`.

## Verify
Send the documented shape and check each parameter receives its own sub-object; send the unwrapped shape to an embed route and expect an error.

## Checked

Every claim above was read in the FastAPI body multiple parameters tutorial page. Removed the unstated 422 status code from Verify.

Method: docs-only read of cited pages, 2026-11-08
