---
id: computing-software.web-development.django-ninja.django-ninja-validation-error-customization
name: django-ninja-validation-error-customization
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, validation-errors, exception-handlers, pydantic, errors, 422]
level: advanced
status: docs-checked
description: "Reshape Django Ninja 422 validation errors by overriding the ValidationError handler or validation_error_from_error_contexts on a NinjaAPI subclass."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/errors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: change what clients see when request validation fails.

Request validation failures raise `ninja.errors.ValidationError` (not `pydantic.ValidationError`). The default response is status 422 with `{"detail": [ ... ]}`.

## Option 1: replace the response
Override the handler like any other:

```python
from django.http import HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError

api = NinjaAPI()

@api.exception_handler(ValidationError)
def validation_errors(request, exc: ValidationError):
    return HttpResponse("Invalid input", status=422)
```

## Option 2: change the errors list
Subclass `NinjaAPI` and override `validation_error_from_error_contexts`. It receives a list of `ValidationErrorContext` (one per parameter source that failed: path, query, body, ...) and must return a `ValidationError`.

```python
from typing import Any
from ninja import NinjaAPI
from ninja.errors import ValidationError, ValidationErrorContext

class CustomNinjaAPI(NinjaAPI):
    def validation_error_from_error_contexts(
        self, error_contexts: list[ValidationErrorContext],
    ) -> ValidationError:
        custom_error_infos: list[dict[str, Any]] = []
        for context in error_contexts:
            model = context.model
            param_source = model.__ninja_param_source__
            for e in context.pydantic_validation_error.errors(
                include_url=False, include_context=False, include_input=False
            ):
                custom_error_infos.append(
                    {"loc": (param_source, *e["loc"]), "msg": e["msg"], "type": e["type"]}
                )
        return ValidationError(custom_error_infos)

api = CustomNinjaAPI()
```

Each `ValidationErrorContext` exposes:
- `pydantic_validation_error`: the underlying `pydantic.ValidationError`.
- `model`: the `ParamModel` that failed; its `__ninja_param_source__` says which part of the request it came from (`"path"`, `"query"`, `"body"`, etc.).

The `ValidationError` you return still passes through the normal `ValidationError` handler (default or your override), so both hooks can be combined.

## Checked
Confirmed 2026-11-08 against the Django Ninja errors guide (docs/docs/guide/errors.md, read in full): the `ninja.errors.ValidationError` 422 default, the handler override, `validation_error_from_error_contexts`, and the `ValidationErrorContext` attributes. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
