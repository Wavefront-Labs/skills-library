---
id: computing-software.software-engineering.pydantic.dump-models-python-json
name: dump-models-python-json
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-serialization-modes, model-dump, model-dump-json, serialization, json, pickle, by-alias]
level: practitioner
status: docs-checked
description: "Convert Pydantic models to dicts or JSON strings with model_dump and model_dump_json, choose python vs json mode, iterate a model, and pickle it."
sources:
  - https://docs.pydantic.dev/latest/concepts/serialization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dump a Pydantic model to a dict or JSON string

Goal: turn a model into a dict, a JSON-compatible dict, or a JSON string.

Pydantic uses "serialize" and "dump" interchangeably. Models (and any type via a TypeAdapter) serialize in two modes: Python and JSON.

## Python mode: `model_dump()`

- Recursively converts models (and model-like types such as dataclasses) to dicts. Exception: a root model dumps its root value directly.
- The output may hold non-JSON types: a `tuple[int, ...]` field dumps as a tuple.
- `model_dump(by_alias=True)` uses `serialization_alias` keys (for example `Field(serialization_alias='foo_alias')`).
- `model_dump(mode='json')` forces JSON-compatible types, so the tuple becomes `[1, 2]`.
- For non-model types use `TypeAdapter.dump_python()`.

```python
m.model_dump()               # {'banana': 3.14, 'foo': 'hello', 'bar': {'whatever': (1, 2)}}
m.model_dump(mode='json')    # {'banana': 3.14, 'foo': 'hello', 'bar': {'whatever': [1, 2]}}
```

## JSON mode: `model_dump_json()`

- Returns a JSON-encoded string; `indent=2` pretty-prints.
- A `datetime(2032, 6, 1, 12, 13, 14)` field comes out as `"2032-06-01T12:13:14"`.
- Beyond what the standard library `json` supports, Pydantic handles dates and times, `UUID`, sets, and more.
- An unsupported type raises `pydantic_core.PydanticSerializationError`. The page notes this often appears only when an object is actually serialized (commonly when building a response), so it is easy to miss until production.
- For non-model types use `TypeAdapter.dump_json()`.

## Iterating a model

`for name, value in model` yields `(field_name, field_value)` pairs. Values are left as is, so sub-models are not converted: `dict(m)` gives `{'banana': 3.14, 'foo': 'hello', 'bar': BarModel(whatever=123)}`. Root models do get converted to a dict with the key `'root'`.

## Pickling

Models support efficient pickling: `pickle.dumps(m)` then `pickle.loads(data)` returns an equal model (`a='hello' b=123` in the page example).

## Gotchas

- Use `mode='json'` on `model_dump` when you need JSON-safe values but still want a dict.
- `dict(model)` is shallow; `model_dump()` is recursive.

## Checked

Checked 2026-11-07. Compared every claim with the serialization concepts page (concepts/serialization.md): serialize/dump terminology, Python and JSON modes, root-model exception, `by_alias` with `serialization_alias`, `mode='json'` turning the tuple into a list, `TypeAdapter.dump_python` / `dump_json`, `PydanticSerializationError`, iteration and `dict(m)` results, root model key `'root'`, and pickling. All confirmed; nothing removed.

Method: documentation only; no commands were run.
