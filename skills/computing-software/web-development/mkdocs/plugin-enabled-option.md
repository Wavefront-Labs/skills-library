---
id: computing-software.web-development.mkdocs.plugin-enabled-option
name: plugin-enabled-option
category: computing-software
field: web-development
product: mkdocs
tags: [plugin-enabled, plugins, env-variables, conditional-plugins]
level: advanced
status: docs-checked
description: "Toggle any MkDocs plugin on or off with the universal enabled option (1.6+), typically driven by an environment variable."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since 1.6 MkDocs guarantees every plugin has a boolean `enabled` option, on top of the plugin's own keys. Combine with `!ENV` to switch a plugin per environment:

```yaml
plugins:
  - search
  - code-validator:
      enabled: !ENV [LINT, false]
```

Here `code-validator` is the docs' placeholder name. With no `LINT` variable the plugin is off; set `LINT=true` to enable it.

```bash
LINT=true mkdocs build
```

Gotcha: `enabled` is read as a boolean; the `!ENV` default list `[LINT, false]` supplies `false` when the variable is absent (see `env-variables-in-config`).

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (plugins, `enabled` option, new in 1.6, and Environment variables): the boolean `enabled` option on every plugin and the `!ENV [LINT, false]` example. Removed: a use-case claim and a generic verify line.

Method: documentation only; no commands were run.
