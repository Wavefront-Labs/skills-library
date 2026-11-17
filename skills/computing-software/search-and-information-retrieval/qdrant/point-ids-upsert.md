---
id: computing-software.search-and-information-retrieval.qdrant.point-ids-upsert
name: point-ids-upsert
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [points, upsert, ids, uuid, idempotent, pts-upsert]
level: intro
status: docs-checked
description: "Insert or overwrite Qdrant points by ID with upsert; IDs are unsigned 64-bit integers or UUIDs and loading is idempotent."
sources:
  - https://qdrant.tech/documentation/manage-data/points/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A point has an id, a vector (or vectors), and an optional payload. Point IDs are 64-bit unsigned integers or UUIDs; a UUID string can be used instead of a numeric id in any request. Accepted UUID string forms include simple (`936DA01F9ABD4d9d80C702AF85C822A8`), hyphenated and urn.

```http
PUT /collections/{collection_name}/points
{
  "points": [
    { "id": 1, "vector": [0.9, 0.1], "payload": { "city": "Paris" } },
    { "id": "5c56c793-69f3-4fbf-87e6-c4bf54c28c26", "vector": [0.1, 0.9] }
  ]
}
```

Behaviour from the docs:

- Every point modification is asynchronous and happens in two steps. First the operation is written to the write-ahead log; after that the service does not lose the data even on power loss.
- All Qdrant APIs, including point loading, are idempotent: repeating the same call equals one execution, and points with the same id are overwritten when re-uploaded. This makes re-delivery from a message queue without exactly-once guarantees safe.
- Python client: `upload_points` (as of v1.7.1; it replaced the deprecated `upload_records`) and `upload_collection` add parallelization, retries and lazy batching for large loads. If ids are not provided the client generates random UUIDs.

Pick ids you can reconstruct from source data so a re-run of an import overwrites rather than duplicates.

## Checked

2026-11-08. Confirmed against the Points page: id types and UUID forms, two-step asynchronous write and WAL durability, idempotence, upload helpers and v1.7.1 note, random UUIDs when ids are omitted. Page read by section (intro, IDs, batches, Python client, idempotence); other sections skipped. Removed unconfirmed claims: UUID v5 derivation advice as a documented practice, and that a just-written point may take a moment to be searchable.
Method: documentation only; no commands were run.
