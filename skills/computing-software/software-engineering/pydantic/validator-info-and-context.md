---
id: computing-software.software-engineering.pydantic.validator-info-and-context
name: validator-info-and-context
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validation-info, validationinfo, validation-context, field-name, contextvar, python]
level: practitioner
status: docs-checked
description: "Use ValidationInfo in Pydantic validators to read earlier validated data, pass validation context, get field_name, and work around context with direct init."
sources:
  - https://docs.pydantic.dev/latest/concepts/validators/
  - https://docs.pydantic.dev/latest/concepts/types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ValidationInfo, validated data and context

Goal: give a validator access to other fields, caller-supplied context, or its own field name.

Field and model validators (all modes) can take an optional extra `ValidationInfo` argument exposing: `data`, `context`, `mode` (`'python'`, `'json'` or `'strings'`) and `field_name` (field validators only).

## `info.data`: already validated fields

```python
from pydantic import BaseModel, ValidationInfo, field_validator

class UserModel(BaseModel):
    password: str
    password_repeat: str
    username: str

    @field_validator('password_repeat', mode='after')
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data['password']:
            raise ValueError('Passwords do not match')
        return value
```

Validation follows field definition order, so only fields defined **earlier** are in `info.data` (`username` is not available above). `data` is `None` for model validators.

## `info.context`: caller-supplied

```python
class Model(BaseModel):
    text: str

    @field_validator('text', mode='after')
    @classmethod
    def remove_stopwords(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(info.context, dict):
            stopwords = info.context.get('stopwords', set())
            v = ' '.join(w for w in v.split() if w.lower() not in stopwords)
        return v

Model.model_validate({'text': 'This is an example document'},
                     context={'stopwords': ['this', 'is', 'an']})
# text='example document'
```

Check `isinstance(info.context, dict)` since no context may be given.

## Context with `Model(...)`

Not currently possible when instantiating directly. The page's workaround: a `ContextVar` plus a custom `__init__`:

```python
def __init__(self, /, **data: Any) -> None:
    self.__pydantic_validator__.validate_python(
        data, self_instance=self, context=_init_context_var.get(),
    )
```

Set the var with a `@contextmanager` (`token = var.set(value)` ... `var.reset(token)` in `finally`) around the `Model(...)` call.

## `info.field_name` in custom types

Inside `__get_pydantic_core_schema__`, use `core_schema.with_info_after_validator_function(cls.validate, handler(int))`; `validate(cls, value, info)` then sees `info.field_name`. The same works for `Annotated` markers such as `AfterValidator(fn)` where `fn(value, info)`. Requires Pydantic V2.4 or later.

## Checked

Checked 2026-11-07. Re-read concepts/validators in full (in chunks). For concepts/types, read the utility types section and the Access to field name section, not the whole page. Compared every claim; no changes needed.

Method: documentation only; no commands were run.
