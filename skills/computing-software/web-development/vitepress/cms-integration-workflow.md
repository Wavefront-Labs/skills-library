---
id: computing-software.web-development.vitepress.cms-integration-workflow
name: cms-integration-workflow
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, cms, headless-cms, loadenv, dynamic-routes, env-file, api-token, content-marker]
level: advanced
status: docs-checked
description: "Connect a headless CMS: load tokens with loadEnv, fetch entries in a paths loader, and render title, params and content in the template."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/cms.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Connecting a CMS is mostly the dynamic-routes mechanism, with three steps.

1. **Secrets.** If the CMS needs auth, keep tokens in a `.env` file and load them inside the paths loader with `loadEnv` from `vitepress`:

```js
// posts/[id].paths.js
import { loadEnv } from 'vitepress'
const env = loadEnv('', process.cwd())
```

2. **Fetch and shape paths.** Map every CMS entry to a params object plus raw content:

```js
export default {
  async paths() {
    const data = await (await fetch('https://my-cms-api', {
      headers: { /* token if necessary */ }
    })).json()
    return data.map(entry => ({
      params: { id: entry.id, /* title, authors, date etc. */ },
      content: entry.content
    }))
  }
}
```

3. **Render in `posts/[id].md`.**

```md
# {{ $params.title }}

- by {{ $params.author }} on {{ $params.date }}

<!-- @content -->
```

Notes: the docs only offer this generic workflow, since each CMS differs (use the CMS's client library if it has one). Anything in params goes to the browser, so keep API tokens in the loader only. The paths loader runs at build time, so content changes need a new build to appear. Large bodies should travel as `content`, not params, because params are serialized into the client JavaScript payload.

## Checked

2026-11-04. Confirmed against the VitePress CMS guide (General Workflow: loadEnv, paths loader, content, $params, <!-- @content -->) and the routing guide (Dynamic Routes: paths loader runs at build time, params are serialized into the client payload, rendering raw content with the content property). Removed: the webhook-to-CI advice and the Verify step.

Method: documentation only; no commands were run.
