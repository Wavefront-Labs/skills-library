---
id: computing-software.devops-ci-cd.concourse-ci.load-var-step
name: load-var-step
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [load-var-step, local-var, format, reveal, redaction, steps]
level: practitioner
status: docs-checked
description: "Load a file into a local build var with load_var: the format options json, yaml, trim and raw, detection by extension, structured values, and the reveal flag for redacted secrets."
sources:
  - https://concourse-ci.org/docs/steps/load-var/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`load_var: name` reads a file at runtime and exposes its content to later steps as the local var `name`, referenced as `((.:name))`.

```yaml
plan:
  - get: examples
  - load_var: version
    file: examples/misc/simple-value.txt
  - put: img
    params:
      version: ((.:version))
```

`file` is required: a path whose first segment names an artifact. `format` decides how it is read:
- `json`, `yaml` or `yml`: parsed, and the resulting structure becomes the value, so fields are addressed like `((.:version.hello))-((.:version.number))`.
- `trim`: the content with leading and trailing whitespace removed.
- `raw`: the content unmodified, whitespace included.

If `format` is unset, Concourse detects it from the file extension and falls back to `trim` when it cannot tell.

`reveal` (default `false`) allows the var's content to appear in build output even when secret redaction is on. Without it, if a file produced in a task prints the values, they are redacted automatically.

This step is how you pass dynamic data between steps. It is also the source of dynamic lists for the `across` modifier: load a JSON array into a local var, then iterate over `((.:packages))`.

## Checked

2026-11-04. Formats, detection fallback, reveal and examples confirmed on the Load Var Step page; across usage on the Across page.

Method: documentation only; no commands were run.
