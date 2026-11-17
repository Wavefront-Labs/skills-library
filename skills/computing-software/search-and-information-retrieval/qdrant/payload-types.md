---
id: computing-software.search-and-information-retrieval.qdrant.payload-types
name: payload-types
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [payload, json, data-types, keyword, pl-types]
level: practitioner
status: docs-checked
description: "Payload value types Qdrant filters on: integer, float, bool, keyword, geo, datetime and uuid, with array and type-mismatch behaviour."
sources:
  - https://qdrant.tech/documentation/manage-data/payload/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A payload is any information representable as JSON, stored alongside a vector. For filtering, Qdrant supports these value types:

- `integer`: 64-bit integer, from -9223372036854775808 to 9223372036854775807
- `float`: 64-bit floating point number
- `bool`: true or false
- `keyword`: a string value
- `geo`: an object with `lon` (longitude) and `lat` (latitude), e.g. `{ "lon": 52.52, "lat": 13.405 }`
- `datetime`: RFC 3339. Without a timezone, UTC is assumed. Seconds can have up to 6 decimals, so the finest granularity is microseconds.
- `uuid`: functionally like `keyword`, but stored internally as the parsed UUID

```json
{ "id": 1, "vector": [0.1, 0.2],
  "payload": { "name": "Hotel", "rating": 4.5, "open": true,
               "created": "2026-01-02T03:04:05Z", "tags": ["spa", "bar"] } }
```

Behaviour:

- Filters check only values whose stored type fits the condition; a value of the wrong type is treated as not satisfied. A range condition on string data returns nothing.
- For arrays (multiple values of the same type), a filter succeeds if at least one element meets the condition.
- A UUID string takes 36 bytes, while the numeric form is 128 bits (16 bytes). The docs recommend the `uuid` index type for payload-heavy collections to save RAM and improve search performance.
- Filters are fast when the filtered field has a payload index (see the payload index skills).

## Checked

2026-11-08. Confirmed against the Payload page: the type list and definitions, integer range, datetime format and microsecond precision, array and mismatch behaviour, uuid sizes and recommendation. Page read by section (types, update and index parts); client-language tabs skipped. Removed unconfirmed claims: `text` as a payload value type on this page, `on_disk_payload` defaulting to true, and the rule that a field must hold one type across points.
Method: documentation only; no commands were run.
