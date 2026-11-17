---
id: computing-software.software-engineering.pydantic.validate-arguments-schema
name: validate-arguments-schema
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-arguments-schema, generate-arguments-schema, schema-validator, validate-call, experimental, pydantic-core, signature]
level: advanced
status: docs-checked
description: "Validate a function arguments without calling it using experimental generate_arguments_schema and a pydantic-core SchemaValidator, skipping parameters by callback."
sources:
  - https://docs.pydantic.dev/latest/concepts/experimental/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validate a callable's arguments without calling it (experimental)

Goal: validate argument data (for example JSON loaded from elsewhere) against a function signature, where `@validate_call` would require actually calling the function.

`generate_arguments_schema()` from `pydantic.experimental.arguments_schema` builds a core schema, used with `pydantic_core.SchemaValidator`. Unlike `@validate_call`, the underlying callable is not called.

## Basic use

```python
from pydantic_core import SchemaValidator
from pydantic.experimental.arguments_schema import generate_arguments_schema

def func(p: bool, *args: str, **kwargs: int) -> None: ...

arguments_schema = generate_arguments_schema(func=func)
val = SchemaValidator(arguments_schema, config={'coerce_numbers_to_str': True})

args, kwargs = val.validate_json(
    '{"p": true, "args": ["arg1", 1], "kwargs": {"extra": 1}}'
)
print(args, kwargs)
#> (True, 'arg1', '1') {'extra': 1}
```

The JSON input is an object keyed by parameter name, with `args` for `*args` and `kwargs` for `**kwargs`. The result is an `(args, kwargs)` pair. Here `coerce_numbers_to_str` turns the `1` in `args` into `'1'`.

## Get a dict of bound arguments

```python
from inspect import signature
signature(func).bind(*args, **kwargs).arguments
#> {'p': True, 'args': ('arg1', '1'), 'kwargs': {'extra': 1}}
```

## Skip parameters with `parameters_callback`

The callback is called for every parameter with `(index, name, annotation)`. Returning `'skip'` leaves that parameter out of the schema:

```python
def skip_first_parameter(index: int, name: str, annotation: Any) -> Any:
    if index == 0:
        return 'skip'

arguments_schema = generate_arguments_schema(
    func=func, parameters_callback=skip_first_parameter
)
val = SchemaValidator(arguments_schema)
args, kwargs = val.validate_json('{"args": ["arg1"], "kwargs": {"extra": 1}}')
#> ('arg1',) {'extra': 1}
```

Note: the feature lives in the experimental module, so it is subject to change or removal (see the experimental features page).

## Checked

Checked 2026-11-07. Re-read concepts/experimental in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
