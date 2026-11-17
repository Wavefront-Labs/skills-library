---
id: computing-software.software-engineering.pydantic.polymorphic-and-as-any-serialization
name: polymorphic-and-as-any-serialization
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-polymorphic-serialization, serialize-as-any, subclass, polymorphism, serialization, duck-typing]
level: practitioner
status: docs-checked
description: "Control whether subclass fields appear when serializing Pydantic models: default behavior, polymorphic_serialization (v2.13), SerializeAsAny and serialize_as_any."
sources:
  - https://docs.pydantic.dev/latest/concepts/serialization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serialize subclasses: default, polymorphic, and "as Any"

Goal: decide whether subclass-only fields are included when a subclass instance sits in a base-typed field.

## Defaults

- Subclasses of supported types (e.g. a `date` subclass) serialize as the superclass: `{"date":"2023-01-01"}`.
- For model-like fields (models, dataclasses) the value serializes as the annotated class, even if it is a subclass; only fields declared on the annotation appear. With `user: User` holding a `UserLogin(name=..., password=...)`, `model_dump()` gives `{'user': {'name': 'pydantic'}}`. The page says this is deliberate: you know precisely which fields could be included, preventing surprises such as leaking secrets added in subclasses.

## Polymorphic serialization (added v2.13)

Serialize an instance by its own runtime schema. Applies only to Pydantic models and Pydantic dataclasses; standard library dataclasses are not supported, even as subclasses of a Pydantic dataclass.

- Config level: `polymorphic_serialization` in `ConfigDict`, set on the class that should be polymorphic, not on the class referencing it.
- Runtime level: `polymorphic_serialization=True` or `False` on a serialization call. It applies to all nested types and overrides config.

```python
outer_model.model_dump()                                 # {'user': {'name': 'pydantic'}}
outer_model.model_dump(polymorphic_serialization=True)   # {'user': {'name': 'pydantic', 'password': 'password'}}
```

This was formerly called duck-typed serialization, which the page calls a misnomer.

## "Any" serialization

A more extreme form: the annotation is ignored and the runtime type decides, for all types, not only models. Pydantic can infer: many standard library types, types with a `__pydantic_serializer__` attribute, and anything handled by the `fallback` function passed to a serialization method. The page says that in most cases polymorphic serialization is preferred.

- Field level: `SerializeAsAny[User]`. Validation and static typing treat it as `User`; serialization treats it as `Any`.
- Runtime: `model_dump(serialize_as_any=True)` includes subclass fields in every field; `False` (default) does not.

```python
class OuterModel(BaseModel):
    as_any: SerializeAsAny[User]
    as_user: User
# as_any -> {'name': 'pydantic', 'password': 'password'}; as_user -> {'name': 'pydantic'}
```

Gotcha: `serialize_as_any=True` applies to all values, not just where duck typing matters; prefer `SerializeAsAny` when you need it on specific fields.

## Checked

Checked 2026-11-07. Re-read the concepts/serialization page in full (in chunks) and compared every claim; no changes needed.

Method: documentation only; no commands were run.
