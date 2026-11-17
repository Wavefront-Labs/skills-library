---
id: computing-software.web-development.hugo.menus-in-config
name: menus-in-config
category: computing-software
field: web-development
product: hugo
tags: [menus, menu-entries, pageref, nested-menu, site-menus]
level: practitioner
status: docs-checked
description: "Define Hugo menus in project configuration with name, weight, pageRef or url, nest entries with parent, and loop over site.Menus in a template."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/menus.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Menu entries can be defined automatically, in front matter, or in project configuration. Configured menus live under `menus.<NAME>` and are read with the `Menus` method on `Site`.

Entries usually have `name`, `weight` and either `pageRef` or `url`. `pageRef` is the logical path of an internal target; `url` is for external destinations only.

| Page kind | pageRef |
|---|---|
| home | `/` |
| page | `/books/book-1` |
| section | `/books` |
| taxonomy | `/tags` |
| term | `/tags/foo` |

```toml
[[menus.main]]
name = 'Products'
pageRef = '/products'
weight = 10

[[menus.main]]
name = 'Hardware'
pageRef = '/products/hardware'
parent = 'Products'
weight = 1

[[menus.main]]
name = 'Hugo'
pre = '<i class="fa fa-heart"></i>'
url = 'https://gohugo.io/'
weight = 30
[menus.main.params]
rel = 'external'
```

`parent` creates nested entries.

Template access:

```go-html-template
{{ range site.Menus.main }}
  ...
{{ end }}
```

In a `config` directory, per-language files such as `menus.en.toml` use `[[main]]` instead of `[[menus.main]]`.

## Checked

2026-11-04: definition methods, menus.NAME layout, name/weight/pageRef/url properties, pageRef table, nested parent example, site.Menus access (Configure menus page) and the [[main]] form in per-language config files (Configuration introduction page) confirmed. Nothing removed.

Method: documentation only; no commands were run.
