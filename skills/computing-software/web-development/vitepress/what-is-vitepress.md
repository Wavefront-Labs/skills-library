---
id: computing-software.web-development.vitepress.what-is-vitepress
name: what-is-vitepress
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, static-site-generator, ssg, vite, vue, docs-site, spa-hydration]
level: intro
status: docs-checked
description: "Explain what VitePress is, its use cases, SPA-after-first-load model, and how it relates to VuePress, to decide if it fits a project."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/what-is-vitepress.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VitePress is a static site generator (SSG) that takes Markdown, applies a theme, and emits static HTML that any static host can serve. It is built on Vite and Vue 3.

**Use cases.** (1) Documentation: the default theme is designed for technical docs (the Vue, Vite, Rollup, Pinia, Vitest and many other docs sites use it). (2) Blogs, portfolios and marketing sites: write a fully custom theme with the normal Vite + Vue developer experience, use data loaders and dynamic routes to build pages from local or remote data, provided the data can be determined at build time.

**Developer experience.** Vite-powered instant server start with edits reflected in under 100 ms without a page reload; built-in Markdown extensions (frontmatter, tables, syntax highlighting, advanced code-block features); every Markdown file is also a Vue single-file component, so Vue templating and components work inside content.

**Performance model.** First visit serves pre-rendered static HTML (good SEO and load speed), then a JS bundle hydrates the page into a SPA, so later navigations fetch only the incoming page and VitePress prefetches chunks for links in the viewport. The Vue compiler separates static from dynamic parts, so static Markdown is dropped from the JS payload and skipped during hydration; you pay only for dynamic parts.

**VuePress.** VitePress is the spiritual successor of VuePress 1 (Vue 2 plus webpack). VuePress 1 is deprecated; VuePress 2 is community-maintained. Migrating a default-theme VuePress 1 site is relatively straightforward (see the migration skill).

**Choose it when** you want Markdown-first content with Vue-based customization, and the data can be determined at build time (the docs' own condition for what it can build).

Verify: you can describe in one sentence why a page loads as plain HTML first and becomes a SPA afterwards.

## Checked

2026-11-08. Read the VitePress docs source page guide/what-is-vitepress. Confirmed use cases and named sites, the under-100 ms edit claim, Markdown and Vue-enhanced features, the hydration and prefetch model, and the VuePress history. Replaced Shiki highlighting with syntax highlighting (the page does not name Shiki) and replaced the per-request rendering claim with the page's build-time-data condition.

Method: docs-only read of cited pages, 2026-11-08
