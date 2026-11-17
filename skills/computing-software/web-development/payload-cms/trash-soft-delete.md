---
id: computing-software.web-development.payload-cms.trash-soft-delete
name: trash-soft-delete
category: computing-software
field: web-development
product: payload-cms
tags: [trash, soft-delete, deletedat, restore-documents]
level: intro
status: docs-checked
description: "Enable soft deletes with trash true so deleted documents get deletedAt and can be restored from a Trash view."
sources:
  - https://payloadcms.com/docs/trash/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trash (soft delete)

Goal: let editors recover deleted documents.

```ts
export const Posts: CollectionConfig = {
  slug: 'posts',
  trash: true,
  fields: [{ name: 'title', type: 'text' }],
}
```

Payload injects a `deletedAt` timestamp, set on soft delete and cleared on restore. The Admin Panel adds a Trash view at `/collections/:collectionSlug/trash` listing documents with a `deletedAt` value, with restore and permanent delete actions.

Trashed documents are excluded from normal queries. Pass `trash: true` (Local API option, REST `?trash=true`, GraphQL argument) to include them in find, findByID, update, delete and the version finds; to get only trashed documents also add `where: { deletedAt: { exists: true } }`.

Gotcha: trash respects the collection's `delete` access function. When trashing, `data.deletedAt` is set in that function; on a permanent delete `data` is undefined, so you can let editors trash but only admins delete permanently. A trashed document cannot have a version restored until the document itself is restored.

Verify: delete a document, find it in the Trash view, and restore it.

## Checked

2026-11-04. Read trash/overview. Confirmed: trash: true on the collection, the injected deletedAt field set on soft delete and cleared on restore, the Trash view route /collections/:collectionSlug/trash with restore, delete and empty-trash actions, support in Local, REST and GraphQL, the operations that honour trash, trash: true including soft-deleted documents and needing a deletedAt exists where clause to return only trashed ones, the delete access control receiving data.deletedAt when trashing and undefined data on permanent delete, and the version-restore restriction. Removed: the unique-index claim (not on the page) and the Live Preview wording (the page does not mention it).
Method: documentation only; no commands were run.
