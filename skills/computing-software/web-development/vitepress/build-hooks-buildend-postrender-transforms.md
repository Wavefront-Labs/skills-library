---
id: computing-software.web-development.vitepress.build-hooks-buildend-postrender-transforms
name: build-hooks-buildend-postrender-transforms
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, build-hooks, buildend, postrender, transformhead, transformhtml, transformpagedata, og-image, ssgcontext]
level: sme
status: docs-checked
description: "Use buildEnd, postRender, transformHead, transformHtml and transformPageData to extend builds, add head tags, and attach page data."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Build hooks are site-config functions used for sitemaps, search indexing, PWA and teleports.

- **`buildEnd(siteConfig)`**: runs after SSG finishes but before the CLI exits; good for generating files.
- **`postRender(context)`**: called when SSG rendering of a page is done; receives `SSGContext { content, teleports?, vpIcons, ... }` so you can handle Vue teleport content. May return a modified context. VitePress SSG supports teleports to `body` only; for other targets wrap the teleport in `<ClientOnly>` or inject the teleport markup into the right place in the final HTML from `postRender`.
- **`transformHead(context)`**: returns extra `HeadConfig[]` per page, merged with existing head. `TransformContext` has `page` (relative to srcDir, e.g. `index.md`), `assets`, `siteConfig`, `siteData`, `pageData`, `title`, `description`, `head`, `content`. Build only, not dev, and not updated on client-side navigation. Never mutate the context.
- **`transformHtml(code, id, context)`**: transform the final HTML before it is written. Changing HTML can cause hydration problems. The icon stylesheet link still contains the `vp-icons.__VP_ICONS_HASH__.css` placeholder here; hooks that inline or fingerprint head assets should skip that tag.
- **`transformPageData(pageData, { siteConfig })`**: mutate `pageData` or return values to merge. It also runs in dev and on client navigation, so guard heavy work with `process.env.NODE_ENV === 'production'`.

```ts
export default {
  async transformHead(context) {
    if (context.page === '404.md') return
    const imageUrl = await generatePageImage(context)
    return [['meta', { name: 'og:image', content: imageUrl }]]
  },
  transformPageData(pageData) {
    const title = pageData.frontmatter.layout === 'home' ? 'VitePress' : `${pageData.title} | VitePress`
    pageData.frontmatter.head ??= []
    pageData.frontmatter.head.push(['meta', { name: 'og:title', content: title }])
  }
}
```

Choose transformPageData for cheap metadata (works everywhere), transformHead when generation is expensive (skips dev cost), and frontmatter `head` for static per-page tags.

## Checked

2026-11-04. Confirmed against the VitePress site-config page (Build Hooks: buildEnd, postRender and SSGContext, transformHead and TransformContext, transformHtml and the icon placeholder note, transformPageData and its examples) and the using-vue guide (teleports to body only in SSG). Removed: the Verify step.

Method: documentation only; no commands were run.
