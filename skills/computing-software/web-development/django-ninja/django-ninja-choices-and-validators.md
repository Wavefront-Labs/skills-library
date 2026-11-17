---
id: computing-software.web-development.django-ninja.django-ninja-choices-and-validators
name: django-ninja-choices-and-validators
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, tutorial-validation, field-validator, model-validator, choices, pydantic-custom-error, validation-errors]
level: practitioner
status: docs-checked
description: "Validate Django Ninja input with choices enums, field and model validators and custom error types, and read the resulting 422 responses."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-3.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make schemas accept only valid values and report every problem in one `422`.

## Choices as enums
`ModelSchema` ignores `choices`: a `status` listed in `Meta.fields` is just a `str`. Declare the field with the Django choices class as its type; `TextChoices` and `IntegerChoices` are enums, so Pydantic validates them and OpenAPI lists the values:
```python
class TaskOut(ModelSchema):
    status: TaskStatus
    priority: Priority
```
A docstring on the choices class becomes the enum description in OpenAPI. A bad value gives type `enum` with a msg like `Input should be 1, 2, 3 or 4`.

## Validators
```python
from pydantic import field_validator, model_validator
from pydantic_core import PydanticCustomError

class TaskUpdate(ModelSchema):
    priority: Priority = Priority.MEDIUM
    class Meta:
        model = Task
        fields = ["title", "description", "due_date"]

    @field_validator("title", check_fields=False)
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise PydanticCustomError("blank", "Title can't be blank")
        return value

class TaskIn(TaskUpdate):
    @model_validator(mode="after")
    def urgent_needs_due_date(self):
        if self.priority == Priority.URGENT and self.due_date is None:
            raise ValueError("Urgent tasks need a due date")
        return self
```
- A field validator runs after the type check and returns the value to store (here stripped).
- A `mode="after"` model validator runs once every field is valid, can compare fields, and returns `self`.
- A `ModelSchema` subclass inherits `Meta`, fields and validators, so put editable fields in a base schema and create-only fields in a subclass.
- Validators naming `Meta.fields` fields need `check_fields=False`; otherwise class creation fails with `PydanticUserError: Decorators defined with incorrect fields`. Fields you declare yourself do not need it.

## Error messages
`ValueError("...")` gives type `value_error` with `Value error, ` prepended to your message. `PydanticCustomError(type, message)` uses your type and message exactly, so clients can match on the type.

The `422` body is `{"detail": [{"type", "loc", "msg", ...}]}`. `loc` is `["body", "payload", "<field>"]`: request body, view argument name, field. All field errors come back together. The model validator runs only when all fields are valid, and its error has `loc` `["body", "payload"]`. None of this reaches the view, so nothing is saved.

Keep fields such as `status` out of input schemas when they change only through a dedicated endpoint.

## Checked

2026-11-07: Confirmed against tutorial/part-3.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
