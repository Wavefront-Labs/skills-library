---
id: computing-software.software-engineering.pydantic.fix-decorator-and-discriminator-errors
name: fix-decorator-and-discriminator-errors
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-usage-errors, field-validator, discriminated-union, discriminator, model-serializer, validator-signature, pydantic-user-error]
level: practitioner
status: docs-checked
description: "Diagnose Pydantic PydanticUserError codes for field_validator, field_serializer, model_serializer and discriminated unions, with the fix for each code."
sources:
  - https://docs.pydantic.dev/latest/errors/usage_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Usage errors: decorators and discriminated unions

Goal: map a `PydanticUserError` `code` (on `exc_info.code`) to its fix.

## Validator and serializer decorators

- `decorator-invalid-fields`: field names passed as a list. Use separate strings: `@field_validator('a', 'b')`.
- `decorator-missing-arguments`: bare `@field_validator` or `@field_serializer`. Give at least one field name.
- `decorator-missing-field`: the named field does not exist, e.g. `@field_validator('b')` with only `a`. Pass `check_fields=False` when inheriting and the field comes later (example: `create_model('FooModel', a=(str, 'cake'), __base__=Model)`).
- `validator-instance-method`: `@field_validator` on an instance method (`def check_a(self, value)`). Use `@classmethod`.
- `model-after-validator-classmethod`: `@model_validator(mode='after')` must be an instance method, not a classmethod.
- `validator-input-type`: `json_schema_input_type` given with `mode` other than `'before'`, `'plain'`, `'wrap'`. It is not available for `after` validators because the value is already validated against the annotation.
- `validator-signature`: wrong signature, e.g. `check_a(cls)` with no value argument.
- `field-serializer-signature`, `model-serializer-signature`, `model-serializer-instance-method`, `multiple-field-serializers`: see the field-serializers and model-serializers skills for valid signatures.

## Discriminated unions (`Field(discriminator='pet_type')`)

- `discriminator-no-field`: a union member (e.g. `Cat`) lacks the discriminator field.
- `discriminator-needs-literal`: the discriminator field is not a `Literal` (e.g. `pet_type: int`).
- `discriminator-alias-type`: a non-string alias such as `AliasChoices('Pet', 'PET')`.
- `discriminator-alias`: members define different aliases (`'PET'` vs `'Pet'`); they must match.
- `discriminator-validator`: a before, wrap or plain validator on the discriminator field is disallowed since it would change the value that selects the model. Workaround: use a standard union without the discriminator, e.g. `pet: Cat | Dog`; then `Model(pet={'pet_type': 'kitten'}).pet.pet_type == 'cat'`.
- `callable-discriminator-no-tag`: with a callable `Discriminator(fn)`, every union choice needs a `Tag`, e.g. `Annotated[str, Tag('str')] | Annotated[Model, Tag('model')]`.

## Misc

- `typed-dict-version`: use `typing_extensions.TypedDict`, not `typing.TypedDict`, on Python < 3.12.
- `invalid-annotated-type`: the annotation cannot annotate that type, e.g. `Annotated[str, FutureDate()]`.

## Checked

Checked 2026-11-07. Compared every claim with the usage errors page (errors/usage_errors.md): each decorator, discriminator, `validator-input-type`, `typed-dict-version` and `invalid-annotated-type` code, the example triggers, the `check_fields=False` fix, the standard-union workaround for `discriminator-validator`, and the `Tag` requirement. All confirmed; nothing removed.

Method: documentation only; no commands were run.
