---
id: computing-software.software-engineering.pydantic.pydantic-construct-init-and-copy
name: pydantic-construct-init-and-copy
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validation-modes, model-construct, model-post-init, model-copy, custom-init, unvalidated]
level: practitioner
status: docs-checked
description: "Use model_construct, custom __init__, model_post_init and model_copy correctly, including what each skips or does not validate."
sources:
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: create or duplicate model instances without surprises.

model_construct() builds an instance without validation. Reasons given: data already known valid (performance), non-idempotent validators, validators with side effects you do not want. It can create invalid models, so only use it with data that is already validated or trusted. In V2 the performance gap to validation is narrow and for simple models validation may be faster, so profile first.

Behaviour notes:
- No validation includes dict-to-model conversion; convert inner dicts to models yourself.
- Fields with defaults still get their defaults if you omit them.
- Private attributes: `__pydantic_private__` is populated as it would be with validation.
- No `__init__` of the model or parents is called, even a custom one.
- For `RootModel`, pass the root value positionally.
- `extra`: `'allow'` stores extras in `__pydantic_extra__` and `__dict__`; `'ignore'` drops them; `'forbid'` does not raise.

Custom `__init__`: the default `__init__` only runs for the constructor and delegates to pydantic-core. A custom `__init__` is called unconditionally from all validation methods, without validation, so call `super().__init__(**kwargs)`. It is not recommended because strictness, extra-data behaviour and validation context are lost. To act after init, use an after field or model validator, or `model_post_init()`:

```python
class MyModel(BaseModel):
    id: int

    def model_post_init(self, context: Any) -> None:
        logging.info("Model initialized with id %d", self.id)
```

model_copy(): duplicates a model, with optional `update` values that are not validated. Shallow by default, `deep=True` for a deep copy:

```python
m.model_copy(update={'banana': 0})
id(m.bar) == id(m.model_copy().bar)             # True (shared)
id(m.bar) == id(m.model_copy(deep=True).bar)    # False
```
Copying is particularly useful with frozen models.

## Checked

Checked 2026-11-07. Re-read concepts/models in full (in chunks) and compared every claim; no changes needed.

Method: documentation only; no commands were run.
