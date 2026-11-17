---
id: computing-software.web-development.jekyll.collection-query-filters
name: collection-query-filters
category: computing-software
field: web-development
product: jekyll
tags: [where-filter, where-exp, find-filter, group-by, nil-detection, binary-operators]
level: advanced
status: docs-checked
description: "Query arrays and collections in Liquid with where, where_exp, find, find_exp, group_by and group_by_exp, including nil/empty tests and and/or expressions."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/jekyll_filters.yml
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/liquid/filters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `where`: all objects whose key has the value: `{{ site.members | where:"graduation_year","2014" }}`.
- `where_exp` (3.2.0+): all objects where an expression is true.
- `find` (4.1.0): the first match or `nil`: `{{ site.members | find: "graduation_year", "2014" }}`.
- `find_exp` (4.1.0): first object for which the expression is true, else `nil`.
- `group_by`: groups items by property, returning name/items pairs.
- `group_by_exp` (3.4.0): groups by an expression.

```liquid
{{ site.members | where_exp:"item", "item.graduation_year < 2014" }}
{{ site.members | where_exp:"item", "item.projects contains 'foo'" }}
{{ site.members | group_by:"graduation_year" }}
{{ site.members | group_by_exp: "item", "item.graduation_year | truncate: 3, ''" }}
```

Detect missing values with `where` (4.0+): `nil` finds documents where the property is undefined or explicitly `nil`; the Liquid literals `empty` or `blank` find empty values:

```liquid
{% assign filtered_posts = site.posts | where: 'my_prop', nil %}
{% assign filtered_posts = site.posts | where: 'my_prop', empty %}
```

`where_exp` accepts the binary operators `and` and `or` (4.0+):

```liquid
{{ site.movies | where_exp: "item", "item.genre == 'horror' and item.language == 'English'" }}
```

## Checked

2026-11-04. Confirmed against the Jekyll Liquid filters page and jekyll_filters data: where, where_exp (3.2.0), find and find_exp (4.1.0), group_by_exp (3.4.0), nil/empty detection and and/or operators (4.0). Nothing removed.

Method: documentation only; no commands were run.
