---
id: computing-software.web-development.fastapi.form-data-fields
name: form-data-fields
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, forms, form-data, python-multipart, checkbox, oauth2-password-flow]
level: practitioner
status: docs-checked
description: "Receive HTML form fields in FastAPI with Form, install python-multipart, handle unchecked checkboxes with a False default, and avoid mixing Form with JSON Body."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/request-forms.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Form fields

Goal: accept form-encoded input instead of JSON.

## Rules
- Install `python-multipart` first (the docs use `uv add python-multipart`).
- Import `Form` from `fastapi` and declare parameters like `Body` or `Query`. `Form` inherits from `Body`, so validation, examples and an alias (e.g. `user-name` instead of `username`) work.
- You must use `Form`; without it the parameter is a query or JSON body parameter.
- OAuth2 "password flow" requires fields named exactly `username` and `password`, sent as form fields, not JSON.
- Browsers omit unchecked checkboxes. Declare a bool form parameter with default `False`; a checked box sends `"on"`, which FastAPI accepts as `True`.
- Form data is `application/x-www-form-urlencoded`; with files it becomes `multipart/form-data`. `Form(media_type="multipart/form-data")` describes a multipart form in OpenAPI; setting it on one parameter is enough.

## Limitation
You cannot combine `Form` parameters with `Body` fields expected as JSON; the body has one encoding. This is HTTP, not FastAPI.

## Verify
Post with `-d` form encoding and read the values back.

## Checked

2026-11-08: Read the Form Data page (python-multipart, Form inherits Body, alias, OAuth2 password flow field names, checkbox default False and on, media types, multipart note, no JSON Body). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
