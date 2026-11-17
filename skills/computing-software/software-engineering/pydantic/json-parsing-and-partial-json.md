---
id: computing-software.software-engineering.pydantic.json-parsing-and-partial-json
name: json-parsing-and-partial-json
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-json-parsing, model-validate-json, from-json, partial-json, cache-strings, jiter, python]
level: practitioner
status: docs-checked
description: "Parse JSON with Pydantic: model_validate_json with strict mode, partial JSON via from_json allow_partial for LLM output, and the cache_strings setting."
sources:
  - https://docs.pydantic.dev/latest/concepts/json/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON parsing, partial JSON, string caching

Goal: validate JSON text directly and handle truncated or streamed JSON.

## `model_validate_json` and strict

Builtin JSON parsing (`BaseModel.model_validate_json`, `TypeAdapter.validate_json`, `pydantic_core.from_json`) gives performance gains, custom errors and `strict` support. In strict mode JSON text still works for types JSON lacks (dates, tuples):

```python
class Event(BaseModel):
    model_config = ConfigDict(strict=True)
    when: date
    where: tuple[int, int]

Event.model_validate_json('{"when": "1987-01-28", "where": [51, -1]}')   # ok
Event.model_validate({'when': '1987-01-28', 'where': [51, -1]})          # ValidationError
```

Since v2.5.0 parsing uses `jiter`, almost compatible with `serde`, and additionally supports `inf` and `NaN`. For duplicate keys the last value wins: `'{"x": 1, "x": 2}'` gives `x=2`.

## Partial JSON (v2.7+)

```python
from pydantic_core import from_json

from_json('["aa", "bb", "c', allow_partial=True)   # ['aa', 'bb']
from_json('["aa", "bb", "c', allow_partial=False)  # ValueError: EOF while parsing a string at line 1 column 15
```

`allow_partial` defaults to `False`. It also works for dicts: `'{"breed": "lab", "name": "fluffy", "friends": ["buddy", "spot", "rufus"], "age'` parses without the trailing incomplete key. `model_validate_json` does not take this yet, so combine: `Dog.model_validate(from_json(text, allow_partial=True))`.

For reliability all model fields should have defaults. To tolerate cut-off nested values, wrap with a validator that turns only `missing` errors into the default:

```python
def default_on_error(v, handler) -> Any:
    try:
        return handler(v)
    except ValidationError as exc:
        if all(e['type'] == 'missing' for e in exc.errors()):
            raise pydantic_core.PydanticUseDefault()
        raise

bar: Annotated[tuple[str, int] | None, WrapValidator(default_on_error)] = None
```

Useful for validating LLM output.

## `cache_strings` (v2.7.0+)

Set in model config or `from_json`. Values: `True`/`'all'` (default), `'keys'` (only with `from_json` or the `Json` type), `False`/`'none'`. Faster, slightly more memory. Cache: 16,384 entries, only strings shorter than 64 characters. If your data has few repeated strings, `cache_strings=False` may be faster.

Serialization: see `model_dump_json`, `TypeAdapter.dump_json`, `pydantic_core.to_json`.

## Checked

Checked 2026-11-07. Compared every claim with the JSON concepts page (concepts/json.md): builtin parsing benefits, the strict `Event` example, `jiter` from v2.5.0 with `inf` and `NaN`, last-duplicate-key-wins, `allow_partial` (v2.7, default `False`), the combined `from_json` plus `model_validate` approach, the defaults tip with `default_on_error`, and `cache_strings` values, cache size 16,384 and the 64-character limit. All confirmed; nothing removed.

Method: documentation only; no commands were run.
