---
id: computing-software.web-development.hugo.taxonomies-content
name: taxonomies-content
category: computing-software
field: web-development
product: hugo
tags: [taxonomies, terms, term-pages, taxonomy-weight, getterms]
level: practitioner
status: docs-checked
description: "Use Hugo taxonomies in content: assign terms in front matter, taxonomy weight, term pages with metadata, and list terms in taxonomy and term templates."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/taxonomies.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/front-matter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A taxonomy is a classification, a term is a key within it, and a value is a piece of content assigned to a term. Terms are strings in a flat list.

Assign terms with the plural taxonomy name in front matter, as an array even for one term:

```toml
title = 'Unbreakable'
actors = ['Bruce Willis','Samuel L. Jackson']
directors = ['M. Night Shyamalan']
```

Hugo creates a page listing all terms and a list page per term, for example `/categories/development/`.

Weights: `[taxonomy_name]_weight` in front matter. In the docs example (`weight = 10`, `tags_weight = 1000`) the page floats toward the top of section and home lists and sinks toward the bottom of the `chemistry` and `science` term pages.

```toml
weight = 10
tags_weight = 1000
tags = ['chemistry','science']
```

Term metadata: a branch bundle per term, such as `content/authors/jsmith/_index.md`, may carry front matter and resources. A taxonomy template can read it:

```go-html-template
{{ range .Data.Terms.Alphabetical }}
  <h2><a href="{{ .Page.RelPermalink }}">{{ .Page.LinkTitle }}</a></h2>
{{ end }}
```

Custom `taxonomy.html` and `term.html` can be placed in `layouts/<taxonomy>/`. Terms can be added to `home`, `page`, `section`, `taxonomy` and `term` kinds; read them with `Params` or `GetTerms`:

```go-html-template
{{ with .GetTerms "tags" }}...{{ end }}
```

Term metadata example: a taxonomy configured as `author = 'authors'` with `content/authors/jsmith/_index.md` (front matter `title`, `affiliation`) and `portrait.jpg` beside it. In `layouts/authors/term.html` read `.Params.affiliation` and `.Resources.Get "portrait.jpg"`; in `layouts/authors/taxonomy.html` read them through `.Page` while ranging `.Data.Terms.Alphabetical`.

## Checked
Confirmed 2026-11-08 against the Hugo taxonomies page and the taxonomies section of the front matter page (both read in full): definitions, front matter assignment, default destinations, weights, term metadata and the page kinds that accept terms. Reworded the weight claim to what the docs example states and added the metadata example.
Method: docs-only read of cited pages, 2026-11-08
