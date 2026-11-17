---
id: computing-software.web-development.docusaurus.babel-config
name: babel-config
category: computing-software
field: web-development
product: docusaurus
tags: [babel, rspack, swc-loader, webpack-opt-in, babel-preset]
level: advanced
status: docs-checked
description: "When Babel applies in Docusaurus (only with the deprecated webpack option, since Rspack with SWC is the default) and how to extend the built-in Babel preset."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docusaurus uses Rspack by default and transpiles site source with the Rspack built-in SWC loader. Babel is only used if you opt into webpack through the deprecated `webpack` site config. In that case, customize Babel by creating `babel.config.js` in the project root.

To use the built-in preset as a base:

```sh
npm install --save @docusaurus/babel
```

```js title="babel.config.js"
export default {
  presets: ['@docusaurus/babel/preset'],
};
```

Most of the time the default preset works. To customize (for example to add Flow support), edit this file directly. Restart the dev server for changes to take effect.

## Checked

2026-11-04: read the Docusaurus configuration page, section Customizing Babel Configuration. Confirmed Rspack with SWC by default, Babel only with the deprecated webpack option, the @docusaurus/babel install, the preset line and restart. Nothing removed.

Method: documentation only; no commands were run.
