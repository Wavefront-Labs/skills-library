---
id: computing-software.web-development.payload-cms.plugins-overview
name: plugins-overview
category: computing-software
field: web-development
product: payload-cms
tags: [plugins, official-plugins, plugin-api, buildconfig-plugins]
level: intro
status: docs-checked
description: "Add official plugins through the plugins array and understand that a plugin is a function taking and returning a config."
sources:
  - https://payloadcms.com/docs/plugins/overview
  - https://payloadcms.com/docs/upload/storage-adapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Plugins overview

Goal: extend Payload with plugins.

```ts
export default buildConfig({
  plugins: [
    // add plugins here
  ],
})
```

A plugin takes the existing config and returns a modified config with new fields, hooks, collections, admin views or endpoints. Writing one is plain JavaScript:

```ts
export const myPlugin = (opts) => (incomingConfig) => ({
  ...incomingConfig,
  collections: [...(incomingConfig.collections ?? []), myCollection],
})
```

Official plugins covered in these docs: Form Builder, MCP, SEO, Redirects, Nested Docs, Search, Multi-Tenant, Import/Export, Stripe, Sentry (and an e-commerce plugin). Storage adapters are registered under the top-level `storage` key, not `plugins`.

Example use cases: sync data to a CRM, password-protect documents, add reporting views, encrypt collections, add endpoints or GraphQL.

Verify: the plugin's collection or fields appear after restart.

## Checked

2026-11-04. Read plugins/overview and upload/storage-adapters. Confirmed: the plugins array in buildConfig, that a plugin takes the incoming config and returns a modified config, the official plugin list (Form Builder, MCP, Multi-Tenant, Nested Docs, Redirects, Search, Sentry, SEO, Stripe, Import/Export, Ecommerce), the example use cases, and that storage adapters are registered under the top-level storage key (from the storage adapters page).
Method: documentation only; no commands were run.
