---
id: computing-software.web-development.docusaurus.versioning-config-options
name: versioning-config-options
category: computing-software
field: web-development
product: docusaurus
tags: [lastversion, includecurrentversion, onlyincludeversions, version-banner, version-label]
level: advanced
status: docs-checked
description: "Tune docs versioning with lastVersion, includeCurrentVersion, onlyIncludeVersions, disableVersioning and per-version label, path, banner, badge and className."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/docs/versioning.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defaults suit "release v1, start v2 immediately": current (`./docs`, labelled Next) is at `/docs/next`, latest at `/docs`.

If you release v1 and will maintain it without a v2, avoid maintaining two folders by treating current as the cut version:

```js title="docusaurus.config.js"
docs: {
  lastVersion: 'current',
  versions: {
    current: {label: '1.0.0', path: '1.0.0'},
  },
},
```

`./docs` is then served at `/docs/1.0.0` and is the default in the navbar dropdown.

Plugin options:

- `disableVersioning`: include only the current version even if versions exist.
- `includeCurrentVersion`: turn off if the current version is a work in progress.
- `lastVersion`: which version the `/docs` route refers to.
- `onlyIncludeVersions`: subset of `versions.json` to deploy; limit to 2 or 3 in dev and deploy previews to speed startup and builds.
- `versions`: per-version metadata.
  - `label`: shown in dropdown and banner.
  - `path`: route base path (latest defaults to `/`, current to `/next`).
  - `banner`: `'none'`, `'unreleased'` or `'unmaintained'` (versions above latest are unreleased, below are unmaintained).
  - `badge`: show a version badge on each doc.
  - `className`: added to the `<html>` element for that version's pages.

## Checked

2026-11-04: read the Docusaurus Versioning page in full. Confirmed the two version patterns, the lastVersion current example, and every plugin option and per-version field (label, path, banner, badge, className) with the tips. Nothing removed.

Method: documentation only; no commands were run.
