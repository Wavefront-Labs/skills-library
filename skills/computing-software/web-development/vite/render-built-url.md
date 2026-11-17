---
id: computing-software.web-development.vite.render-built-url
name: render-built-url
category: computing-software
field: web-development
product: vite
tags: [render-built-url, advanced-base-options, cdn-assets, runtime-url]
level: advanced
status: docs-checked
description: "Use experimental.renderBuiltUrl to serve entry HTML, hashed assets and public files from different paths or a CDN, with runtime and relative return forms."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Experimental. A single static `base` is not enough when generated HTML, hashed assets and copied public files deploy to different paths (for example for different cache strategies). Use `experimental.renderBuiltUrl`:

```ts
experimental: {
  renderBuiltUrl(filename, { hostType }) {
    if (hostType === 'js') {
      return { runtime: `window.__toCdnUrl(${JSON.stringify(filename)})` }
    } else {
      return { relative: true }
    }
  },
},
```

The second argument carries `hostId`, `hostType` and `type`; `type === 'public'` identifies public files, so each group can be handled independently:

```ts
if (type === 'public') return 'https://www.domain.com/' + filename
```

Rules:
- `filename` is a decoded URL; a returned URL string must be decoded too and Vite encodes it when rendering.
- With an object holding `runtime`, the code is rendered as-is, so handle any needed encoding yourself.

## Checked

2026-11-07. Re-read the Building for Production guide (docs/guide/build.md) in full, focusing on Advanced Base Options. Confirmed the experimental status, the three deploy groups, the renderBuiltUrl(filename, { hostType }) example with runtime and relative returns, the hostId/hostType/type context, the type === 'public' branch, and the decoded filename and runtime-rendered-as-is encoding notes. Nothing removed.

Method: documentation only; no commands were run.
