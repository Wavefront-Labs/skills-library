---
id: computing-software.software-engineering.pydantic.fix-datetime-url-uuid-union-errors
name: fix-datetime-url-uuid-union-errors
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-validation-error-types, datetime-parsing, timezone-aware, url-scheme, uuid-version, union-tag-invalid, discriminator]
level: practitioner
status: docs-checked
description: "Decode Pydantic date, time, timezone, URL, UUID and discriminated-union error types such as date_from_datetime_inexact, timezone_aware, url_scheme, union_tag_invalid."
sources:
  - https://docs.pydantic.dev/latest/errors/validation_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: from an error `type`, find the cause for temporal, URL, UUID and discriminator failures.

## Dates and times
- `date_type`, `datetime_type`, `time_type`, `time_delta_type`: wrong input type (`None`); also raised for strict fields when input is not an instance.
- `date_parsing`, `datetime_parsing`: JSON string that cannot be parsed, with `Field(strict=True)` and `model_validate_json`.
- `date_from_datetime_parsing`: string not parseable for a `date` field (`'XX1494012000'`). `datetime_from_date_parsing`: string not parseable for `datetime` (`'2023-13-01'`, no 13th month).
- `date_from_datetime_inexact`: a `datetime` with nonzero time given to a `date` field; time components must all be zero.
- `time_parsing` (`'25:20:30.400'`), `time_delta_parsing` (`'t'`).
- `date_future` / `datetime_future`: `FutureDate` / `FutureDatetime` not in the future. `date_past` / `datetime_past`: `PastDate` / `PastDatetime` not in the past.
- `timezone_aware`: `AwareDatetime` field got a naive datetime. `timezone_naive`: `NaiveDatetime` field got a tz-aware one.
- `datetime_object_invalid`: something wrong with the object, e.g. a custom `tzinfo` without `utcoffset` on an `AwareDatetime`.

## URLs
- `url_parsing`: not parseable (`AnyUrl` given `'test'`). `url_scheme`: scheme invalid for the type (`HttpUrl` given `'ftp://example.com'`). `url_syntax_violation`: e.g. `'http:////example.com'` with `Field(strict=True)`. `url_too_long`: length greater than 2083. `url_type`: wrong input type.

## UUIDs
- `uuid_parsing`: bad string (`'12345678-124-1234-1234-567812345678'`). `uuid_type`: input not `str`, `bytes` or `UUID`. `uuid_version`: value does not match the UUID version of the field (page example: `UUID5` field given `'a6cc5730-2261-11ee-9c43-2eb5a363657c'`).

## Discriminated unions
With `Field(discriminator='pet_type')` on `BlackCat | WhiteCat`:
- `union_tag_invalid`: discriminator value is not one of the expected values (`{'pet_type': 'dog'}`).
- `union_tag_not_found`: no discriminator value can be extracted (`{'name': 'blackcat'}`).

## Other
- `literal_error`, `enum`: see fix-constraint-validation-errors.
- `recursion_loop`, `recursion_depth_exceeded`: see handle-cyclic-references.

## Checked

Checked 2026-11-07. Compared every claim with the validation errors page (errors/validation_errors.md): all date, time, timezone, URL, UUID and discriminator error types, their trigger inputs, the 2083 URL length limit, and the strict-field notes. All confirmed; nothing removed.

Method: documentation only; no commands were run.
