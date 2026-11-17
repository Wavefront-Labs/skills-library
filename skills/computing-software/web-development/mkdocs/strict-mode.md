---
id: computing-software.web-development.mkdocs.strict-mode
name: strict-mode
category: computing-software
field: web-development
product: mkdocs
tags: [strict-mode, warnings, ci-build, build-flags]
level: practitioner
status: docs-checked
description: "Make MkDocs halt on warnings with strict: true or --strict, useful for continuous testing of broken links and plugin warnings."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`strict` decides how warnings are handled. `true` halts processing when a warning is raised; `false` (default) prints the warning and continues.

```yaml
strict: true
```

Or per run:

```bash
mkdocs build --strict
```

Typical CI use: combine with `validation` severities set to `warn`, so broken links, missing anchors and omitted nav files fail the job.

```yaml
validation:
  links:
    not_found: warn
    anchors: warn
```

Plugin and hook authors: a `log.warning(...)` under the `mkdocs.plugins.` logger namespace breaks the build when `--strict` is passed.

Gotcha: `prebuild_index: true` on the search plugin only issues a warning if Node.js cannot be called; with `--strict` that failure raises an error.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (strict, validation, prebuild_index) and the Plugins guide (log warnings under the `mkdocs.plugins.` namespace break the build with `--strict`). Removed: an exit-code verify line the pages do not state.

Method: documentation only; no commands were run.
