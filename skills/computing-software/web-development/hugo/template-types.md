---
id: computing-software.web-development.hugo.template-types
name: template-types
category: computing-software
field: web-development
product: hugo
tags: [templates, baseof, partials, views, layouts-directory]
level: practitioner
status: docs-checked
description: "Hugo template types in the layouts directory: base, home, page, section, taxonomy, term, single, list, all, partial, view, render hook and shortcode templates."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/types.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Templates live in `layouts` at the project root.

```tree
layouts/
├── _markup/        <-- render hooks
├── _partials/
├── _shortcodes/
├── films/
│   ├── _views/
│   │   └── card.html
│   ├── page.html
│   └── section.html
├── baseof.html
├── home.html
├── page.html
├── section.html
├── taxonomy.html
└── term.html
```

- **Base** (`baseof.html`): shared HTML structure. Applies to home, page, section, taxonomy, term, single, list and all templates, but only if the template has at least one `define` and nothing else but whitespace and comments. It replaces `block` actions with matching `define` content.
- A base template can be varied by file name (`baseof.de.html`, `baseof.section.html`) or by subdirectory (`docs/baseof.html`). Hugo matches those identifiers against the template being rendered, not the page: `baseof.section.html` applies to `section.html`, not `list.html`.
- **Home, page, section, taxonomy, term:** one per kind. In taxonomy templates `Data` provides `Singular`, `Plural` and `Terms` (`Terms` returns a taxonomy object with `Alphabetical` and `ByCount`); in term templates `Data` provides `Singular`, `Plural` and `Term`.
- **Single:** fallback for page templates. **List:** fallback for home, section, taxonomy and term. **All:** fallback for home, page, section, taxonomy, term, single and list.
- **Partial:** returns a component or value via `partials.Include` or `partials.IncludeCached`. Lookup ignores page kind, content type, logical path, language and output format, but still tries the most specific name first: `footer.section.de.html` falls back to `footer.section.html`, `footer.de.html`, then `footer.html`. Inline partials are defined with `define "_partials/name.html"` and registered globally.
- **View:** like a partial, called with `Render` on `Page`.
- **Render hook** (`_markup/`) overrides Markdown-to-HTML conversion; **shortcode** (`_shortcodes/`) is called from content pages.

```go-html-template
{{ block "main" . }}
  fallback
{{ end }}
```

Pair it with `{{ define "main" }}...{{ end }}` in the child template.

```go-html-template
{{ .Render "_views/card" }}
```

## Checked
Confirmed 2026-11-08 against the Hugo template types page (read in full): structure, base template conditions, fallback chain, partial lookup, views, hooks and shortcodes. Added base-name variants, term Data methods and partial name fallback; corrected the All fallback list.
Method: docs-only read of cited pages, 2026-11-08
