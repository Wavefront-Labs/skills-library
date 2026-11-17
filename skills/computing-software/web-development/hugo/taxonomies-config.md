---
id: computing-software.web-development.hugo.taxonomies-config
name: taxonomies-config
category: computing-software
field: web-development
product: hugo
tags: [taxonomies-config, categories, tags, singular-plural, disablekinds]
level: practitioner
status: docs-checked
description: "Configure Hugo taxonomies: the default categories and tags, singular key with plural value, keeping defaults when adding one, and disabling taxonomy and term kinds."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/taxonomies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The default configuration defines two taxonomies: `categories` and `tags`.

When creating a taxonomy, use the singular form for the key and the plural for the value (`category` and `categories`). Use the value as the key in front matter, always as an array, even for one term.

```yaml
title: Example
categories:
  - vegetarian
  - gluten-free
tags:
  - appetizer
  - main course
```

Adding a taxonomy removes the defaults unless you list them too:

```toml
[taxonomies]
author = 'author'
category = 'categories'
tag = 'tags'
```

If you never expect more than one term for a taxonomy, the singular form can be used for both key and value (`author = 'author'`); the front matter value is still an array.

To turn the taxonomy system off, disable the `taxonomy` and `term` page kinds at the root of the project configuration:

```toml
disableKinds = ['taxonomy','term']
```

See the taxonomies content skill for terms, weights and term pages.

## Checked
Confirmed 2026-11-08 against the Hugo taxonomies configuration page (read in full): defaults, singular key and plural value, array front matter, keeping defaults when adding one, and disableKinds. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
