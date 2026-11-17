---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-string-substitution
name: woodpecker-string-substitution
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [string-substitution, variable-expansion, escaping]
level: practitioner
status: docs-checked
description: "Use Woodpecker substitution and bash-style string operations, and escape with $$."
sources: ["https://woodpecker-ci.org/docs/usage/environment", "https://woodpecker-ci.org/docs/usage/security-boundaries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker string substitution

`${VAR}` expressions in the YAML are substituted into the YAML text before it is parsed, which allows dynamic settings, commands and filters.

```yaml
steps:
  - name: s3
    image: woodpeckerci/plugin-s3
    settings:
      target: /target/${CI_COMMIT_SHA}
```

Bash-style operations are emulated:

- `${param}` plain substitution
- `${param,}` lowercase first char; `${param,,}` lowercase all
- `${param^}` uppercase first char; `${param^^}` uppercase all
- `${param:pos}` and `${param:pos:len}` substring
- `${param=default}` default value
- `${param##prefix}` remove prefix; `${param%%suffix}` remove suffix
- `${param/old/new}` find and replace

```yaml
target: /target/${CI_COMMIT_SHA:0:8}
target: /target/${CI_COMMIT_TAG##v}
```

The first keeps the first eight characters of the commit SHA.

The second strips the `v` from a tag like `v1.0.0`.

Because substitution runs first, a shell variable you want evaluated at runtime must be escaped with `$$`:

```yaml
commands:
  - export PATH=$${PATH}:/go
```

The `environment` section does not expand variables; export them in `commands` instead. Forge values such as commit messages are untrusted; Woodpecker quotes values with line breaks so they cannot add YAML structure.

## Checked

2026-11-03. Confirmed against: environment (substitution, string operations table, escaping, environment section not expanding) and security-boundaries (untrusted forge values, line-break quoting). Removed: wording that said substitution happens before the pipeline starts (docs say it is applied to the YAML text before parsing).

Method: documentation only; no commands were run.
