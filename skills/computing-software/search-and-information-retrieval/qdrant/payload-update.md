---
id: computing-software.search-and-information-retrieval.qdrant.payload-update
name: payload-update
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [set-payload, overwrite-payload, delete-payload, clear, pl-update]
level: practitioner
status: docs-checked
description: "Set, overwrite, delete and clear payload on Qdrant points by id or filter, including updating one nested key with the key parameter."
sources:
  - https://qdrant.tech/documentation/manage-data/payload/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Payload operations act on points selected by id (`points`) or by `filter`; you do not need to know ids.

- Set payload sets only the given values and keeps other fields:

```http
POST /collections/{collection_name}/points/payload
{ "payload": { "color": "red" }, "points": [1, 2] }
```

- Overwrite fully replaces the existing payload:

```http
PUT /collections/{collection_name}/points/payload
{ "payload": { "color": "red" }, "points": [1] }
```

- Delete selected keys:

```http
POST /collections/{collection_name}/points/payload/delete
{ "keys": ["color"], "points": [1] }
```

- Clear removes all payload from the selected points: `POST /collections/{collection_name}/points/payload/clear`.

Selecting by filter, for example:

```json
{ "payload": { "color": "red" }, "filter": { "must": [ { "key": "color", "match": { "value": "blue" } } ] } }
```

To modify one nested key (available as of v1.8.0), pass `key` to set payload:

```json
{ "payload": { "nested_property": "qux" }, "key": "property1", "points": [1] }
```

Given `property1.nested_property` and `property2.nested_property`, this changes only `property1.nested_property` and leaves `property2` alone.

Prefer set over overwrite when other jobs also write fields on the same points.

## Checked

2026-11-08. Confirmed against the Payload page: set, overwrite, clear and delete endpoints and methods, selection by ids or filter, the `key` parameter and its v1.8.0 version gate with the documented result. Page read by section; client-language tabs skipped. Corrected: the nested example used a `location`/`city` shape the docs do not show, replaced with the documented `property1` shape. Removed unconfirmed claims about the write-ahead log and the `wait` parameter, and about a payload index speeding up filter selection.
Method: documentation only; no commands were run.
