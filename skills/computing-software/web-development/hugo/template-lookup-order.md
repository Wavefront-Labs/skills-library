---
id: computing-software.web-development.hugo.template-lookup-order
name: template-lookup-order
category: computing-software
field: web-development
product: hugo
tags: [template-lookup, layout, type, page-kind, output-format]
level: practitioner
status: docs-checked
description: "How Hugo picks a template: identifiers in the file name and location in layouts, their ranking, and how to target a template with type and layout front matter."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/lookup-order.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo selects the most specific template from the identifiers in a template's file name and its location in `layouts`. Project and module (theme) `layouts` directories are all searched; if both supply the same file name, the project wins. Override a module template by using the same file name in the same directory of the project.

Identifiers in descending order of importance:

1. Custom layout: the `layout` front matter value.
2. Page kind: `home`, `page`, `section`, `taxonomy` or `term`.
3. Standard layout: `single` or `list`.
4. Output format name: `html`, `rss`, `json`.
5. Standard layout: `all`.
6. Language key: `en`, `de`.
7. Media type suffix: `html`, `xml`.
8. Page path: the template's location relative to the page's logical path.
9. Content type: the `type` front matter value.

Page path and content type come from the directory; the rest come from the file name. Each kind identifier applies only to its kind: `taxonomy.html` does not render term pages (use `term.html`, `list.html` or `all.html`). If no kind template exists, Hugo falls back to single or list, then all.

## File names

Separate identifiers with dots and end with the media type suffix.

- `layouts/section.html`: section pages, html format.
- `layouts/section.de.html`: same, in German.
- `layouts/section.rss.xml`: rss format.
- `layouts/section.json`: json format. When the format name equals the suffix it can be omitted, so `section.json` equals `section.json.json`; the template with fewer identifiers wins.
- If a media type has several suffixes, any may end the name; with a tie, the suffix listed first in the media type's `suffixes` wins.
- Use lowercase identifiers (`page.en-us.html`). Do not use a dot inside a custom layout or partial name; use a hyphen (`foo-bar.html`).
- Since 0.161.0, prefixed identifiers are available: `_kind_<kind>_`, `_layout_<layout>_`, `_outputformat_<format>_`, `_language_<key>_`, `_role_<name>_`, `_version_<name>_` (for example `page._layout_contact_.html`).

## Directory structure

Each subdirectory not starting with an underscore is the root of a logical path, and Hugo searches from the page's logical path up to the `layouts` root. Name the kind in the file, not the directory: `layouts/section.html`, whereas `layouts/section/` means `content/section`. A root-level page such as `content/about.md` uses `layouts/about/`.

```tree
layouts/
├── blog/
│   ├── sub/
│   │   └── section.html  <-- content/blog/sub/_index.md
│   ├── page.html         <-- content/blog/post-1.md and content/blog/sub/post-2.md
│   └── section.html      <-- content/blog/_index.md
├── home.html
├── page.html
└── section.html
```

A closer template does not always win: for a German page in `blog`, `layouts/page.de.html` beats `layouts/blog/page.html` because language outranks page path. The same rules apply to base templates, render hooks in `_markup` and shortcodes in `_shortcodes`, which may sit at any level; they also consider the content type. `_partials` must be at the `layouts` root and Hugo does not consider the current page when choosing a partial.

## Target a template

You cannot change the lookup order, but a page can set `layout`, `type` or both.

```toml
title = 'Contact'
layout = 'contact'
```

This renders with `layouts/contact.html`. To group templates, set `type = 'miscellaneous'` on the pages and use `layouts/miscellaneous/page.html` and `layouts/miscellaneous/contact.html`. Setting `type` replaces the top-level section in the logical path: `content/films/action/film-1.md` with `type = 'miscellaneous'` searches `layouts/miscellaneous/action`, not `layouts/films/action`.

Common placements: `layouts/all.html` (everything), `layouts/home.html`, `layouts/blog/page.html`, `layouts/blog/section.html`, `layouts/tags/term.html` (all tag terms), `layouts/tags/hugo/term.html` (one term), `layouts/page.featured.html` (pages with `layout = 'featured'`), `layouts/docs/baseof.html`, `layouts/docs/_markup/render-link.html`, `layouts/docs/_shortcodes/note.html`.

## Checked
Confirmed 2026-11-08 against the Hugo template lookup order page (read in full). The earlier draft described an older model (single.html, list.html and index.amp.html as kind, `layouts/page/single.html` for root pages, a six-item parameter list). Rewritten to the current identifier ranking, file name and directory rules, and the type and layout targeting examples.
Method: docs-only read of cited pages, 2026-11-08
