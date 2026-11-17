---
id: computing-software.web-development.vitepress.dynamic-async-config
name: dynamic-async-config
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, dynamic-config, async-config, top-level-await, config-function, defineconfig, remote-data]
level: advanced
status: docs-checked
description: "Generate the VitePress config from remote or computed data by default-exporting an async function or using top-level await."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The config file may default-export a **function** (the docs show an async one) returning the config, for building sidebars or other settings from data that is only known at build time.

```ts
import { defineConfig } from 'vitepress'

export default async () => {
  const posts = await (await fetch('https://my-cms.com/blog-posts')).json()
  return defineConfig({
    lang: 'en-US',
    title: 'VitePress',
    themeConfig: {
      sidebar: [
        ...posts.map((post) => ({
          text: post.name,
          link: `/posts/${post.name}`
        }))
      ]
    }
  })
}
```

Top-level `await` is equally supported:

```ts
const posts = await (await fetch('https://my-cms.com/blog-posts')).json()
export default defineConfig({ /* use posts */ })
```

## Checked

2026-11-04. Confirmed against the VitePress site-config page (Dynamic (Async) Config: default-exported async function, defineConfig, top-level await). Removed: the whole Guidance list (Node-only execution, serialization of themeConfig, error handling, filesystem sidebars, dev reload), none of which that page states, and the Verify step. Thin skill: about 110 words survive; the id is kept.

Method: documentation only; no commands were run.
