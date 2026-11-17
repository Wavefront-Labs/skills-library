---
id: computing-software.software-engineering.api-design.json-merge-patch-vs-json-patch
name: json-merge-patch-vs-json-patch
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, rest, json-merge-patch, json-patch, http-patch, put-vs-patch, partial-update]
level: practitioner
status: verified
description: "Choose PUT, JSON Merge Patch (RFC 7396) or JSON Patch (RFC 6902) for updates, handle nulls and arrays correctly, and guard concurrent edits with ETags."
sources: ["https://www.rfc-editor.org/rfc/rfc7396", "https://www.rfc-editor.org/rfc/rfc6902", "https://www.rfc-editor.org/rfc/rfc5789", "https://www.rfc-editor.org/rfc/rfc9110#name-put"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PUT vs PATCH: JSON Merge Patch and JSON Patch

| Method | Semantics | Use when |
|---|---|---|
| `PUT` | replace whole representation; missing fields reset | small resources, client owns all fields |
| `PATCH` + `application/merge-patch+json` | send only changed fields; `null` deletes | default for JSON APIs |
| `PATCH` + `application/json-patch+json` | ordered ops (`add/remove/replace/move/copy/test`) | array element edits, atomic conditional changes |
| `PATCH` + field mask (AIP-134) | body + `update_mask=title,labels` | protobuf/gRPC APIs |

Checked: a hand-written RFC 7396 merge, and the `jsonpatch` library for RFC 6902 (test op, remove, add `/-`, `~0`/`~1` escapes, atomic rollback on a failing `test`) behaved as described; RFC 5789 says the server must apply the entire patch atomically and lists 400 (malformed), 415 (unsupported), 422 (unprocessable), 409 (conflicting state) and 412-style conflicting-modification handling for `If-Match`; RFC 6585 defines 428.

## Merge Patch (RFC 7396)
```json
PATCH /users/u1   Content-Type: application/merge-patch+json
{"nickname": null, "address": {"city": "Leeds"}}
```
- `null` removes the field; nested objects merge recursively; **arrays replace wholesale**.
- Cannot set a field to JSON `null` as a value. If null is meaningful, use JSON Patch or field masks.
- Deserialising into a typed DTO loses the difference between "absent" and "null": parse into a
  generic map/JsonNode first, or use `Optional`/`JsonNullable` wrappers.

## JSON Patch (RFC 6902)
```json
[{"op":"test","path":"/version","value":7},
 {"op":"remove","path":"/tags/2"},
 {"op":"add","path":"/tags/-","value":"urgent"}]
```
- Applied atomically: any failing op (including `test`) aborts the whole patch -> 409/422.
- Paths are JSON Pointers (RFC 6901): escape `~` as `~0`, `/` as `~1`.
- Index-based array ops race with concurrent edits; pair with `If-Match`.

## Always
- Validate the patched result against the full schema, then enforce field permissions on what
  changed (no patching `role` or `owner_id`: see mass assignment).
- Concurrency: return `ETag`, require `If-Match` on PATCH/PUT, respond **412** on mismatch,
  **428** if missing and you require it.
- Advertise support: `Accept-Patch: application/merge-patch+json, application/json-patch+json`.
- Unsupported patch type: 415.
