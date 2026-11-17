---
id: computing-software.web-development.docusaurus.versioning-navbar-and-practices
name: versioning-navbar-and-practices
category: computing-software
field: web-development
product: docusaurus
tags: [docsversiondropdown, navbar-version, site-alias, versioned-assets, archive-versions]
level: advanced
status: docs-checked
description: "Version-aware navbar items and docsVersionDropdown options, plus recommended practices: when to cut versions, @site imports, file-path links and per-version assets."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/docs/versioning.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docs navbar items `doc`, `docSidebar`, `docsVersion` and `docsVersionDropdown` pick a version in order: active version (the one being browsed), preferred version (last viewed), then latest (`lastVersion`).

Show a subset in order, or relabel:

```js title="docusaurus.config.js"
{type: 'docsVersionDropdown', versions: ['current', '3.0', '2.0']},
{type: 'docsVersionDropdown', versions: {current: {label: 'Version 4.0'}, '3.0': {label: 'Version 3.0'}}},
```

Practices:

- Version only when needed; a patch release with no new features should not get its own docs version.
- Keep the number of versions below 10. Archive older versions as separate immutable deployments on a static host and link to them.
- Do not use relative imports inside docs, as nesting changes when a version is cut. Use the `@site` alias:

```diff
- import Foo from '../src/components/Foo';
+ import Foo from '@site/src/components/Foo';
```

- Link other docs by relative file path with the extension so links are rewritten to the matching version.
- Versioned assets: put them in the docs folder and use relative paths (`![alt](./myImage.png)`). Global assets go in `/static` and use absolute paths (`/myImage.png`).

## Checked

2026-11-04: read the Docusaurus Versioning page in full. Confirmed the navbar items, active/preferred/latest order, docsVersionDropdown versions forms, and the recommended practices (when to version, fewer than 10 versions, archives, @site imports, file path links, assets). Nothing removed.

Method: documentation only; no commands were run.
