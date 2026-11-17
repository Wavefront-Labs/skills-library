---
id: computing-software.software-engineering.pydantic.pydantic-field-options-deprecated-computed
name: pydantic-field-options-deprecated-computed
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-field-metadata, computed-field, deprecated, exclude, discriminator, repr, frozen-field]
level: practitioner
status: docs-checked
description: "Use Field options frozen, exclude, repr, discriminator and deprecated, plus the computed_field decorator, in Pydantic models."
sources:
  - https://docs.pydantic.dev/latest/concepts/fields/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: tune individual fields beyond type and default.

- `repr`: `Field(repr=False)` hides a field from the model's string representation (`repr=True` is the default).
- `frozen`: `name: str = Field(frozen=True)`; assigning raises `ValidationError` "Field is frozen" (type `frozen_field`). `Final[str]` (or `name: Final = 'John'`, type inferred) also makes a field immutable.
- `exclude`: `age: int = Field(exclude=True)` drops the field from `model_dump()`. `exclude_if` (added v2.12) excludes conditionally. See the serialization docs for inclusion/exclusion.
- `title`, `description`, `examples`, `json_schema_extra` only customize the generated JSON Schema.

Discriminator for unions: pass a field name, or a `Discriminator` instance when the discriminating field differs per model:

```python
class Model(BaseModel):
    pet: Cat | Dog = Field(discriminator='pet_type')   # Cat/Dog have pet_type: Literal[...]
```
```python
def pet_discriminator(v):
    if isinstance(v, dict):
        return v.get('pet_type', v.get('pet_kind'))
    return getattr(v, 'pet_type', getattr(v, 'pet_kind', None))

class Model(BaseModel):
    pet: Annotated[Cat, Tag('cat')] | Annotated[Dog, Tag('dog')] = Field(
        discriminator=Discriminator(pet_discriminator))
```

Deprecated fields (v2.7.0): `deprecated` accepts a string (the message), a boolean, or a `deprecated` decorator instance (`warnings.deprecated`, or the `typing_extensions` backport). It emits a runtime deprecation warning on access and sets `deprecated: True` in JSON Schema. `category` and `stacklevel` are ignored. Reading a deprecated field inside a validator emits the warning; wrap it in `warnings.catch_warnings()` with `simplefilter('ignore', DeprecationWarning)` to silence it.

computed_field: include a `@property` (or `cached_property`) in serialization and in serialization-mode JSON Schema.

```python
class Box(BaseModel):
    width: float; height: float; depth: float

    @computed_field
    @property
    def volume(self) -> float:
        return self.width * self.height * self.depth

Box(width=1, height=2, depth=3).model_dump()
#> {'width': 1.0, 'height': 2.0, 'depth': 3.0, 'volume': 6.0}
```
Schema marks it `readOnly: True` and required. Pydantic adds no validation or cache invalidation to the property. Use an explicit `@property`. Computed fields can be deprecated and, since v2.13, use `exclude_if` on the decorator.

## Checked

Checked 2026-11-07. Re-read concepts/fields in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
