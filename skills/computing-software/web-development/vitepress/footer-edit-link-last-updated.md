---
id: computing-software.web-development.vitepress.footer-edit-link-last-updated
name: footer-edit-link-last-updated
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, footer, editlink, edit-this-page, lastupdated, git-timestamp, shallow-clone, fetch-depth]
level: practitioner
status: docs-checked
description: "Add footer text, an edit-on-GitHub link with :path or a function, and git-based last-updated times that survive shallow CI clones."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-footer.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-edit-link.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-last-updated.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Footer.** `themeConfig.footer` takes `message` and `copyright` (inline HTML allowed, rendered inside a `<p>`; use the `layout-bottom` slot for blocks). It is **not shown when the sidebar is visible**. Disable per page with `footer: false`.

**Edit link.**

```js
themeConfig: {
  editLink: {
    pattern: 'https://github.com/vuejs/vitepress/edit/main/docs/:path',
    text: 'Edit this page on GitHub'
  }
}
```

`pattern` can be a function of `PageData` (it is serialized and run in the browser, so it must be pure):

```js
pattern: ({ filePath }) => filePath.startsWith('packages/')
  ? `https://github.com/acme/monorepo/edit/main/${filePath}`
  : `https://github.com/acme/monorepo/edit/main/docs/${filePath}`
```

Disable per page with `editLink: false`.

**Last updated.** Set site-level `lastUpdated: true`. VitePress runs `git log -1 --pretty="%ai"` per file, so the Markdown must be committed. Customize with `themeConfig.lastUpdated = { text: 'Updated at', formatOptions: { dateStyle: 'full', timeStyle: 'medium' } }` (default `{ dateStyle: 'short', timeStyle: 'short' }`). Per page: `lastUpdated: false`, or a date value to show that instead.

**CI trap.** If every page shows the same date it is a shallow clone. In GitHub Actions use `actions/checkout` with `fetch-depth: 0`; elsewhere prepend `git fetch --unshallow &&` to the build command. Sitemap `<lastmod>` tags depend on the `lastUpdated` option.

## Checked

2026-11-04. Confirmed against the VitePress default-theme Footer, Edit Link and Last Updated pages, the default-theme-config page (lastUpdated text and formatOptions defaults), the Frontmatter Config page (lastUpdated boolean or Date) and the sitemap-generation guide (lastmod needs lastUpdated). Removed: the claim that the shallow-clone trap applies to sitemap lastmod beyond the lastUpdated dependency, and the Verify step.

Method: documentation only; no commands were run.
