---
id: computing-software.web-development.vitepress.relocatable-builds-relative-base
name: relocatable-builds-relative-base
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, relocatable-build, relative-base, base-dot-slash, file-protocol, ipfs, offline-docs]
level: sme
status: docs-checked
description: "Use base './' to produce a build that works from any sub path, IPFS gateways, archives, and file:// without rebuilding."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/deploy.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When the final URL is not known at build time (an IPFS gateway at `https://gateway/ipfs/<cid>/...`, the Wayback Machine, a shared folder, docs bundled inside an app), set:

```ts
export default { base: './' }
```

Every page then references assets and other pages relative to its own location, and the client runtime recovers the real mount point on load. One build works from any sub path, even several at once, with routing, search and prefetching functional. Opening the generated HTML straight from the file system (`file://`) gives a styled, navigable static site; browsers block JS modules over `file://`, so there is no hydration and interactive features such as search stay inactive while pre-rendered content and links work.

Caveats to remember:
- Keep `cleanUrls` off (default); portable output needs `.html` links because there is no server to rewrite pretty URLs.
- `404.html` is generated for root depth; hosts that serve it as a fallback for deep URLs render it unstyled.
- `head` entries are verbatim, so avoid root-absolute paths like `/favicon.ico` there; use absolute URLs or `transformHead`.
- Raw HTML `<a>` tags keep their `href` as written; use Markdown link syntax for site-absolute links (embedded `<img>` sources go through the asset pipeline and are handled).
- Links produced by `createContentLoader` content stay site-absolute (resolve only at a root mount).
- Serve canonical URLs: the root as `/dir/` not `/dir`, with no added trailing slashes on pages.
- The dev server always serves at `/`; relative behaviour applies to production builds only.

Verify: copy `dist` into two different sub folders on a static server and click through both.

## Checked

2026-11-08. Read the VitePress docs source pages deploy (relocatable builds section) and site-config (base). Confirmed the base ./ behaviour, the file:// limits, and each caveat in the list (cleanUrls, 404.html, head entries, raw anchors, createContentLoader links, canonical URLs, dev server at /). No claims removed.

Method: docs-only read of cited pages, 2026-11-08
