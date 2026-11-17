---
id: computing-software.web-development.eleventy.permalinks
name: permalinks
category: computing-software
field: web-development
product: eleventy
tags: [permalink, output-path, url-structure, permalink-false, index-html]
level: intro
status: docs-checked
description: "Know where Eleventy writes each input file by default, remap output with the permalink key, skip writing with permalink false and avoid collisions."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/permalinks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default output (output dir `_site`):

| Input | Writes to | URL |
| --- | --- | --- |
| `index.njk` | `_site/index.html` | `/` |
| `template.njk` | `_site/template/index.html` | `/template/` |
| `subdir/template.liquid` | `_site/subdir/template/index.html` | `/subdir/template/` |
| `subdir/template/template.liquid` or `.../index.liquid` | `_site/subdir/template/index.html` | `/subdir/template/` |

Eleventy writes `index.html` files so URLs need no extension (Cool URIs don't change).

Remap with `permalink` in front matter or anywhere in the data cascade. Missing subdirectories are created. A directory permalink gets `index.html` added:

```yaml
permalink: this-is-a-new-path/subdirectory/testing/
```

Output files can have any extension, e.g. `permalink: index.json`.

`permalink: false` skips writing the file but still renders it for collections, with `url` and `outputPath` set to `false`.

If two inputs write to the same location, Eleventy throws an error.

`permalinkBypassOutputDir: true` (0.1.4+) writes outside the output directory, e.g. `permalink: _includes/index.html` to generate a child template for reuse.

## Checked

2026-11-08. Confirmed against the Eleventy docs Permalinks page (markdown source): the default output table, Cool URIs rationale, directory permalinks gaining index.html, any output extension, permalink false semantics, collision error, and permalinkBypassOutputDir with its version note. Nothing removed.

Method: documentation only; no commands were run.
