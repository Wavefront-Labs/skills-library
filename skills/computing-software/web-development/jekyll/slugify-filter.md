---
id: computing-software.web-development.jekyll.slugify-filter
name: slugify-filter
category: computing-software
field: web-development
product: jekyll
tags: [slugify, url-slugs, slugify-modes, transliteration]
level: practitioner
status: docs-checked
description: "Turn strings into URL slugs with Jekyll's slugify filter and choose among the none, raw, default, pretty, ascii and latin modes."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/liquid/filters.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/jekyll_filters.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`slugify` converts a string into a lowercase URL slug. The optional mode says what to filter; the default is `default`.

- `none`: no characters.
- `raw`: spaces.
- `default`: spaces and non-alphanumeric characters.
- `pretty`: spaces and non-alphanumeric characters except `._~!$&'()+,;=@`.
- `ascii`: spaces, non-alphanumeric and non-ASCII characters.
- `latin`: like `default`, except Latin characters are first transliterated, e.g. `àèïòü` to `aeiou` (3.7.0+).

```liquid
{{ "The _config.yml file" | slugify }}           => the-config-yml-file
{{ "The _config.yml file" | slugify: "pretty" }} => the-_config.yml-file
{{ "The _cönfig.yml file" | slugify: "ascii" }}  => the-c-nfig-yml-file
{{ "The cönfig.yml file" | slugify: "latin" }}   => the-config-yml-file
```

## Checked

2026-11-04. Confirmed against the Jekyll Liquid filters page: slugify modes and examples. Removed the closing line about the permalink :name and :title placeholders, which these pages do not state.

Method: documentation only; no commands were run.
