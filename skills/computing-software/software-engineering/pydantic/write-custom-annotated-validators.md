---
id: computing-software.software-engineering.pydantic.write-custom-annotated-validators
name: write-custom-annotated-validators
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-custom-validators, annotated, wrap-validator, get-pydantic-core-schema, validation-context, model-validator, nested-validation]
level: advanced
status: docs-checked
description: "Build Pydantic validators as Annotated metadata with __get_pydantic_core_schema__ and a wrap validator, and validate nested models via model_validator or context."
sources:
  - https://docs.pydantic.dev/latest/examples/custom_validators/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: attach reusable validation logic to a type, and validate nested fields using parent data.

## Annotated metadata validator (timezone constraint)
A frozen dataclass placed in `Annotated[...]` customizes the core schema through `__get_pydantic_core_schema__`. A `wrap` validator runs code before and after default validation:
```python
@dataclass(frozen=True)
class MyDatetimeValidator:
    tz_constraint: str | None = None

    def tz_constraint_validator(self, value: Any, handler: ValidatorFunctionWrapHandler):
        result = handler(value)  # standard pydantic validation
        ...
        return result

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            self.tz_constraint_validator,
            handler(source_type),
        )

ta = TypeAdapter(Annotated[dt.datetime, MyDatetimeValidator('America/Los_Angeles')])
```
Imports: `from pydantic_core import CoreSchema, core_schema` and `GetCoreSchemaHandler`, `ValidatorFunctionWrapHandler`, `PydanticUserError`, `TypeAdapter` from `pydantic`. The page's validator uses `assert` statements; a wrong tz gives a `ValidationError` of type `assertion_error` with `loc` `()`. The same pattern enforces a UTC offset between `lower_bound` and `upper_bound` using `result.utcoffset().total_seconds() / 3600`; `ta.validate_json('"2023-01-01T00:00:00-08:00"')` works with bounds (-10, -5).

## Nested model needing parent data, option 1: validator on the outer model
```python
class Organization(BaseModel):
    forbidden_passwords: list[str]
    users: list[User]

    @model_validator(mode='after')
    def validate_user_passwords(self) -> Self:
        for user in self.users:
            if user.password in self.forbidden_passwords:
                raise ValueError(f'Password {user.password} is forbidden. ...')
        return self
```
(`Self` from `typing_extensions`.) The error has an empty `loc`.

## Option 2: validation context
The nested `User` has `@field_validator('password', mode='after')` reading `info.context.get('forbidden_passwords', [])`. The parent adds to the context:
```python
@field_validator('forbidden_passwords', mode='after')
@classmethod
def add_context(cls, v, info: ValidationInfo):
    if info.context is not None:
        info.context.update({'forbidden_passwords': v})
    return v

Organization.model_validate(data, context={})
```
The error loc is `users.0.password`. If `context` is not passed to `model_validate()`, `info.context` is `None` and the check silently does not run. The page warns that mutating context adds power but can make code confusing and hard to debug.

## Checked

Checked 2026-11-07. Re-read examples/custom_validators in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
