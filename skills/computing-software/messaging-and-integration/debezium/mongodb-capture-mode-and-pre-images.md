---
id: computing-software.messaging-and-integration.debezium.mongodb-capture-mode-and-pre-images
name: mongodb-capture-mode-and-pre-images
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mongodb, capture-mode, pre-image, update-events]
level: advanced
status: docs-checked
description: "Use capture.mode and MongoDB 6.0 pre-images to get full documents and before values in MongoDB change events."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mongodb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`capture.mode` (default `change_streams_update_full`) decides what update events contain:

- `change_streams`: updates carry no full document and no `before` field.
- `change_streams_update_full`: updates include the full document in `after`, with no `before`.
- `change_streams_update_full_with_pre_image`: full document plus a `before` field.
- `change_streams_with_pre_image`: pre-image without a fetched full document.

`capture.mode.full.update.type` (default `lookup`) sets how the full document is fetched; `post_image` needs MongoDB 6.0 or later.

Gotcha with full-document modes: the connector requests the document only after receiving the update, so a quick later update can make `updateDescription` and `after` disagree. The connector receives the document as modified by the later update.

Pre-images need MongoDB 6.0 or later. Enable `changeStreamPreAndPostImages` on the collection using `db.createCollection()`, `create` or `collMod`, then pick one of the `*_with_pre_image` modes.

Limit: a change stream event cannot exceed 16 megabytes, and pre-images make that more likely, which can cause failures.

Related: `field.exclude.list` takes fully qualified field names such as `databaseName.collectionName.fieldName.nestedFieldName`, where database and collection may use `*`.

Check: update a document and confirm the event has the `before` field you expect.

## Checked

2026-11-03. Page used: the Debezium mongodb connector reference, https://debezium.io/documentation/reference/stable/connectors/mongodb.html.
Confirmed against it: the four capture.mode values and default, capture.mode.full.update.type, the update/after inconsistency note, MongoDB 6.0 pre-images and changeStreamPreAndPostImages, the 16 MB limit, field.exclude.list format.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
