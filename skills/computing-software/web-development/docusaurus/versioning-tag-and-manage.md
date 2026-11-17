---
id: computing-software.web-development.docusaurus.versioning-tag-and-manage
name: versioning-tag-and-manage
category: computing-software
field: web-development
product: docusaurus
tags: [docs-version, versions-json, versioned-docs, versioned-sidebars, current-version]
level: practitioner
status: docs-checked
description: "Tag a new docs version with docs:version, understand versions.json and versioned folders, add docs to old versions, and delete a version."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/docs/versioning.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Versioning copies the current `docs` into a frozen set. Most sites do not need it: it increases build time and complexity, and suits high-traffic sites with rapid doc changes between versions.

```sh
npm run docusaurus docs:version 1.1.0
```

This copies `docs/` to `versioned_docs/version-1.1.0/`, saves the sidebar as `versioned_sidebars/version-1.1.0-sidebars.json` (if one exists) and appends the version to `versions.json` (newest to oldest).

Mapping:

| Path | Version | URL |
| --- | --- | --- |
| `versioned_docs/version-1.0.0/hello.md` | 1.0.0 | /docs/1.0.0/hello |
| `versioned_docs/version-1.1.0/hello.md` | 1.1.0 (latest) | /docs/hello |
| `docs/hello.md` | current | /docs/next/hello |

Terminology: current is the `./docs` folder (a file system location); latest is the version served by default in navbar items (navigation behaviour).

New docs go in the folder of the target version, plus an entry in that version's sidebar file. Versioned sidebar files are relative to that version's content root. Editing a file in `versioned_docs/version-2.6/` affects only 2.6.

Delete a version: remove it from `versions.json`, delete its `versioned_docs/version-X` directory and its `versioned_sidebars/version-X-sidebars.json`.

## Checked

2026-11-04: read the Docusaurus Versioning page in full. Confirmed when versioning is worthwhile, the docs:version command and what it creates, the path to URL table, current versus latest terminology, adding docs to a version, and the delete steps. Nothing removed.

Method: documentation only; no commands were run.
