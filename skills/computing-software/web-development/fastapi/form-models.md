---
id: computing-software.web-development.fastapi.form-models
name: form-models
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, forms, pydantic-model, extra-forbid, discriminated-union, form-data, multipart]
level: advanced
status: docs-checked
description: "Declare FastAPI form fields with a Pydantic model (0.113.0+), forbid extras (0.114.0+), combine models, make a group optional and mix with files."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/request-form-models.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Form models

Goal: validate form fields as a unit.

## Rules
- Needs `python-multipart`. Supported since FastAPI `0.113.0`: declare a Pydantic model and annotate the parameter as `Form`.
- Booleans for HTML checkboxes should default to `False`.
- Forbid extras with model config `extra="forbid"` (since `0.114.0`); a stray field returns `extra_forbidden` with `loc` `["body", "extra"]`.
- Combine several form models with individual `Form` parameters. Each validates independently, but each model's `extra` setting applies to all form fields and files, including those in other parameters or dependencies.
- Optional group: `Model | None = None`. None sent means `None`; any field sent (even an empty value) means the model is validated and needs all required fields. An optional model made only of unchecked checkboxes is omitted, so send e.g. `enabled=false`.
- Optional union of models works with a discriminator such as `kind=person` or `kind=company`.
- A form model can be combined with file parameters under `multipart/form-data`.

## Verify
Send an extra field and expect `extra_forbidden`.

## Checked

2026-11-08: Read the Form Models page (0.113.0, 0.114.0, extra_forbidden error, combining models, optional models and unions, files with forms). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
