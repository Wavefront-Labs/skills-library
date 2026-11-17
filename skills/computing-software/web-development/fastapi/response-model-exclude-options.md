---
id: computing-software.web-development.fastapi.response-model-exclude-options
name: response-model-exclude-options
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, response-model, exclude-unset, exclude-defaults, exclude-none, response-model-include, response-model-exclude]
level: advanced
status: docs-checked
description: "Trim FastAPI responses with response_model_exclude_unset, exclude_defaults, exclude_none, include and exclude, and know their schema trade-off."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/response-model.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Response encoding parameters

Goal: omit fields from JSON without new models.

## Decorator parameters
- `response_model_exclude_unset=True`: default values are left out; only explicitly set values appear. Values set equal to the default (for example `tax` 10.5 or `tags` `[]`) are still included, because Pydantic knows they were set explicitly.
- `response_model_exclude_defaults=True` and `response_model_exclude_none=True` exist as well, matching Pydantic's `exclude_defaults` and `exclude_none`.
- `response_model_include` / `response_model_exclude` take a set of attribute names, e.g. `{"name", "description"}`. A list or tuple is converted to a set.

## Trade-off
Include/exclude are a shortcut for a single model, but the OpenAPI schema and docs still show the full model. Using multiple classes is still recommended. The same applies to `response_model_by_alias`.

## Checked

Method: docs-only read of cited pages, 2026-11-08
