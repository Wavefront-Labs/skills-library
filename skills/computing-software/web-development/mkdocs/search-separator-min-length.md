---
id: computing-software.web-development.mkdocs.search-separator-min-length
name: search-separator-min-length
category: computing-software
field: web-development
product: mkdocs
tags: [search-plugin, min-search-length, separator, lunr]
level: practitioner
status: docs-checked
description: "Tune the built-in MkDocs search plugin word splitting with separator and the minimum query length with min_search_length."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default `search` plugin uses lunr.js. Two options shape matching:

`separator`: regular expression for word separator characters when building the index. Default `'[\s\-]+'` (whitespace and hyphen). To also split on dots:

```yaml
plugins:
  - search:
      separator: '[\s\-\.]+'
```

`min_search_length`: integer minimum query length. Default 3, because shorter queries give poor results. Lower it for short terms like "MQ":

```yaml
plugins:
  - search:
      min_search_length: 2
```

Gotcha: because configuring `plugins` removes defaults, list `search` explicitly (as above) whenever you use other plugins.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (search plugin `separator`, `min_search_length`, plugins): lunr.js, defaults `[\s\-]+` and 3, both examples, and that setting `plugins` drops defaults. Removed: a rebuild claim and a generic verify line.

Method: documentation only; no commands were run.
