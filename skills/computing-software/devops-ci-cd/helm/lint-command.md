---
id: computing-software.devops-ci-cd.helm.lint-command
name: lint-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [lint, chart-validation, strict, with-subcharts, values-schema, warnings]
level: practitioner
status: docs-checked
description: "Validate a chart with helm lint: errors versus warnings, --strict, --with-subcharts and passing values for rendering."
sources:
  - "https://helm.sh/docs/helm/helm_lint/"
  - "https://helm.sh/docs/chart_best_practices/conventions/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm lint PATH` runs a series of checks that the chart is well-formed. If it finds problems that would make installation fail it prints `[ERROR]`; for issues that break convention or recommendation it prints `[WARNING]`.

```bash
helm lint ./mychart --strict --with-subcharts -f ci/values.yaml
```

Flags:

- `--strict` fails on lint warnings, so warnings break the CI job.
- `--with-subcharts` also lints dependent charts.
- `--quiet` prints only warnings and errors.
- `-f/--values`, `--set`, `--set-string`, `--set-file`, `--set-json`, `--set-literal` supply values so templates render with realistic input.
- `--skip-schema-validation` disables JSON schema validation against `values.schema.json`.

The best practices guide notes that lint validates chart names against the DNS-1123 label rules (lowercase letters, digits and dashes, starting and ending alphanumeric, at most 63 characters).

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_lint/ (flags, [ERROR] and [WARNING] wording) and https://helm.sh/docs/chart/best_practices/conventions/ (DNS-1123 chart names). Removed: the closing advice on values variants and cluster contact (not on the pages).
Method: documentation only; no commands were run.

