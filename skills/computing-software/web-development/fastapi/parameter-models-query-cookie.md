---
id: computing-software.web-development.fastapi.parameter-models-query-cookie
name: parameter-models-query-cookie
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, query-parameters, cookie-parameters, header-parameters, pydantic-model, extra-forbid, parameter-models]
level: advanced
status: docs-checked
description: "Group related FastAPI query or cookie parameters in a Pydantic model (0.115.0+), forbid extras, combine models and make a whole group optional."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-param-models.md, https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/cookie-param-models.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameter models

Goal: validate a related set of query parameters or cookies once, reusably.

## Method
- Supported since FastAPI `0.115.0`. Declare the fields in a Pydantic model and annotate the parameter with the model plus `Query` (or `Cookie`). The same works for `Header`.
- FastAPI extracts each field from the request and hands you the model.
- Forbid extras with Pydantic config `extra="forbid"`. A stray `tool` query parameter returns `"type": "extra_forbidden"` with `"loc": ["query", "tool"]`, and likewise for cookies.
- Several models can be combined with single parameters and dependencies. The query string stays flat (no key per model). Each model validates independently, but each model's `extra` setting applies to all parameters of that kind: `forbid` rejects any parameter outside the model, `allow` keeps them as model extras.
- Models sharing a name or alias each validate it; OpenAPI lists it once, so keep the type and constraints the same.
- Optional group: `Model | None` with default `None`. If no field is sent the value is `None`; if any is sent, FastAPI validates the model (both fields are required in the page's examples). `| None` without a default is still required.

## Gotcha
The docs UI cannot send cookies (browser JavaScript limitation), so Execute will error.

## Verify
Send an unexpected parameter and expect `extra_forbidden`.

## Checked

Every claim above was read in the FastAPI query parameter models and cookie parameter models tutorial pages (0.115.0, extra forbid and the extra_forbidden error shape, combining models, shared names, optional groups, cookies in the docs UI). The optional-group wording now says both fields are required in the page's examples rather than all required fields.

Method: docs-only read of cited pages, 2026-11-08
