---
id: computing-software.devops-ci-cd.gitlab-ci.variables-expand-false-raw-values-and-dollar-escaping
name: variables-expand-false-raw-values-and-dollar-escaping
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, expand-false, raw-variables, variable-expansion, dollar-escaping]
level: practitioner
status: docs-checked
description: "Stop GitLab CI from expanding $ in variable values: variables expand false, raw values, $$ escaping, and UI variable expansion."
sources: ["https://docs.gitlab.com/ci/variables/", "https://docs.gitlab.com/ci/yaml/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables: expand false and raw values

**Goal:** a value containing `$` (passwords, regexes, shell snippets) reaches the job unchanged.

## YAML variables
```yaml
variables:
  GREETING: "hello $USER_NAME"            # expanded: references to other variables resolve
  PATTERN:
    value: '^v[0-9]+\.[0-9]+$'
    expand: false                         # raw: stays literally as written
```
- `expand: false` marks a single variable raw. The long form with `value:` is required to add the key.
- `expand` works with `default` and job `variables` only; it cannot be used with `rules:variables` or `workflow:rules:variables`.

## UI / API variables
Variables created in Settings > CI/CD are not expanded by default (default changed in GitLab 18.6); the checkbox is **Expand variable reference**. Do not mask a value you want expanded: with masking, character limits prevent using `$` to reference other variables.

## Shell vs GitLab expansion
Two stages exist: GitLab expands references when it builds the job variables; then the shell expands `$VAR` in `script`. A raw variable skips the first only. To keep the shell from expanding, single-quote it in `script` or use `"${VAR}"` knowingly.

## Gotchas
- Debug with `echo "$VAR" | od -c` in a throwaway job, never with secrets in shared logs.

## Verify
A job that prints a non-secret raw value (`printf '%s\n' "$PATTERN"`) shows the literal text including `$`.

## Checked

2026-11-02. Confirmed: `variables:expand` (true by default), VAR2/VAR3 example behaviour, the restriction on `rules:variables`; UI variables not expanded by default (18.6) and the Expand variable reference checkbox; masking/expansion conflict (GitLab CI/CD YAML reference and variables docs). Removed: the incorrect claim that expand can be set in rules:variables, `$$` escaping and downstream/mask bullets (not found in fetched pages).

Method: documentation only; no commands were run.
