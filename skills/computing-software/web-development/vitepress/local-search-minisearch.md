---
id: computing-software.web-development.vitepress.local-search-minisearch
name: local-search-minisearch
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, search, local-search, minisearch, search-provider-local, fuzzy-search, search-i18n, search-false]
level: practitioner
status: docs-checked
description: "Enable built-in local full-text search with provider 'local', tune MiniSearch, translate UI, and exclude pages."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-search.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable with:

```ts
export default defineConfig({
  themeConfig: { search: { provider: 'local' } }
})
```

It uses an in-browser fuzzy full-text index built with MiniSearch. Community alternatives named in the docs: pagefind, typesense and Cloudflare AI Search plugins.

**Translations** go under `options.locales.<code>.translations`: `button` (`buttonText`, `buttonAriaLabel`) and `modal` (`displayDetails`, `resetButtonTitle`, `backButtonTitle`, `noResultsText`, and a nested `footer` with `selectText`, `navigateText`, `closeText` and matching `...AriaLabel` keys). Use `root` as the code to translate the default locale.

**MiniSearch options**

```ts
options: {
  miniSearch: {
    options: { /* extractField, tokenize, processTerm */ },
    searchOptions: { /* default: { fuzzy: 0.2, prefix: true, boost: { title: 4, text: 2, titles: 1 } } */ }
  }
}
```

By default Chinese or Japanese character runs are segmented with `Intl.Segmenter` (browsers lacking it fall back to the plain split); setting `options.tokenize` replaces this. Document IDs in `searchOptions.filter` and `boostDocument` are site-relative like `/guide/page.html#section`, excluding `base`.

**Excluding pages:** frontmatter `search: false`. Or a custom `_render(src, env, md)` that returns `''` for chosen paths; it runs in Node and is stripped from client data:

```ts
async _render(src, env, md) {
  const html = await md.renderAsync(src, env)
  if (env.frontmatter?.search === false) return ''
  if (env.relativePath.startsWith('some/path')) return ''
  return html
}
```

A custom `_render` must handle `search: false` itself, and check optional `env` properties only after `renderAsync`. The same hook can prepend content (for example the frontmatter title as a heading) before indexing.

Verify: the search box finds a term from a page and not from an excluded page.

## Checked

2026-11-08. Read the VitePress docs source page default-theme-search (local search sections). Confirmed provider local, the MiniSearch default searchOptions, Intl.Segmenter tokenizing, document ID format, search: false, the custom _render hook and its warning, and the community plugin names. Rewrote the translations line to match the key layout in the page.

Method: docs-only read of cited pages, 2026-11-08
