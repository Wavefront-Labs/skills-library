---
id: computing-software.web-development.mkdocs.search-languages
name: search-languages
category: computing-software
field: web-development
product: mkdocs
tags: [search-languages, lunr-languages, locale, search-plugin]
level: practitioner
status: docs-checked
description: "Choose search index languages with the search plugin lang option using ISO 639-1 codes, supported list, and the bandwidth warning."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/localizing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`lang` is a list of ISO 639-1 codes used when building the search index:

```yaml
plugins:
  - search:
      lang:
        - en
        - de
```

Supported via Lunr Languages: `ar`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `hu`, `it`, `ja`, `no`, `pt`, `ro`, `ru`, `es`, `sv`, `th`, `tr`, `vi`.

Default: the value of `theme.locale` if set, otherwise `[en]`.

Gotchas:
- Multiple languages work, but each added language adds significant bandwidth and browser load; keep each MkDocs instance to one language if you can.
- Chinese and other Asian languages are not supported; some users report decent results with Japanese.
- More languages can be contributed to Lunr Languages.

Related: `localize-theme` (translates UI text only).

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (search `lang`): ISO 639-1 codes, the 19 supported codes, default from `theme.locale` else `[en]`, the bandwidth warning, and the Asian-language note; and against Localizing Your Theme (translates theme text only). Removed: a generic verify line.

Method: documentation only; no commands were run.
