---
id: computing-software.software-engineering.pydantic.partial-validation-streaming
name: partial-validation-streaming
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-partial-validation, experimental-allow-partial, typeadapter, streaming, llm, partial-json, jiter]
level: advanced
status: docs-checked
description: "Validate incomplete JSON or Python data, such as streamed LLM output, with TypeAdapter and experimental_allow_partial, including its modes and limitations."
sources:
  - https://docs.pydantic.dev/latest/concepts/experimental/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial validation of incomplete input (experimental, v2.10+)

Goal: validate a still-arriving JSON string (e.g. a streamed LLM response) or a Python object built from incomplete data. The page calls the implementation a proof of concept.

## Usage

Pass `experimental_allow_partial` to `TypeAdapter.validate_json()`, `validate_python()` or `validate_strings()`. Values (default `False`):

- `False` / `'off'`: disabled
- `True` / `'on'`: enabled, no trailing strings
- `'trailing-strings'`: also keep an incomplete trailing string

```python
class Foobar(TypedDict):
    a: int
    b: NotRequired[float]
    c: NotRequired[Annotated[str, MinLen(5)]]

ta = TypeAdapter(list[Foobar])
ta.validate_json('[{"a": 1, "b"', experimental_allow_partial=True)            # [{'a': 1}]
ta.validate_json('[{"a": 1, "b": 1.0, "c": "abcd', experimental_allow_partial=True)  # [{'a': 1, 'b': 1.0}]
ta.validate_json('[{"b": 1.0, "c": "abcde"', experimental_allow_partial=True)  # []  (a is required)
ta.validate_json('[{"a": 1, "b": 1.0, "c": "abcdefg', experimental_allow_partial='trailing-strings')
# [{'a': 1, 'b': 1.0, 'c': 'abcdefg'}]
```

With `'trailing-strings'`, `'{"a": "hello", "b": "wor'` validates as `{'a': 'hello', 'b': 'wor'}`.

## How it works

1. The jiter parser supports partial JSON; the flag is passed to it as `allow_partial`. For pure partial JSON parsing you can use jiter directly or `pydantic_core.from_json` with `allow_partial`.
2. Pydantic ignores ALL errors in the last element of the input (last item of a sequence or last value of a mapping), since truncation can break `MinLen(5)`, `Ge(10)` or required-field checks.

It guarantees a valid instance of the requested type or a validation error.

## Limitations

- TypeAdapter only; not available via `BaseModel` entry points.
- Only `list`, `set`, `frozenset`, `dict[X, Y]` and `TypedDict` (only non-required fields may be missing) understand partial input; other types validate all-or-nothing. A `BaseModel` does not forward the instruction, so a list field inside a model fails with a normal `string_too_short` style error rather than dropping the last item.
- Complete-but-invalid JSON can be accepted: `{"a": 1, "b": "12"}` is indistinguishable from the truncated `{"a": 1, "b": "12`, so both give `{'a': 1}`.
- Clearly invalid data passes if the error is in the last element: `list[Annotated[int, Ge(10)]]` with `[20, 30, 4]` gives `[20, 30]`; `list[int]` with `[1, 2, 'wrong']` gives `[1, 2]`.

## Checked

Checked 2026-11-07. Compared every claim with the experimental features page (concepts/experimental.md): v2.10 partial validation, the `experimental_allow_partial` values and default, the `Foobar` example results, `'trailing-strings'` behaviour, jiter `allow_partial`, ignoring errors in the last element, the TypeAdapter-only limitation, supported types, the BaseModel non-forwarding case, and the two accepted-invalid-input cases. All confirmed; nothing removed.

Method: documentation only; no commands were run.
