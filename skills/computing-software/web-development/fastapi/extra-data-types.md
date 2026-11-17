---
id: computing-software.web-development.fastapi.extra-data-types
name: extra-data-types
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, data-types, uuid, datetime, timedelta, decimal, frozenset, bytes]
level: intro
status: docs-checked
description: "Use UUID, datetime, date, time, timedelta, frozenset, bytes and Decimal in FastAPI parameters and know how each is represented in requests and responses."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/extra-data-types.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extra data types

They keep editor support, conversion of request and response data, validation and automatic docs. Inside the function you get the natural Python type, so normal date arithmetic works.

## Representations
- `UUID`: a `str`.
- `datetime.datetime`: ISO 8601 `str` (like `2008-09-15T15:53:00+05:00`).
- `datetime.date`: ISO 8601 `str` (like `2008-09-15`).
- `datetime.time`: ISO 8601 `str` (like `14:23:55.003`).
- `datetime.timedelta`: a `float` of total seconds. Pydantic can also represent it as an ISO 8601 time diff.
- `frozenset`: same as `set`. Requests read a list, drop duplicates and convert; responses become a `list`; the schema marks `uniqueItems`.
- `bytes`: treated as `str`; schema is a `str` with `binary` format.
- `Decimal`: handled as a `float`.

Other valid types are listed on Pydantic's data types page.

## Verify
Call with an ISO string and confirm the function sees the Python type.

## Checked

2026-11-08: Read the Extra Data Types page (representation of UUID, datetime, date, time, timedelta, frozenset, bytes, Decimal). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
