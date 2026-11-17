---
id: computing-software.web-development.hugo.url-slug-and-aliases
name: url-slug-and-aliases
category: computing-software
field: web-development
product: hugo
tags: [urls, slug, url-front-matter, aliases, redirects]
level: practitioner
status: docs-checked
description: "Control Hugo page URLs with slug and url front matter, leading slashes in multilingual sites, canonifyURLs and relativeURLs, and redirect old paths with aliases."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/urls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a page's URL matches its path in `content`.

- `slug` overrides the last path segment (not for the home page). Since 0.167.0, a `slug` on a section, taxonomy or term page applies to pages beneath it too.
- `url` overrides the entire path, is not sanitized, and wins if both are set. A `url` on a section does not affect pages beneath it. A colon is escaped with backslashes and fails on Windows.

```toml
title = 'My First Post'
slug = 'my-first-post'
```

A matching permalink pattern takes precedence over a slug inherited from an ancestor. A `url` ending in a file extension (`articles/my-first-article.html`) produces that exact URL; without one you get a trailing-slash URL. `url` also accepts permalink tokens, typically in `cascade` (for example `url = '/:sections[last]/:slug'`).

Leading slash: monolingual sites treat `about` and `/about` alike. Multilingual: `/about` is relative to `baseURL`, `about` to `baseURL` plus the language prefix (for example `https://example.org/de/about/`).

Post-processing options (mutually exclusive): `canonifyURLs = true` (legacy, likely to be removed) prepends `baseURL`; `relativeURLs = true` suits serverless sites browsed via the file system.

**Aliases** redirect old paths:

```toml
aliases = ['/old-url', 'old-name', '../old/path']
```

`/old-url` is site-relative; `old-name` is page-relative. Aliases are generated only for output formats where both `isHTML` and `permalinkable` are `true`.

By default Hugo writes an HTML file with a meta refresh at each alias. Override it with `layouts/alias.html` (context: `Permalink`, `Page`). For server-side redirects, use the `Aliases` method to generate a `_redirects` or `.htaccess` file, and set `disableAliases` to `true` to skip the HTML files (the `Aliases` method stays available). Client-side redirects create a directory plus `index.html` at each alias location, for example `public/posts/old-path/index.html`.

## Checked
Confirmed 2026-11-08 against the Hugo URL management page (read in full): slug, url, leading slashes, post-processing and aliases all match. Added permalink precedence, file extensions in `url`, tokens, and the alias output location. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
