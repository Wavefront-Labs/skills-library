---
id: computing-software.web-development.payload-cms.document-locking
name: document-locking
category: computing-software
field: web-development
product: payload-cms
tags: [document-locking, locked-documents, lockdocuments, concurrent-editing]
level: intro
status: docs-checked
description: "Prevent concurrent edits with document locking, configure lockDocuments duration or disable it, and enforce locks in the Local API."
sources:
  - https://payloadcms.com/docs/admin/locked-documents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Document locking

Goal: stop two editors overwriting each other.

Locking is on by default. When a user starts editing a document in the Admin Panel it is locked for them; others can view read-only, take over, or return to the dashboard. The lock expires after inactivity (default duration 300 seconds).

```ts
export const Posts: CollectionConfig = {
  slug: 'posts',
  lockDocuments: {
    duration: 600,   // seconds
  },
  fields: [],
}
```

Disable per collection or global with `lockDocuments: false`.

Local API: locks are ignored by default (`overrideLock: true`); pass `overrideLock: false` to refuse operations on a locked document. Locks affect Local and REST API update and delete operations, including on globals.

## Checked

2026-11-04. Read admin/locked-documents in the payloadcms/payload docs. Confirmed: on by default, lockDocuments duration and false, overrideLock default true. Added: 300 second default and API scope. Removed: the browser verify step.
Method: documentation only; no commands were run.
