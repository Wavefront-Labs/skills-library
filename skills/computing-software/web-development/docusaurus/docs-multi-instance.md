---
id: computing-software.web-development.docusaurus.docs-multi-instance
name: docs-multi-instance
category: computing-software
field: web-development
product: docusaurus
tags: [multi-instance, docs-plugin, docspluginid, versioned-paths, docs-version]
level: advanced
status: docs-checked
description: "Run two or more docs plugin instances on one Docusaurus site, with the preset instance as default, per-instance version folders, CLI commands and navbar items."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/docs/docs-multi-instance.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Multi-instance is only useful for versioned docs, per the page (for separate lifecycles, or mixing versioned and unversioned docs). For several sidebars alone, use one plugin. If each documentation set is very large, prefer separate sites.

`@docusaurus/preset-classic` already includes a docs instance. Configure it as default and add another with a unique `id`:

```js title="docusaurus.config.js"
presets: [['@docusaurus/preset-classic', {
  docs: {
    path: 'product',
    routeBasePath: 'product',
    sidebarPath: './sidebarsProduct.js',
  },
}]],
plugins: [['@docusaurus/plugin-content-docs', {
  id: 'community',
  path: 'community',
  routeBasePath: 'community',
  sidebarPath: './sidebarsCommunity.js',
}]],
```

Versioned storage: the default instance uses `website/versions.json`, `versioned_docs`, `versioned_sidebars`; others use `website/[pluginId]_versions.json`, `[pluginId]_versioned_docs`, `[pluginId]_versioned_sidebars`.

Tag versions per instance:

```sh
npm run docusaurus docs:version 1.0.0
npm run docusaurus docs:version:community 1.0.0
```

Docs navbar items take `docsPluginId`, for example `{type: 'docsVersionDropdown', docsPluginId: 'ios'}`.

## Checked

2026-11-04: read the Docusaurus Docs Multi-instance page in full. Confirmed the use cases, the preset plus second instance setup, versioned paths, the per-instance version command and docsPluginId. Corrected the opening claim from mainly useful to only useful for versioned docs, as the page says.

Method: documentation only; no commands were run.
