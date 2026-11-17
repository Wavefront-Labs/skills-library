---
id: computing-software.database-administration.couchdb.deleted-docs-and-id-size
name: deleted-docs-and-id-size
category: computing-software
field: database-administration
product: couchdb
tags: [performance, deleted-documents, tombstones, document-ids, database-rotation]
level: advanced
status: docs-checked
description: "Why deleted documents and long or random _id values enlarge CouchDB databases, and how to mitigate with database rotation and short sequential ids."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/performance.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Deletes.** A DELETE creates a new revision holding `_id`, `_rev` and `_deleted`. It remains even after compaction so the deletion can replicate. Deleted documents still affect view build times, PUT and DELETE times and file size, as they grow the B+Tree. The number of deleted documents is shown in the database information. For short-lived data (log entries, message queues), periodically switch to a new database and delete the old one once its entries have all expired.

**Document IDs.** File size depends on `_id` sizes: the id appears in the document and is duplicated in the binary tree used to find it. The page cites one user who moved from 16 byte ids to 4 byte ids and saw a database go from 21GB to 4GB with 10 million documents.

- Sequential, at least sorted, ids insert faster than random ids.
- Consider generating ids yourself, allocating sequentially, with a compact encoding: 8 bytes need 16 hex digits but only 11 characters in base64url (no padding).

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/performance page (DELETE operation, Document's ID): the deletion revision and compaction, effects on view build and request times and file size, database rotation advice, the 16-byte to 4-byte id example (21GB to 4GB, 10 million documents), sequential ids, hex versus base64url. Removed the doc_del_count field name, which the page does not name.

Method: documentation only; no commands were run.
