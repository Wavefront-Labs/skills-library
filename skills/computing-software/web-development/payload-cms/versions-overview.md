---
id: computing-software.web-development.payload-cms.versions-overview
name: versions-overview
category: computing-software
field: web-development
product: payload-cms
tags: [versions, version-history, maxperdoc, readversions]
level: practitioner
status: docs-checked
description: "Understand versions: enabled by default with maxPerDoc 100, stored in separate version collections, restore support, and the three workflow levels."
sources:
  - https://payloadcms.com/docs/versions/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Versions overview

Goal: keep an audit history and enable restore.

Versions are enabled by default for every collection and global (100 kept, drafts disabled). Collections cap history with `maxPerDoc`, globals with `max`; both must be integers and `0` keeps all versions. Opt out with `versions: false`. Versions are stored in a separate collection or global, so the shape of your data does not change.

With versions you can: keep an audit log including which user made each change, restore prior states, build draft preview, control who sees drafts via access control, add autosave, and schedule publishing.

Three levels:

1. Versions on, drafts off - a new version is saved on every update (good for audit logs, for example on users).
2. Versions and drafts - control which documents are published and which are drafts.
3. Versions, drafts and autosave - the Admin saves drafts automatically while you edit.

```ts
export const Pages: CollectionConfig = {
  slug: 'pages',
  versions: { maxPerDoc: 50, drafts: true },
  fields: [],
}
```

Use `access.readVersions` to control who can read versions; it also restricts the Admin version views.

Version operations: `payload.findVersions`, `findVersionByID` and `restoreVersion` (globals: `findGlobalVersions`, `findGlobalVersionByID`, `restoreGlobalVersion`). REST is `GET /api/{slug}/versions`, `GET /api/{slug}/versions/:id` and `POST /api/{slug}/versions/:id` to restore (globals under `/api/globals/{slug}/versions`). Versions live in a `_slug_versions` database collection.

Verify: edit a document twice and see two entries in its Versions tab.

## Checked

2026-11-04. Read versions/overview. Confirmed: versions enabled by default for collections and globals, versions: false to opt out, separate storage, the capabilities list, the three levels, maxPerDoc default 100 and 0 saving all versions, drafts as true or an object, the _slug_versions naming, the version operations in REST, GraphQL and Local API, and readVersions access restricting Admin version views. Corrected: globals use max instead of maxPerDoc.
Method: documentation only; no commands were run.
