---
id: computing-software.web-development.vite.ssr-plugin-cli
name: ssr-plugin-cli
category: computing-software
field: web-development
product: vite
tags: [ssr-plugin-option, configure-server-ssr, configure-preview-server, ssr-conditional-transform]
level: advanced
status: docs-checked
description: "SSR-specific plugin logic: the ssr flag in resolveId, load and transform options, and adding SSR middleware with configureServer and configurePreviewServer post hooks."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/ssr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Frameworks such as Vue or Svelte compile components differently for client and SSR. Vite passes an extra `ssr` property in the `options` object of `resolveId`, `load` and `transform`:

```js
export function mySSRPlugin() {
  return {
    name: 'my-ssr',
    transform(code, id, options) {
      if (options?.ssr) {
        // perform ssr-specific transform...
      }
    },
  }
}
```

The options object in `load` and `transform` is optional. Before Vite 2.7 this was a positional `ssr` parameter, so older posts may show the previous API.

CLI: `vite dev` and `vite preview` also work for SSR apps. Add SSR middleware to the dev server with `configureServer` and to the preview server with `configurePreviewServer`. Use a post hook so your middleware runs after Vite's own.

## Checked

2026-11-07. Re-read the Server-Side Rendering guide (docs/guide/ssr.md) in full. Confirmed the ssr property in the options of resolveId, load and transform, the optional options object, the Vite 2.7 positional-parameter note, and the Vite CLI section (vite dev, vite preview, configureServer, configurePreviewServer, post hook). Nothing removed.

Method: documentation only; no commands were run.
