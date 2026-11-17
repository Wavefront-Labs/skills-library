---
id: computing-software.software-engineering.pydantic.pydantic-generic-models-parametrize
name: pydantic-generic-models-parametrize
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-generic-models, generics, typevar, basemodel-generic, model-parametrized-name, isinstance]
level: practitioner
status: docs-checked
description: "Build reusable generic Pydantic models with TypeVar or PEP 695 syntax, subclass them, rename parametrizations and avoid isinstance traps."
sources:
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: reuse one model shape for different payload types.

```python
DataT = TypeVar('DataT')

class Response(BaseModel, Generic[DataT]):  # BaseModel first, then Generic
    data: DataT

Response[int](data=1)
Response[int](data='value')  # ValidationError: 1 validation error for Response[int]
```
Python 3.12+ syntax also works: `class Response[DataT](BaseModel): data: DataT` (full type parameter syntax and TypeVar defaults supported since v2.11).

Facts:
- Config, validators and serialization logic on the generic model apply to parametrized classes; methods and attributes are inherited.
- Pydantic creates cached subclasses at runtime when you parametrize, so overhead is minimal.
- It does not check that a concrete type satisfies a TypeVar upper bound.
- To keep a subclass generic it must also inherit `Generic`: `class ChildClass(BaseClass[TypeX], Generic[TypeX])`. You can partially fill: `class ChildClass(BaseClass[int, TypeY], Generic[TypeY, TypeZ])`.
- Rename concrete classes by overriding `model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str`; returning `f'{params[0].__name__.title()}Response'` gives `IntResponse(data=1)`.
- Parametrized generics can be field types: `product: ResponseModel[Product]`. Reusing the same TypeVar in nested models (`nested: InnerT[T]`) enforces consistency; mismatches report e.g. `nested.inner`.

isinstance warning: do not do `isinstance(my_model, MyGenericModel[int])`; `isinstance(my_model, MyGenericModel)` is fine. To check a parametrization, subclass it: `class MyIntModel(MyGenericModel[int]): ...` then `isinstance(my_model, MyIntModel)`.

Revalidation: with a field `inner: GenericModel[Any]`, passing a `GenericModel[int]` instance is revalidated (the contained data is inspected again), which re-triggers custom validators (an after model validator prints twice in the docs example). Validating `GenericModel[str]` against `GenericModel[int]` still fails.

## Checked

Checked 2026-11-07. Re-read concepts/models in full (in chunks). Replaced the phrase 'revalidated against the looser type', which is not on the page, with wording the page supports.

Method: documentation only; no commands were run.
