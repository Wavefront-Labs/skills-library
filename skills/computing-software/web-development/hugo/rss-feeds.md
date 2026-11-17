---
id: computing-software.web-development.hugo.rss-feeds
name: rss-feeds
category: computing-software
field: web-development
product: hugo
tags: [rss, feeds, services-rss, disablekinds, rss-template]
level: practitioner
status: docs-checked
description: "Control Hugo RSS feeds: which page kinds get them, disabling feeds, the item limit, copyright and author, linking the feed in head, and custom RSS templates."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/rss.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Hugo generates RSS feeds for home, section, taxonomy and term pages. Control them in project configuration.

Choose page kinds:

```toml
[outputs]
home = ['html', 'rss']
section = ['html', 'rss']
taxonomy = ['html']
term = ['html']
```

Disable all feeds by adding `rss` to `disableKinds`:

```toml
disableKinds = ['rss']
```

Feeds have no item limit by default. Set one (`-1` also means unlimited):

```toml
[services.rss]
limit = 42
```

The built-in template renders `copyright` and `params.author` name and email when present:

```toml
copyright = '© 2023 ABC Widgets, Inc.'
[params.author]
name = 'John Doe'
email = 'jdoe@example.org'
```

Reference the feed in `head`:

```go-html-template
{{ with .OutputFormats.Get "rss" }}
  {{ printf `<link rel=%q type=%q href=%q title=%q>` .Rel .MediaType.Type .Permalink site.Title | safeHTML }}
{{ end }}
```

Custom templates override the embedded one, one per page kind: `layouts/home.rss.xml`, `section.rss.xml`, `taxonomy.rss.xml`, `term.rss.xml`. They receive a `Page` as context.

## Checked

2026-11-04. Confirmed against the Hugo docs page RSS templates: default feeds for home, section, taxonomy and term pages, the `outputs` and `disableKinds` examples, the unlimited default and `services.rss` limit with -1, the rendered `copyright` and `params.author` values, the head link snippet and the four custom template names. Nothing removed.

Method: documentation only; no commands were run.
