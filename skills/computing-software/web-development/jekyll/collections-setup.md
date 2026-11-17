---
id: computing-software.web-development.jekyll.collections-setup
name: collections-setup
category: computing-software
field: web-development
product: jekyll
tags: [collections, collections-dir, collection-folder, collection-output, future-documents]
level: practitioner
status: docs-checked
description: "Define Jekyll collections as a list or mapping, add documents in _name folders, set output and future, and gather them under collections_dir."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/collections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Define a collection in `_config.yml`, as a sequence or, for metadata, a mapping:

```yaml
collections:
  - staff_members
```

```yaml
collections:
  staff_members:
    output: true
```

A sequence leaves pages unrendered; `output: true` needs the mapping form.

Add documents in a folder named exactly like the collection with a leading underscore, e.g. `_staff_members/jane.md`. Front matter is processed and the rest becomes `content`. A file with no front matter is treated as a static file. Files are written to the destination only if `output: true`. (Posts are the exception: valid filenames are processed without front matter.)

Loop and link:

```liquid
{% for staff_member in site.staff_members %}
  <h2><a href="{{ staff_member.url }}">{{ staff_member.name }}</a></h2>
  <p>{{ staff_member.content | markdownify }}</p>
{% endfor %}
```

Show future-dated items per collection:

```yaml
collections:
  staff_members:
    future: true
```

`collections_dir: my_collections` (3.7.0+) gathers them; Jekyll then looks in `my_collections/_books`. Move `_drafts` and `_posts` inside it too, and the directory name cannot start with an underscore.

## Checked

2026-11-04. Confirmed against the Jekyll Collections page: sequence versus mapping form, folder naming, output, future, collections_dir (3.7.0) and the underscore rule. Nothing removed.

Method: documentation only; no commands were run.
