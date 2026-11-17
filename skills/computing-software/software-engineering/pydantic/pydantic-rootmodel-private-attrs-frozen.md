---
id: computing-software.software-engineering.pydantic.pydantic-rootmodel-private-attrs-frozen
name: pydantic-rootmodel-private-attrs-frozen
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-root-model, rootmodel, private-attr, frozen, classvar, abstract-base-class]
level: practitioner
status: docs-checked
description: "Use RootModel for non-object roots, PrivateAttr for underscore attributes, frozen models, ClassVar and ABC with Pydantic models."
sources:
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: handle models that are not plain field bags.

RootModel: the root type is the generic parameter and can be any type Pydantic supports. Pass the value as the first and only argument to `__init__` or `model_validate`.

```python
Pets = RootModel[list[str]]
Pets(['dog', 'cat'])                       #> root=['dog', 'cat']
Pets(['dog', 'cat']).model_dump_json()     #> ["dog","cat"]
Pets.model_json_schema()
# {'items': {'type': 'string'}, 'title': 'RootModel[list[str]]', 'type': 'array'}

class Pets(RootModel[list[str]]):
    def describe(self) -> str:
        return f'Pets: {", ".join(self.root)}'
```

Private attributes: a leading underscore makes an attribute private. It is not a field, not in the schema, and not validated or set by `__init__`/`model_validate`. Use `PrivateAttr`:

```python
class TimeAwareModel(BaseModel):
    _processed_at: datetime = PrivateAttr(default_factory=datetime.now)
    _secret_value: str

    def model_post_init(self, context: Any) -> None:
        self._secret_value = randint(1, 5)
```
Dunder names (`__attr__`) are not supported and are ignored. Since v2.13 default factories for private attributes can take the validated data as an argument.

ClassVar: `x: ClassVar[int] = 1` is a class variable, not a field; in the docs `print(Model())` shows only `y=2` while `Model.x` is `1`.

Frozen: `model_config = ConfigDict(frozen=True)`. Assigning raises `ValidationError` ("Instance is frozen", type `frozen_instance`). Immutability is only faux: a `dict` field can still be mutated in place (`foobar.b['apple'] = 'grape'` works), and Python does not enforce immutability.

ABC: models work with `abc.ABC` and `@abc.abstractmethod`:

```python
class FooBarModel(BaseModel, abc.ABC):
    a: str
    b: int
    @abc.abstractmethod
    def my_abstract_method(self): ...
```

## Checked

Checked 2026-11-07. Re-read concepts/models in full (in chunks). Replaced the claim about Model().model_dump() for a ClassVar, which is not on the page, with what the page's example prints.

Method: documentation only; no commands were run.
