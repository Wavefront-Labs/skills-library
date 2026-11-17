---
id: computing-software.web-development.hugo.page-resources
name: page-resources
category: computing-software
field: web-development
product: hugo
tags: [page-resources, resources-get, resources-metadata, counter, shared-resources]
level: practitioner
status: docs-checked
description: "Access Hugo page resources from a bundle, set name, title and params metadata with the resources front matter array and :counter, and handle multilingual sharing."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/page-resources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Page resources are reachable only from page bundles, and only by the page they are bundled with. Capture them with `Resources.ByType`, `Resources.Get`, `Resources.GetMatch` or `Resources.Match`.

```go-html-template
{{ $path := "images/a.jpg" }}
{{ with .Resources.Get $path }}
  <img src="{{ .RelPermalink }}" width="{{ .Width }}" height="{{ .Height }}" alt="">
{{ else }}
  {{ errorf "Unable to get page resource %q" $path }}
{{ end }}
```

Set metadata with the `resources` front matter array. Keys: `src` (required, case-insensitive glob relative to the bundle), `name`, `title` (both support `:counter`) and `params`.

```yaml
resources:
  - src: images/sunset.jpg
    name: header
  - src: "**.pdf"
    name: pdf-file-:counter
    params:
      icon: pdf
```

- For `name` and `title` the first matching entry wins; for `params` all matches contribute and later entries win duplicates. Put specific patterns before broad wildcards.
- `:counter` starts at 1 per unique `src` pattern and counts separately for `name` and `title`.
- Look up by the `name` you set, not the file path.
- `page`-type resources take their metadata from their own front matter.

Multilingual single-host sites store shared Markdown-bundle resources once, in the default language's bundle. `markup.goldmark.duplicateResourceFiles = true` duplicates them, which the page calls inefficient.

## Checked

2026-11-04: bundle-only access, the four Resources methods, errorf example, resources front matter keys, case-insensitive src, first-match and params merge rules, :counter behaviour, page-type metadata and the multilingual sharing and duplicateResourceFiles notes confirmed against the Hugo docs Page resources page. Nothing removed.

Method: documentation only; no commands were run.
