---
id: computing-software.web-development.docusaurus.presets-and-themes
name: presets-and-themes
category: computing-software
field: web-development
product: docusaurus
tags: [preset-classic, themes, presets, custom-preset, plugin-bundle]
level: practitioner
status: docs-checked
description: "Load themes, configure plugins through preset-classic option keys, disable bundled plugins with false, and write your own preset function."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/using-plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Themes load like plugins. The `themes` and `plugins` entries are interchangeable for consumers, except themes load after plugins and can override a plugin's default theme components.

`@docusaurus/preset-classic` bundles theme-classic, theme-search-algolia, and plugins content-docs, content-blog, content-pages, debug, google-gtag, google-tag-manager, sitemap, svgr and css-cascade-layers. It relays each option key to its plugin or theme:

```js
presets: [
  ['@docusaurus/preset-classic', {
    theme: {customCss: ['./src/css/custom.css']}, // theme-classic
    docs: {},     // content-docs, false to disable
    blog: {},     // content-blog, false to disable
    pages: {},    // false to disable
    sitemap: {},  // false to disable
    svgr: {},
    gtag: {},     // only enabled when explicitly specified
    googleTagManager: {},
  }],
],
```

`debug` defaults to true in dev and false in prod.

A custom preset is a function like a plugin constructor returning `{plugins, themes}`:

```js
export default function preset(context, opts = {}) {
  return {
    themes: [['docusaurus-theme-awesome', opts.theme]],
    plugins: [['@docusaurus/plugin-content-docs', {...opts.docs1, id: 'docs1'}]],
  };
}
```

Reference it by relative path in `presets`.

## Checked

2026-11-04. Read in full against the Docusaurus Using Plugins page (using-plugins.mdx): themes versus plugins loading order, the preset-classic bundle list, option keys relayed to each plugin, false to disable, gtag and googleTagManager only when specified, debug default, and the custom preset function shape all match. Nothing removed.

Method: documentation only; no commands were run.
