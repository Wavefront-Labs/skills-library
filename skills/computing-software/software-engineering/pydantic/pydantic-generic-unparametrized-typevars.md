---
id: computing-software.software-engineering.pydantic.pydantic-generic-unparametrized-typevars
name: pydantic-generic-unparametrized-typevars
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-generic-models, typevar-bound, serializeasany, typevar-default, data-loss, serialization]
level: practitioner
status: docs-checked
description: "Predict validation and serialization of unparametrized generic Pydantic models with bound, constrained or default TypeVars."
sources:
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: avoid silent data loss when a generic model is used without parametrizing it.

Validation of an unparametrized TypeVar (treated like built-in generics such as `list`):
- bound or constrained TypeVar: the bound/constraint type is used.
- TypeVar with a default (PEP 696, `typing_extensions.TypeVar(..., default=str)`): the default is used.
- unbound/unconstrained: falls back to `Any`.

```python
T = TypeVar('T'); U = TypeVar('U', bound=int); V = TypeVar('V', default=str)
class Model(BaseModel, Generic[T, U, V]):
    t: T; u: U; v: V
Model(t='t', u='u', v=1)  # errors on u (int_parsing) and v (string_type)
```

Data loss warning: if you pass a subtype of the bound/constraint/default without parametrizing, the subtype is not kept.

```python
ItemT = TypeVar('ItemT', bound='ItemBase')
class ItemHolder(BaseModel, Generic[ItemT]):
    item: ItemT
ItemHolder(**{'item': {'value': 1}})             # item=ItemBase()  (field info lost)
ItemHolder[IntItem](**{'item': {'value': 1}})    # item=IntItem(value=1)
```
Fix: parametrize explicitly.

Serialization differs by kind of TypeVar:
- Model used as an upper bound and never parametrized: validated with the bound but serialized as `Any`, so subclass fields appear (`bar` in `details` for `MyErrorDetails`). Parametrizing (`Error[ErrorDetails]`) serializes with the concrete type, so `bar` is dropped.
- Constraints or a default value and not parametrized: the default/constraint type is used for both validation and serialization (`bar` dropped). Override with `SerializeAsAny`:

```python
class SerializeAsAnyError(BaseModel, Generic[ErrorDataT]):
    message: str
    details: SerializeAsAny[ErrorDataT]
```
which dumps `{'foo': 'var', 'bar': 'baz'}`.

Bound-or-not does not change `model_dump()` when the value is a plain model: `ItemBound` and `ItemNoBound` with `IntValue(value=3)` all dump `{'item': {'value': 3}}`.

## Checked

Checked 2026-11-07. Re-read concepts/models in full (in chunks) and compared every claim; no changes needed.

Method: documentation only; no commands were run.
