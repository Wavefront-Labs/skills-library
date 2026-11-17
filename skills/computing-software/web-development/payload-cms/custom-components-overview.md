---
id: computing-software.web-development.payload-cms.custom-components-overview
name: custom-components-overview
category: computing-software
field: web-development
product: payload-cms
tags: [custom-components, component-paths, importmap, server-components]
level: advanced
status: docs-checked
description: "Replace or extend Admin Panel UI with Custom Components referenced by path, and regenerate the import map."
sources:
  - https://payloadcms.com/docs/custom-components/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom Components overview

Goal: swap or add Admin Panel UI.

Custom Components are referenced by path (a string pointing to a file and export), not imported directly, so the Admin can load them. Four places: root components, collection components, global components and field components.

```ts
export default buildConfig({
  admin: {
    components: {
      logout: { Button: '/components/Logout#MyLogoutButton' },
    },
  },
})
```

Component paths resolve relative to the project base directory, or to `admin.importMap.baseDir` when set. A path without `#` uses the default export.

The import map is regenerated at startup, on hot reload in development, or on demand. It is not regenerated at runtime or after a production build, so regenerate it before building:

```bash
pnpm payload generate:importmap
```

Components are Server Components by default; add `'use client'` for interactivity. Env variables needed client-side must use the `NEXT_PUBLIC_` (or `VITE_`) prefix.

## Checked

2026-11-04. Read custom-components/overview and configuration/environment-vars in the payloadcms/payload docs. Confirmed: path references, default export, import map generation command, Server Components by default, NEXT_PUBLIC_ and VITE_ prefixes. Changed: path resolution wording and import map regeneration timing to match the page; removed the unconfirmed restart verify step and the baseDir code hint.
Method: documentation only; no commands were run.
