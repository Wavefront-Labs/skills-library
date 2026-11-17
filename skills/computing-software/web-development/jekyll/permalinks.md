---
id: computing-software.web-development.jekyll.permalinks
name: permalinks
category: computing-software
field: web-development
product: jekyll
tags: [permalinks, permalink-placeholders, builtin-permalink-styles, pretty-urls, collection-permalinks]
level: practitioner
status: docs-checked
description: "Set Jekyll output URLs via front matter, global permalink config, built-in styles (date, pretty, ordinal, weekdate, none) and per-collection overrides."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/permalinks.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/permalinks.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Front matter: `permalink: /about/` sets one file's output path. Built-in style names such as `pretty` are not recognised in front matter.

Global, in `_config.yml`, using placeholders:

```yaml
permalink: /:categories/:year/:month/:day/:title:output_ext
```

Pages and collections other than `posts`/`drafts` have no time or categories, so those parts are ignored (`:title` acts as `:basename` for pages).

Built-in styles for posts:

- `date`: `/:categories/:year/:month/:day/:title:output_ext`
- `pretty`: `/:categories/:year/:month/:day/:title/`
- `ordinal`: `/:categories/:year/:y_day/:title:output_ext`
- `weekdate` (4.0): `/:categories/:year/W:week/:short_day/:title:output_ext`
- `none`: `/:categories/:title:output_ext`

So `permalink: pretty` replaces typing the full template.

Collections override the global style in their own config:

```yaml
collections:
  my_collection:
    output: true
    permalink: /:collection/:name
```

Collection placeholders: `:collection`, `:path`, `:name` (slugified base filename), `:title` (the `slug` front matter, else slugified filename, case preserved), `:output_ext`.

Pages: only front matter overrides the global style; a permalink from front matter defaults is ignored. Page placeholders: `:path`, `:basename`, `:output_ext`.

## Checked

2026-11-04. Confirmed against the Jekyll permalinks doc and its permalinks data file: front matter example, global placeholders, the five built-in formats and the 4.0 note on `weekdate`, collection override and collection/page placeholders, and the note that built-in styles are not recognised in front matter. Nothing removed.

Method: documentation only; no commands were run.
