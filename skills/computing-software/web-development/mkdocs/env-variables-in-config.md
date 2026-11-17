---
id: computing-software.web-development.mkdocs.env-variables-in-config
name: env-variables-in-config
category: computing-software
field: web-development
product: mkdocs
tags: [env-variables, env-tag, config-defaults, ci-configuration]
level: practitioner
status: docs-checked
description: "Read MkDocs config values from environment variables with the !ENV tag, fallback lists with defaults, and type conversion limits."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `!ENV` to set an option from an environment variable:

```yaml
site_name: !ENV SITE_NAME
```

If the variable is undefined the value is `null`. Give a default as the last list item:

```yaml
site_name: !ENV [SITE_NAME, 'My default site name']
site_name: !ENV [SITE_NAME, OTHER_NAME, 'My default site name']
```

In a list, every item but the last is a variable name; the last is a literal default.

Type handling: simple types (string, bool, integer, float, datestamp, null) are parsed as if written in YAML, so `true` becomes a boolean. Lists and key/value mappings cannot be defined in a single variable.

A common use is toggling plugins:

```yaml
plugins:
  - search
  - code-validator:
      enabled: !ENV [LINT, false]
```

(`code-validator` is the docs' placeholder plugin name.) Implemented by the pyyaml_env_tag project.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (Special YAML tags, Environment variables; plugin enabled option): `!ENV`, null when undefined, the default as last list item, multiple fallbacks, type parsing, complex types not allowed, pyyaml_env_tag. Removed: a generic verify command.

Method: documentation only; no commands were run.
