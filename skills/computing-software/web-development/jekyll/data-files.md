---
id: computing-software.web-development.jekyll.data-files
name: data-files
category: computing-software
field: web-development
product: jekyll
tags: [data-files, site-data, data-subfolders, author-lookup, yaml-json-csv]
level: practitioner
status: docs-checked
description: "Load YAML, JSON, CSV and TSV from _data into site.data, use subfolder namespaces, and look up an item such as an author by a front matter key."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/datafiles.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/front-matter-defaults.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Files in `_data` with `.yml`, `.yaml`, `.json`, `.tsv` or `.csv` extensions are available as `site.data`. CSV and TSV must have a header row. The file basename sets the variable name (`members.yml` becomes `site.data.members`), so avoid the same basename with different extensions in one directory.

```liquid
<ul>
{% for member in site.data.members %}
  <li><a href="https://github.com/{{ member.github }}">{{ member.name }}</a></li>
{% endfor %}
</ul>
```

Subfolders add namespace levels: `_data/orgs/jekyll.yml` is `site.data.orgs.jekyll`. Iterating `site.data.orgs` yields pairs, so take `org_hash[1]`:

```liquid
{% for org_hash in site.data.orgs %}
{% assign org = org_hash[1] %}
  {{ org.name }} ({{ org.members | size }} members)
{% endfor %}
```

Look up a specific item with a front matter key. With `_data/people.yml` keyed by `dave` and a post containing `author: dave`:

```liquid
{% assign author = site.data.people[page.author] %}
{{ author.name }}
```

Data files are reloaded during automatic regeneration (unlike `_config.yml`). Plugins and themes can also use data files for configuration.

## Checked

2026-11-04. Confirmed against the Jekyll data files doc and the front matter defaults doc: supported extensions, header-row requirement, basename rule, members example, subfolder namespacing with `org_hash[1]`, the `people` lookup by `page.author`, the reload note, and plugin/theme use. Nothing removed.

Method: documentation only; no commands were run.
