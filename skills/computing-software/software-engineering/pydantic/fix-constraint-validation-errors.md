---
id: computing-software.software-engineering.pydantic.fix-constraint-validation-errors
name: fix-constraint-validation-errors
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validation-error-types, greater-than, string-too-short, too-long, decimal-max-digits, multiple-of, field-constraints]
level: practitioner
status: docs-checked
description: "Match Pydantic constraint error types (greater_than, too_short, string_pattern_mismatch, decimal_*, multiple_of) to the Field argument that caused them."
sources:
  - https://docs.pydantic.dev/latest/errors/validation_errors/
  - https://docs.pydantic.dev/latest/errors/errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: from an error `type`, find which `Field(...)` or `StringConstraints` argument rejected the value.

## Numeric
| Error type | Field argument | Page example |
|---|---|---|
| `greater_than` | `gt` | `Field(gt=10)` with 10 |
| `greater_than_equal` | `ge` | `Field(ge=10)` with 9 |
| `less_than` | `lt` | `Field(lt=10)` with 10 |
| `less_than_equal` | `le` | `Field(le=10)` with 11 |
| `multiple_of` | `multiple_of` | `Field(multiple_of=5)` with 1 |

## Length
| Value kind | Too long | Too short |
|---|---|---|
| `str` | `string_too_long` (`max_length`) | `string_too_short` (`min_length`) |
| `bytes` | `bytes_too_long` | `bytes_too_short` |
| `list`/other collections | `too_long` | `too_short` |

Example: `x: list[int] = Field(max_length=3)` with `[1, 2, 3, 4]` gives `too_long`.

## Strings
- `string_pattern_mismatch`: value does not match `Field(pattern='test')`.
- `string_not_ascii`: `Annotated[str, StringConstraints(ascii_only=True)]` given `'café'`.

## Decimal
- `decimal_max_digits`: too many digits, `Field(max_digits=3)` with `'42.1234'`.
- `decimal_max_places`: too many digits after the point, `Field(decimal_places=3)` with `'42.1234'`.
- `decimal_whole_digits`: more digits before the point than `max_digits - decimal_places` (only when both are specified), `Field(max_digits=6, decimal_places=3)` with `'12345.6'`.

## Choice and presence
- `literal_error`: not one of `Literal['a', 'b']`.
- `enum`: value not a member of the enum field.
- `missing`: required field absent.
- `extra_forbidden`: extra input with `model_config['extra'] == 'forbid'`.

## Debugging recipe
```python
try:
    Model(x=10)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'greater_than'
```
Per the page examples, `Field(gt=10)` rejects 10 and `Field(lt=10)` rejects 10. The error's `ctx` carries the limit, e.g. `{'gt': 42}` (from the errors page).

See fix-type-and-parsing-validation-errors for wrong-type failures.

## Checked

Checked 2026-11-07. Compared every claim with the validation errors page (errors/validation_errors.md) and the validation errors page (errors/errors.md): each constraint error type with its `Field` argument and example input, the length table, `string_not_ascii`, the three `decimal_*` types, `literal_error`, `enum`, `missing`, `extra_forbidden`, and the `ctx` value `{'gt': 42}`. All confirmed; nothing removed.

Method: documentation only; no commands were run.
