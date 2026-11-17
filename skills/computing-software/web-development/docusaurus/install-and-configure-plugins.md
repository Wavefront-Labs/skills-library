---
id: computing-software.web-development.docusaurus.install-and-configure-plugins
name: install-and-configure-plugins
category: computing-software
field: web-development
product: docusaurus
tags: [plugins, plugin-options, babel-style-config, local-plugin, multi-instance]
level: practitioner
status: docs-checked
description: "Install Docusaurus plugins from npm or local paths, pass options with the name-plus-object tuple, and run several instances of a content plugin with unique IDs."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/using-plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Docusaurus core provides no features itself; docs, blog and pages are all plugins. With no plugins the site has no routes.

Install from npm, then list in `plugins`:

```js title="docusaurus.config.js"
export default {
  plugins: ['@docusaurus/plugin-content-pages'],
};
```

Local plugins: `plugins: ['./src/plugins/docusaurus-local-plugin']` (paths absolute or relative to the config file).

Options use a two-member tuple ("Babel style"):

```js
plugins: [
  '@docusaurus/plugin-debug',
  ['@docusaurus/plugin-sitemap', {ignorePatterns: ['/tags/**']}],
],
```

Content plugins support multiple instances (multiple docs, multiple blogs). Each instance needs a unique `id`; the default ID is `default`. At most one instance may be the default one, by omitting `id` or using `id: 'default'`.

```js
plugins: [
  ['@docusaurus/plugin-content-docs', {id: 'docs-1'}],
  ['@docusaurus/plugin-content-docs', {id: 'docs-2'}],
],
```

## Checked

2026-11-04: read the Docusaurus Using Plugins page in full. Confirmed that core has no features of its own, npm and local plugins, the tuple option style, and the multi-instance id rules. Nothing removed.

Method: documentation only; no commands were run.
