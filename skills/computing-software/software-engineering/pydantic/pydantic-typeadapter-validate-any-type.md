---
id: computing-software.software-engineering.pydantic.pydantic-typeadapter-validate-any-type
name: pydantic-typeadapter-validate-any-type
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-type-adapter, typeadapter, validate-python, dump-json, defer-build, rebuild, typeddict]
level: practitioner
status: docs-checked
description: "Validate, serialize and rebuild non-BaseModel types with Pydantic TypeAdapter, reuse instances for speed, and defer builds for forward refs."
sources:
  - https://docs.pydantic.dev/latest/concepts/type_adapter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: validate or dump types that are not `BaseModel`s, such as `list[User]`, a `TypedDict`, dataclasses or primitives, without writing a model.

```python
class User(TypedDict):
    name: str
    id: int

user_list_adapter = TypeAdapter(list[User])
user_list = user_list_adapter.validate_python([{'name': 'Fred', 'id': '3'}])
#> [{'name': 'Fred', 'id': 3}]
user_list_adapter.validate_python([{'name': 'Fred', 'id': 'wrong', 'other': 'no'}])
# 1 validation error for list[User]
# 0.id  Input should be a valid integer ... [type=int_parsing]
user_list_adapter.dump_json(user_list)
#> b'[{"name":"Fred","id":3}]'
```

Notes:
- `dump_json` returns `bytes`, unlike `BaseModel.model_dump_json`, which returns `str`. Decode if you need a `str`.
- Same idea as `BaseModel.model_validate` but for any Pydantic-compatible type, for example `TypeAdapter(list[Item]).validate_python(item_data)` where `item_data` is JSON from an API.
- The page also lists JSON schema generation as a use, and its `defer_build` example passes a `config=` argument.
- Do not use `TypeAdapter` as a type annotation for fields of a `BaseModel`, even though it overlaps with `RootModel`.

Performance: creating a `TypeAdapter` analyzes the type and builds a pydantic-core schema, which has non-trivial overhead. Create one adapter per type once and reuse it in loops or performance-critical code.

Deferred build (since v2.10): for forward references or expensive schema builds, set `defer_build` so the core schema is built on first use (validation or serialization), or call `rebuild()` yourself:

```python
ta = TypeAdapter('MyInt', config=ConfigDict(defer_build=True))

# some time later, the forward reference is defined
MyInt = int

ta.rebuild()
assert ta.validate_python(1) == 1
```

Validation failures from adapters are the same structured `ValidationError` as for models, so production tooling that records them (such as Logfire) captures these too.

## Checked

Checked 2026-11-07. Re-read concepts/type_adapter in full. Removed the validate_json bullet, which the page does not name, and reworded the config= note to what the page shows (a defer_build example passing config).

Method: documentation only; no commands were run.
