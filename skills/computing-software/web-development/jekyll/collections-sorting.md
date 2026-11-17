---
id: computing-software.web-development.jekyll.collections-sorting
name: collections-sorting
category: computing-software
field: web-development
product: jekyll
tags: [collection-sort-by, collection-order, document-ordering, tutorials-collection]
level: advanced
status: docs-checked
description: "Control document order in a Jekyll collection (4.0+): default date/path sorting, sort_by a front matter key, and a manual order list that takes precedence."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/collections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default: documents sort by `date` when both have it; if either lacks `date`, they sort by path. Custom sorting is set in the collection's metadata (4.0+).

`sort_by` names a front matter key; values sort in increasing order:

```yaml
collections:
  tutorials:
    sort_by: lesson
```

A document without the key goes right after the sorted ones; several such documents are sorted among themselves by date or path.

`order` lists filenames in the desired order:

```yaml
collections:
  tutorials:
    order:
      - hello-world.md
      - introduction.md
      - basic-concepts.md
      - advanced-concepts.md
```

Filenames not in the list go after the rearranged ones. Documents in subdirectories need the subpath in the entry, e.g. `concepts/basics.md`.

If both `sort_by` and `order` are defined, `order` takes precedence.

## Checked

2026-11-04. Confirmed against the Jekyll Collections page: default date/path sorting, sort_by, order and precedence (4.0). Nothing removed.

Method: documentation only; no commands were run.
