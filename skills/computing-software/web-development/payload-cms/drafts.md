---
id: computing-software.web-development.payload-cms.drafts
name: drafts
category: computing-software
field: web-development
product: payload-cms
tags: [drafts, draft-status, schedulepublish, draft-api]
level: practitioner
status: docs-checked
description: "Enable drafts with versions.drafts to get an injected _status field, draft and publish actions, and draft-aware Local API, REST and GraphQL calls."
sources:
  - https://payloadcms.com/docs/versions/drafts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drafts

Goal: save work-in-progress without publishing.

Drafts build on versions. Enable with `versions.drafts: true` or an object:

```ts
versions: {
  drafts: {
    autosave: true,
    schedulePublish: true,
    validate: false,   // default; true validates drafts on save
  },
}
```

Enabling drafts injects a `_status` field. In the Admin Panel a document shows as Draft (never published), Published, or Changed (published but newer drafts exist). The Save button is replaced by save draft and publish actions.

Restrict public reads to published documents:

```ts
access: {
  read: ({ req }) => (req.user ? true : { _status: { equals: 'published' } }),
}
```

The APIs gain draft handling: Local API operations accept `draft: true` (for example `payload.findByID({ collection: 'pages', id, draft: true })` returns the latest draft), and draft saves are not validated by default; set `drafts.validate: true` to validate them.

`_status` defaults to `draft`. With `draft: true` on an update, only the versions table is written and the main document is unchanged unless the data sets `_status: 'published'`. Setting `_status: 'draft'` does not bypass required-field validation; `draft: true` does. The `draft` argument alone does not hide drafts from API reads, so access control must do it.

Scheduled publish creates a background job, so the Jobs queue must be running. Documents that existed before drafts were enabled have no `_status` until re-saved, so also allow `_status: { exists: false }` in public read access. To restrict who can publish, return a Where constraint on `_status` from `update` access; the Admin then hides Publish and Unpublish.

## Checked

2026-11-04. Read versions/drafts in the payloadcms/payload docs. Confirmed: options, injected _status, Admin states, draft argument on create/update/find/findByID, validate default false, read access example. Added: write-location rules, scheduled publish requirement, pre-existing documents caveat, publish control. Removed: the verify step.
Method: documentation only; no commands were run.
