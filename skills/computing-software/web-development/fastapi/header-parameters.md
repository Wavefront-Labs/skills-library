---
id: computing-software.web-development.fastapi.header-parameters
name: header-parameters
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, header-parameters, header, convert-underscores, duplicate-headers]
level: practitioner
status: docs-checked
description: "Read HTTP headers in FastAPI with Header, understand the underscore to hyphen conversion, disable it, and receive duplicate headers as a list."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/header-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Header parameters

Goal: declare headers like query parameters.

## Rules
- Import `Header` from `fastapi` and use it like `Query`, `Path` and `Cookie`: defaults and extra validation are supported.
- You must use `Header`; otherwise the parameter would be read as a query parameter.
- Headers are hyphenated (`user-agent`), which is not a valid Python name. By default `Header` converts underscores to hyphens, so declare `user_agent`. HTTP headers are case-insensitive, so use snake_case.
- To disable the conversion, set `convert_underscores=False`. Warning: some HTTP proxies and servers disallow headers with underscores.
- Duplicate headers: declare a list type and you receive all values as a Python `list`. Two `X-Token` headers (`foo`, `bar`) arrive as a list holding both.

## Verify
Send a request with the header and check the value; try a duplicate header to see the list.

## Checked

Confirmed on the cited FastAPI header-params tutorial page: `Header` as a sister of `Query`, `Path` and `Cookie`, the need to use `Header`, underscore to hyphen conversion, case-insensitivity, `convert_underscores=False` and its proxy warning, and duplicate headers as a list. Removed: nothing.

Method: docs-only read of cited pages, 2026-11-08
