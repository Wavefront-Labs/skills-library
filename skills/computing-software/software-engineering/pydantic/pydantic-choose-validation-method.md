---
id: computing-software.software-engineering.pydantic.pydantic-choose-validation-method
name: pydantic-choose-validation-method
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validation-modes, model-validate, model-validate-json, from-attributes, validation-error, orm]
level: practitioner
status: docs-checked
description: "Pick between __init__, model_validate, model_validate_json and model_validate_strings, read ValidationError, and validate ORM objects."
sources:
  - https://docs.pydantic.dev/latest/concepts/models/
  - https://docs.pydantic.dev/latest/errors/errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick the right entry point for the data you have.

Python mode:
- `Model(**kwargs)`: keyword arguments only.
- `Model.model_validate(obj)`: a dict, a model instance (assumed valid by default; see `revalidate_instances`), or an arbitrary object if enabled.

JSON and strings modes:
- `Model.model_validate_json(str_or_bytes)`: validates a JSON string or `bytes`. Generally faster than parsing to a dict yourself.
- `Model.model_validate_strings({...})`: a (possibly nested) dict with string keys and values, validated in JSON mode so strings coerce to the right types.

```python
m = User.model_validate_strings({'id': '123', 'name': 'James', 'signup_ts': '2024-04-01T12:00:00'})
# signup_ts=datetime.datetime(2024, 4, 1, 12, 0)
User.model_validate_strings({'id': '123', 'signup_ts': '2024-04-01'}, strict=True)  # ValidationError, datetime_parsing
```

The `model_validate_*()` methods let you control strictness, extra data and validation context per call; the constructor does not. Python and JSON modes can behave differently (for example with strictness). For JSON-mode behaviour from a non-JSON source, dump to JSON first (`json.dumps()`) or use `model_validate_strings()` for string-valued dicts.

Errors: one `ValidationError` is raised with every error found.

```python
Model(list_of_ints=['1', 2, 'bad'], a_float='not a float')
# 2 validation errors for Model
# list_of_ints.2  ... [type=int_parsing ...]
# a_float         ... [type=float_parsing ...]
```
`err.errors()` returns dicts; `e['loc']` gives locations such as `('a',)`.

Arbitrary objects (formerly ORM mode): set `ConfigDict(from_attributes=True)` or pass `from_attributes` to `model_validate()`. Attributes are read by field name. In the docs example the nested `Pet` model also sets `from_attributes=True`, and nested objects become nested models:

```python
class Person(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    pets: list[Pet]
anna_model = Person.model_validate(anna)  # anna is a plain object
```

## Checked

Checked 2026-11-07. Re-read concepts/models in full (in chunks) and errors/errors in full. Reworded the from_attributes sentence, because the page's example only shows the nested model also setting from_attributes and does not state a rule. Added errors/errors to sources for the loc and errors() claims.

Method: documentation only; no commands were run.
