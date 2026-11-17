---
id: computing-software.web-development.eleventy.data-cascade
name: data-cascade
category: computing-software
field: web-development
product: eleventy
tags: [data-cascade, data-priority, deep-merge, override-prefix]
level: intro
status: docs-checked
description: "Understand Eleventy's data cascade: the priority order of data sources, how leaf templates win over layouts, and the override: prefix to skip merging."
sources:
  - https://www.11ty.dev/docs/data-cascade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Eleventy merges data from several sources before rendering. Priority, highest first:

1. Computed data
2. Front matter in the template
3. Template data files
4. Directory data files (and ascending parent directories)
5. Front matter in layouts
6. Configuration API global data
7. Global data files

When a template and its layout share a key, the leaf template wins. Objects and Arrays are deep merged:

```yaml
# my-template.md          # _includes/my-layout.njk
title: A Good Post        title: A Very Good Post
tags: [CSS, HTML]         author: Zach
layout: my-layout.njk     tags: [JavaScript]
```

Result: `title: "A Good Post"`, `author: "Zach"`, `tags: ["CSS", "HTML", "JavaScript"]`, `layout: "my-layout.njk"`.

Opt out of merging for one key with the `override:` prefix:

```md
---
# Instead of merging the array, this creates an empty set
override:tags: []
---
```

Here `posts/firstpost.md` no longer inherits the `posts` tag from `posts/posts.json`.

## Checked

2026-11-04. Confirmed against the Eleventy Data Cascade page: the seven-source priority order, leaf template precedence over layouts, deep merge of objects and arrays with the example result, and the override: prefix with the posts/firstpost.md example. Nothing removed.

Method: documentation only; no commands were run.
