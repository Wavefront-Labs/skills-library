---
id: computing-software.software-engineering.pydantic.validator-pattern-ordering-json-schema
name: validator-pattern-ordering-json-schema
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-field-validators, annotated-pattern, validator-order, json-schema-input-type, check-fields, python]
level: practitioner
status: docs-checked
description: "Choose between Annotated validators and field_validator, predict validator execution order, and set json_schema_input_type for before, plain or wrap validators."
sources:
  - https://docs.pydantic.dev/latest/concepts/validators/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a validator pattern, ordering, and JSON Schema input type

Goal: pick the right field-validator style and know when each validator runs.

## Annotated pattern: reuse

Both styles do the same job; the Annotated pattern makes validators reusable and visible in the annotation.

```python
EvenNumber = Annotated[int, AfterValidator(is_even)]

class Model1(BaseModel):
    my_number: EvenNumber

class Model2(BaseModel):
    other_number: Annotated[EvenNumber, AfterValidator(lambda v: v + 2)]

class Model3(BaseModel):
    list_of_even_numbers: list[EvenNumber]  # applies to list items, not the list
```

## Decorator pattern: many fields

```python
class Model(BaseModel):
    f1: str
    f2: str

    @field_validator('f1', 'f2', mode='before')
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.capitalize()
```

- Pass `'*'` as the field name to apply to all fields, including those in subclasses.
- By default the decorator checks that the named fields exist. Pass `check_fields=False` to disable this at class creation (useful when the validator is on a base class and the field lives on subclasses).

## Ordering (Annotated pattern)

Before and wrap validators run **right to left**; after validators then run **left to right**:

```python
name: Annotated[
    str,
    AfterValidator(runs_3rd),
    AfterValidator(runs_4th),
    BeforeValidator(runs_2nd),
    WrapValidator(runs_1st),
]
```

Decorator validators are converted to the annotated form and added last after existing field metadata, so the same ordering applies.

## `json_schema_input_type`

With before, plain or wrap validators the accepted input can differ from the annotation. Declare it so the JSON Schema is right:

```python
@field_validator('value', mode='before', json_schema_input_type=int | str)
@classmethod
def cast_ints(cls, value: Any) -> Any:
    return str(value) if isinstance(value, int) else value

Model.model_json_schema()['properties']['value']
# {'anyOf': [{'type': 'integer'}, {'type': 'string'}], 'title': 'Value'}
```

If omitted, the field type is used (for plain validators, `Any`, since the field type is discarded).

## Checked

Checked 2026-11-07. Re-read concepts/validators in full (in chunks) and compared every claim; no changes needed.

Method: documentation only; no commands were run.
