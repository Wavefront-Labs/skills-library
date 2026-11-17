---
id: computing-software.web-development.strapi.plugins-config-file
name: plugins-config-file
category: computing-software
field: web-development
product: strapi
tags: [strapi, config-plugins, enabled, resolve, local-plugin, providers]
level: practitioner
status: docs-checked
description: "config/plugins: enable or disable plugins, override config, resolve local plugins, and which core features are configured there."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# config/plugins

Per plugin: `enabled` (boolean), optional `config` (override defaults from `strapi-server.js`), optional `resolve` (path, required only for local plugins).

```js
module.exports = ({ env }) => ({
  // enable a plugin that doesn't require any configuration
  i18n: true,
  // enable a custom plugin
  myplugin: {
    // my-plugin is going to be the internal name used for this plugin
    enabled: true,
    resolve: './src/plugins/my-local-plugin',
    config: {
      // user plugin config goes here
    },
  },
  // disable a plugin
  'my-other-plugin': {
    enabled: false, // plugin installed but disabled
  },
});
```

Shorthand: `'plugin-name': true`.

Some core features were historically plugins and are still configured here: Upload (Media Library) and Users & Permissions. Provider configuration for Media Library and Email also lives in this file. GraphQL config is documented on its plugin page.

## Checked

2026-11-04: checked against the Strapi docs page Plugins configuration (configurations/plugins). Confirmed: `enabled`, `config`, `resolve` parameters and their optional/required wording, example config, `'plugin-name': true` shorthand, Upload, Users & Permissions, GraphQL and provider configuration notes. Removed: nothing.

Method: documentation only; no commands were run.
