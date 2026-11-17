---
id: computing-software.web-development.hugo.site-params
name: site-params
category: computing-software
field: web-development
product: hugo
tags: [params, site-params, custom-parameters, multilingual-params, namespacing]
level: intro
status: docs-checked
description: "Define custom site parameters under params, read them with site.Params, avoid kebab-case keys, set per-language params, and namespace theme or module settings."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/params.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Custom site parameters go under `params` and are read with the `Params` method on `Site`.

```toml
baseURL = 'https://example.org/'
locale = 'en-US'
title = 'Project Documentation'
[params]
subtitle = 'Reference, Tutorials, and Explanations'
[params.contact]
email = 'info@example.org'
phone = '+1 206-555-1212'
```

```go-html-template
{{ site.Params.subtitle }} → Reference, Tutorials, and Explanations
{{ site.Params.contact.email }} → info@example.org
```

Key names should be camelCase or snake_case. Kebab-case keys are allowed in TOML, YAML and JSON but are not valid identifiers and cannot be chained:

```go-html-template
{{ site.Params.camelCase.foo }}
{{ site.Params.snake_case.foo }}
```

`{{ site.Params.kebab-case.foo }}` is invalid.

Multilingual projects define a `params` key under each language:

```toml
[languages.de.params]
subtitle = 'Referenz, Tutorials und Erklärungen'
[languages.de.params.contact]
email = 'info@de.example.org'
```

Module and theme developers should namespace their parameters to prevent naming conflicts, for example under `[params.modules.myModule.colors]`, and read them from a single variable such as `$cfg`.

## Checked

2026-11-04: params key, Site Params access, key-naming rule and kebab-case limit, per-language params and namespacing guidance confirmed against the Hugo docs Configure params page. Nothing removed.

Method: documentation only; no commands were run.
