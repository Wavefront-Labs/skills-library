---
id: computing-software.devops-ci-cd.helm.accessing-files-in-templates
name: accessing-files-in-templates
category: computing-software
field: devops-ci-cd
product: helm
tags: [files, glob, get, lines, as-secrets, as-config, helmignore, configmap]
level: practitioner
status: docs-checked
description: "Read chart files from templates with .Files: Get, GetBytes, Glob, Lines, AsConfig, AsSecrets, plus .helmignore rules."
sources:
  - "https://helm.sh/docs/chart_template_guide/accessing_files/"
  - "https://helm.sh/docs/topics/charts/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Helm provides `.Files` for chart files that are not templates:

- `.Files.Get "config.toml"`: file contents as a string.
- `.Files.GetBytes "x.bin"`: contents as bytes.
- `.Files.Glob "foo/*"`: returns a `Files` type for the pattern matches, so you can call any `Files` method on the result; patterns such as `**.yaml` work.
- `.Files.Lines "file"`: iterate lines. A file that is empty or missing gives an empty list rather than a render failure.
- `.Files.AsConfig`: file bodies as a YAML map, for ConfigMap data.
- `.Files.AsSecrets`: file bodies as base64-encoded strings, for Secret data.

```yaml
data:
  {{- (.Files.Glob "foo/*").AsConfig | nindent 2 }}
```

Constraints:

- Files in `templates/` cannot be accessed through `.Files`.
- Files excluded using `.helmignore` cannot be accessed.
- Files outside a Helm application subchart, including those of the parent, cannot be accessed.
- Charts do not preserve UNIX mode information, so file permissions have no effect on `.Files` availability.
- Extra files are bundled with the chart, which must be smaller than 1M because of Kubernetes object storage limits.
- You cannot pass external files during `helm install`; supply user data with `-f` or `--set`.

Use `{{ .Files.Get "config1.toml" | b64enc }}` to base64-encode a file for a Secret's `data`. Path helpers imported from Go's `path` package are lowercase: `base`, `dir`, `ext`, `isAbs`, `clean`.

## Checked

2026-11-08. Read the Accessing Files page in full. Fixed an invalid AsConfig pipe example, removed unsupported claims (.gitignore syntax, tpl, ConfigMap 1 MiB limit wording); added the documented constraints, Lines behaviour and path helpers.

Method: documentation only; no commands were run.
