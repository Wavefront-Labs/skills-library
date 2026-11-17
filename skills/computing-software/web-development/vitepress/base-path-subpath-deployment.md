---
id: computing-software.web-development.vitepress.base-path-subpath-deployment
name: base-path-subpath-deployment
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, base, base-path, subpath, github-pages, gitlab-pages, deploy, withbase]
level: practitioner
status: docs-checked
description: "Set base for sub-path hosting like user.github.io/repo/, know how assets and links adapt, and use withBase for dynamic URLs."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/deploy.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/asset-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`base` is the URL path the site is deployed under. Default `/`. If the site will live at `https://foo.github.io/bar/`, set `base: '/bar/'`. It must start and end with a slash (the single exception is `'./'`, see the relocatable-builds skill). It can also be given per build: `vitepress build --base /bar/`.

```ts
export default { base: '/repo/' }
```

What `base` affects automatically:
- the base is prepended to every URL that starts with `/` in config options, so state it once;
- static asset references written in Markdown or theme templates, including those pointing at `public/`, are adjusted, so `![](/image-inside-public.png)` always works;
- Markdown links get the base prepended. To link to a page outside the base, use a relative path like `../../pure.html` or an HTML anchor with `target="_self"`.

What you must handle yourself: dynamically built paths, for example an `<img :src>` from a theme config value. Wrap them in `withBase` from `vitepress`:

```vue
<script setup>
import { withBase, useData } from 'vitepress'
const { theme } = useData()
</script>
<template><img :src="withBase(theme.logoPath)" /></template>
```

Platform hints: on GitHub or GitLab Pages at `user.github.io/repo/`, set `base` to `/repo/`. GitLab needs no `base` for a custom domain, user or group pages, or with the "Use unique domain" setting. Head entries are emitted verbatim, so the docs' favicon example says to write `/base/favicon.ico` there.

## Checked

2026-11-04. Confirmed against the VitePress site-config page (base), the deploy guide (Setting a Public Base Path, GitLab Pages, relocatable builds), the asset-handling guide (Base URL, withBase) and the routing guide (base prepended to Markdown links, ../../pure.html and target=_self). Removed: the unconfirmed claim that custom domains on GitHub Pages need no base, and the Verify step.

Method: documentation only; no commands were run.
