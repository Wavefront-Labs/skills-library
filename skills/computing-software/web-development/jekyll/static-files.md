---
id: computing-software.web-development.jekyll.static-files
name: static-files
category: computing-software
field: web-development
product: jekyll
tags: [static-files, site-static-files, file-metadata, defaults-for-static-files]
level: practitioner
status: docs-checked
description: "List and filter Jekyll static files via site.static_files, read path, name, basename, extname and modified_time, and tag them through front matter defaults."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/static_files.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A static file has no front matter: images, PDFs and other un-rendered content. They are available in Liquid as `site.static_files`, each with:

- `file.path`: relative path, e.g. `/assets/img/image.jpg`.
- `file.modified_time`: the `Time` it was last modified.
- `file.name`: e.g. `image.jpg`.
- `file.basename`: e.g. `image`.
- `file.extname`: e.g. `.jpg`.

`file` is just a loop variable of your own, not a global.

You cannot put front matter in a static file, but you can give it values with `defaults`:

```yaml
defaults:
  - scope:
      path: "assets/img"
    values:
      image: true
```

Each file under `assets/img` is then treated as having `image: true`, so you can filter:

```liquid
{% assign image_files = site.static_files | where: "image", true %}
{% for myimage in image_files %}
  {{ myimage.path }}
{% endfor %}
```

Output lists the path of every static file matching the condition.

## Checked

2026-11-04. Confirmed against the Jekyll static files doc: definition, the five `site.static_files` properties with examples, the note that `file` is an arbitrary loop variable, and the `defaults` plus `where` filter example. Nothing removed.

Method: documentation only; no commands were run.
