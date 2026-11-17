---
id: computing-software.web-development.directus.extension-bundles
name: extension-bundles
category: computing-software
field: web-development
product: directus
tags: [extension-bundles, bundle-entries, bundle-partial, npm-run-add]
level: advanced
status: docs-checked
description: "Group several Directus extensions into one bundle, describe them as entries in package.json, set partial, and add or remove members."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/09.extensions/4.bundles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bundles group extensions as one distributable package, for installing together or sharing dependencies. Create one by choosing the `bundle` type when scaffolding.

In the bundle's `package.json`, the `directus:extension` object has an `entries` array; each entry's source sits under `src`:

```json
{ "type": "interface", "name": "my-interface", "source": "src/my-interface/index.ts" }
```

`partial` (optional boolean, enabled by default) controls whether entries can be individually disabled.

Add a new member: in the bundle directory run `npm run add` and pick a type; it creates a boilerplate extension.

Add an existing one: move its directory into the bundle's `src` and add an entry to `package.json`.

Remove: delete its directory from `src` and remove its entry.

## Checked

2026-11-04: bundle purpose, entries array and src location, the example entry, partial property, npm run add, and the add existing and remove steps confirmed against the Directus Bundling Extensions page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
