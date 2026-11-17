---
id: computing-software.web-development.fastapi.request-body-pydantic
name: request-body-pydantic
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, request-body, pydantic, basemodel, json]
level: intro
status: docs-checked
description: "Declare a FastAPI request body with a Pydantic BaseModel and how FastAPI decides whether a parameter is path, query or body."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/body.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Request body with BaseModel

Goal: receive JSON as a validated object.

## Method
1. Import `BaseModel` from `pydantic` and subclass it with standard Python types as attributes.
2. Attributes with a default are not required; use `None` for optional. Otherwise they are required.
3. Declare a path operation parameter whose type is the model.

FastAPI reads the body as JSON, converts types, validates, returns a clear error pointing at the bad data, gives you the object, generates JSON Schema, and adds it to OpenAPI and the docs.

## How parameters are classified
- Also in the path: path parameter.
- Singular type (`int`, `float`, `str`, `bool`): query parameter.
- Pydantic model: request body.

Use POST, PUT, DELETE or PATCH. A body on GET has undefined behaviour in the specs; it works but is discouraged, Swagger UI will not document it and proxies may not support it.

## Verify
POST valid and invalid JSON; the invalid one should return an error indicating where and what the bad data was.

## Checked

Every claim above was read in the FastAPI request body tutorial page. Removed the unstated 422 status code from Verify.

Method: docs-only read of cited pages, 2026-11-08
