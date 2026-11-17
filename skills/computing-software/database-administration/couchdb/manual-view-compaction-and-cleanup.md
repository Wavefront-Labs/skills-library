---
id: computing-software.database-administration.couchdb.manual-view-compaction-and-cleanup
name: manual-view-compaction-and-cleanup
category: computing-software
field: database-administration
product: couchdb
tags: [compaction, views, view-cleanup, design-documents, md5]
level: practitioner
status: docs-checked
description: "Compact view indexes per design document with POST /{db}/_compact/{ddoc} and remove outdated index files with POST /{db}/_view_cleanup."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/compaction.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Views are compacted in groups, one per design document:

```
curl -H "Content-Type: application/json" -X POST http://adm:pass@localhost:5984/dbname/_compact/ddoc-name
```

This compacts the view index of the current version of that design document. The response is `202` with `{"ok":true}`, and a compaction background task is created, as with database compaction.

**View cleanup.** Index files on disk are named after the MD5 hash of the view definition. When you change a view, the old index files stay on disk. To delete index files whose view definition no longer exists:

```
curl -H "Content-Type: application/json" -X POST http://adm:pass@localhost:5984/dbname/_view_cleanup
```

Response: `{"ok":true}`.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/compaction page (Manual View Compaction, Views cleanup): per design document compaction, 202 response, MD5-named index files, _view_cleanup. Nothing removed.

Method: documentation only; no commands were run.
