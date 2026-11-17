---
id: computing-software.software-engineering.pydantic.fix-type-and-parsing-validation-errors
name: fix-type-and-parsing-validation-errors
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validation-error-types, int-parsing, bool-parsing, string-type, int-from-float, bytes-type, collection-type-errors]
level: practitioner
status: docs-checked
description: "Decode Pydantic *_type and *_parsing error types (int, float, bool, str, bytes, list, dict, set, tuple, complex, Decimal) and what input triggers each."
sources:
  - https://docs.pydantic.dev/latest/errors/validation_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: map a `type` string from `ValidationError.errors()[i]['type']` to its cause. In the page's entries, `X_type` errors say the input's type is not valid for the field, and `X_parsing` errors say a string could not be parsed.

## Scalars
- `bool_parsing`: string not valid for coercion to bool (`Model(x='true')` is OK, `'test'` fails). `bool_type`: wrong type, e.g. `None`; also raised for strict fields when input is not a `bool`.
- `int_type`: e.g. `None` for an `int` field. `int_parsing`: `'test'` for `int`. `int_from_float`: a `float` such as `0.5` for an `int` field. `int_parsing_size`: a string outside the range Python `str` to `int` parsing permits (OK at `'1' * 4_300` digits, fails at `'1' * 4_301`, from Python or JSON).
- `float_type` (`None`), `float_parsing` (`'test'`).
- `finite_number`: value is infinite or too large for a 64-bit float.
- `string_type`: e.g. `1` for `str` (also strict mode). `string_unicode`: bytes like `b'\x81'` that cannot be parsed as Unicode.
- `bytes_type`: e.g. `123` for `bytes` (also strict mode). `bytes_invalid_encoding`: bytes invalid under the configured encoding, e.g. `model_config = {'val_json_bytes': 'hex'}` with `'a'` (odd number of hex digits).
- `decimal_parsing` (`'test'`), `decimal_type` (e.g. `[1, 2, 3]`, also strict), `fraction_parsing`, `fraction_type`.
- `complex_type`, and `complex_str_parsing` for JSON strings like `"abc"` that do not follow Python's complex rule.
- `none_required`: field typed `None` got a value. A field named `int` with default `None` and annotation `Optional[int]` (name collides with its type) can trigger it.

## Containers
`list_type`, `tuple_type` (also strict), `set_type`, `frozen_set_type`, `dict_type`, `deque_type`, `counter_type`, `ordered_dict_type`, `iterable_type`, `named_tuple_type`, `ellipsis_error`: input type not valid for that container. Others:
- `set_item_not_hashable`: unhashable item validated into a `set`/`frozenset` (one error per bad item).
- `iteration_error`: an exception while iterating (e.g. a generator that raises).
- `mapping_type`: a `Mapping` method such as `.items()` failed.
- `callable_type`: `ImportString[Callable[[Any], Any]]` given `'os.path'` (`'math:cos'` is OK).
- `is_instance_of` / `is_subclass_of`: input not an instance/subclass of the expected type (`arbitrary_types_allowed=True` types; `type[Nested]`).
- `json_invalid` / `json_type`: `Json` field given invalid JSON text / an unparsable type such as `None`.

## Related
Constraint failures are covered in fix-constraint-validation-errors.

## Checked

Checked 2026-11-07. Compared every claim with the validation errors page (errors/validation_errors.md): each scalar and container error type, the trigger inputs, the strict-mode notes, the `int_parsing_size` 4300 / 4301 digit limits and the `none_required` name-collision note. Reworded the opening naming-pattern sentence so it is attributed to the page entries rather than stated as a rule. All other entries confirmed.

Method: documentation only; no commands were run.
