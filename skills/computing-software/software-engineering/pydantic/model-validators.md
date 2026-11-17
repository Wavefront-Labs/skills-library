---
id: computing-software.software-engineering.pydantic.model-validators
name: model-validators
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-model-validators, model-validator, cross-field-validation, before-after-wrap, python]
level: practitioner
status: docs-checked
description: "Validate a whole Pydantic model with model_validator in after, before or wrap mode, including cross-field checks, raw input handling and inheritance rules."
sources:
  - https://docs.pydantic.dev/latest/concepts/validators/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model validators

Goal: enforce constraints on the entire model's data with `@model_validator`. Three modes exist.

## After: instance method, post-init hook

Runs after the whole model validated. Defined as an *instance* method; **return the validated instance**.

```python
from typing_extensions import Self
from pydantic import BaseModel, model_validator

class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self
```

## Before: raw input

Runs before the model is instantiated; the input may be any object, so annotate `data: Any`. Most of the time it is a dict, but with `from_attributes` set you may receive an arbitrary class instance, so check the type.

```python
class UserModel(BaseModel):
    username: str

    @model_validator(mode='before')
    @classmethod
    def check_card_number_not_present(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'card_number' in data:
                raise ValueError("'card_number' should not be included")
        return data
```

Avoid mutating the raw value and then raising later; with unions the mutated value may be passed to other validators.

## Wrap: most flexible

Run code before or after other validation, return data early, or raise. Takes a handler typed `ModelWrapValidatorHandler[Self]`.

```python
import logging
from pydantic import ModelWrapValidatorHandler, ValidationError

class UserModel(BaseModel):
    username: str

    @model_validator(mode='wrap')
    @classmethod
    def log_failed_validation(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        try:
            return handler(data)
        except ValidationError:
            logging.error('Model %s failed to validate with data %s', cls, data)
            raise
```

## Inheritance

A model validator defined in a base class is called when validating a subclass instance. Overriding it in a subclass replaces the base version, so only the subclass version is called.

## Related

- In model validators, `ValidationInfo.data` is `None`.

## Checked

Checked 2026-11-07. Compared every claim with the validators concepts page (concepts/validators.md): after (instance method, return the instance), before (raw input, `from_attributes` case, mutation warning), wrap with `ModelWrapValidatorHandler[Self]`, the inheritance note, and `ValidationInfo.data` being `None` for model validators. All confirmed; nothing removed.

Method: documentation only; no commands were run.
