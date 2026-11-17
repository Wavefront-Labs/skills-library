---
id: computing-software.web-development.vite.preview-options
name: preview-options
category: computing-software
field: web-development
product: vite
tags: [preview-options, preview-port, preview-proxy, preview-inherits-server]
level: practitioner
status: docs-checked
description: "preview.* options (host, allowedHosts, port 4173, strictPort, https, open, proxy, cors, headers) and which default to the matching server option."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/preview-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Preview options apply only to `vite preview`. Most default to the same-named `server.*` option:

- `preview.host`, `preview.allowedHosts`, `preview.strictPort`, `preview.https`, `preview.open`, `preview.proxy` (uses `http-proxy-3`; `^` keys are RegExp; `configure` gives the instance) and `preview.cors` all inherit from `server`.
- `preview.port`: default `4173`; if taken, the next port is tried.
- `preview.headers` (`OutgoingHttpHeaders`): response headers, no inherited default.

```js
export default defineConfig({
  server: { port: 3030 },
  preview: { port: 8080 },
})
```

`server.port` does not set the preview port: the example gives each its own value.

## Checked

2026-11-04. Confirmed against the Vite preview options page (docs/config/preview-options.md): each option's server.* default, preview.port 4173, http-proxy-3, headers. Nothing removed.

Method: documentation only; no commands were run.
