---
id: computing-software.web-development.jekyll.liquid-error-modes
name: liquid-error-modes
category: computing-software
field: web-development
product: jekyll
tags: [liquid-config, error-mode, strict-variables, strict-filters, build-failures]
level: practitioner
status: docs-checked
description: "Make Jekyll builds fail on Liquid mistakes using error_mode (lax, warn, strict), strict_variables and strict_filters, and know they are separate settings."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/liquid.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/default.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`liquid.error_mode` sets how Liquid reacts to errors:

- `lax`: ignore all errors.
- `warn` (default): print a console warning for each error and keep building if possible.
- `strict`: print an error message and stop the build.

`strict_variables` and `strict_filters` (3.8.0+) make the renderer catch unassigned variables and non-existent filters. `error_mode` configures Liquid's parser; the other two configure its renderer, so they are orthogonal and are set separately.

To stop build or serve on any Liquid problem:

```yaml
liquid:
  error_mode: strict
  strict_variables: true
  strict_filters: true
```

The build halts and names the offending error, which helps catch Liquid issues early. Default config is `warn`, `false`, `false`.

## Checked

2026-11-04. Confirmed against the Jekyll Liquid options doc and the default configuration page: the three `error_mode` values and their behaviour, `warn` default, `strict_variables`/`strict_filters` (3.8.0), the parser-versus-renderer note, the strict example and the false defaults. Nothing removed.

Method: documentation only; no commands were run.
