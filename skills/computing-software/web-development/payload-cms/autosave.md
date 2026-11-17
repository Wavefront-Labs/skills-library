---
id: computing-software.web-development.payload-cms.autosave
name: autosave
category: computing-software
field: web-development
product: payload-cms
tags: [autosave, autosave-interval, showsavedraftbutton, debounce]
level: practitioner
status: docs-checked
description: "Configure autosave on drafts-enabled collections with interval (default 800 ms) and showSaveDraftButton."
sources:
  - https://payloadcms.com/docs/versions/autosave
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Autosave

Goal: never lose edits.

Autosave requires versions and drafts. Enable with `true` or options:

```ts
versions: {
  drafts: {
    autosave: {
      interval: 1500,            // ms, debounced, default 800
      showSaveDraftButton: true, // default false
    },
  },
}
```

The Admin saves changes as drafts as you edit and shows when the document was last saved at the top right of the sidebar.

Pair it with read access that hides unpublished documents:

```ts
read: ({ req }) =>
  req.user ? true : { _status: { equals: 'published' } },
```

Local API: with autosave enabled, `update` operations accept an `autosave` argument. When `true`, Payload treats the incoming draft update as an autosave and keeps one autosave version, updating it on each autosave instead of cluttering `_versions` with a new entry every time.

Note: the page says autosaves are stored as a Draft version and also that only one autosave version is created and then updated. Expect a single autosave version to be updated rather than a new version per save.

## Checked

2026-11-04. Read versions/autosave in the payloadcms/payload docs. Confirmed: interval default 800 ms, showSaveDraftButton default false, the autosave argument. Fixed: the verify step claimed a new version each time. Flagged: the page is internally inconsistent about new Draft version versus one updated autosave version.
Method: documentation only; no commands were run.
