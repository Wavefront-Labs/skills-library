---
id: computing-software.devops-ci-cd.helm.values-precedence-and-set-flags
name: values-precedence-and-set-flags
category: computing-software
field: devops-ci-cd
product: helm
tags: [values, set, set-string, set-file, set-json, values-files, precedence]
level: practitioner
status: docs-checked
description: "How Helm merges values from values.yaml, -f files and the --set family, plus the escaping rules for commas and dots."
sources:
  - https://helm.sh/docs/intro/using_helm/
  - https://helm.sh/docs/chart_template_guide/values_files/
  - https://helm.sh/docs/helm/helm_install/
  - https://helm.sh/docs/helm/helm_upgrade/
  - https://helm.sh/docs/chart_best_practices/values/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Values reach templates in order of increasing specificity: the chart's `values.yaml`, a parent chart's `values.yaml` (for a subchart), a file passed with `-f/--values`, then `--set` style parameters. `-f` can be repeated and the rightmost file wins; `--set` can be repeated and the rightmost wins. When both are used, `--set` values are merged into the `--values` result with higher precedence. Overrides given with `--set` are persisted in a Secret with the release.

The flag family on install and upgrade (the reference pages list them for both):

- `--set a=b,c=d` for scalars; dotted paths such as `outer.inner=value` build nested maps; lists use braces (`--set name={a,b,c}`) or an index (`--set servers[0].port=80`).
- `--set-string` forces a string (reference example: `long_int=1234567890`).
- `--set-file key=path` reads a value from a file, for values too long for the command line or generated.
- `--set-json 'key=[{"a":1}]'` sets scalars, objects or arrays as JSON. Repeating it for the same key replaces the earlier value, and `--set-json='foo.key2="bar"'` can override one key of an earlier object.
- `--set-literal` sets a literal string value.
- `--set name=[],a=null` produces an empty array and a null.

Escaping: use a backslash for commas (`--set name=value1\,value2` gives `value1,value2`) and for dots inside a key, for example `--set nodeSelector."kubernetes\.io/role"=master`.

To delete a key coming from chart defaults, override it with null. The values guide's example: setting `livenessProbe.exec.command` alone leaves the default `httpGet` in place because the maps are coalesced, so also pass `--set livenessProbe.httpGet=null` when switching a probe to `exec`.

Inspect the user-supplied values of a release with `helm get values RELEASE`. On `helm upgrade`:

- `--reset-values` resets to the values built into the chart.
- `--reuse-values` reuses the last release's values and merges new `--set`/`-f` overrides over them (and is ignored if `--reset-values` is given).
- `--reset-then-reuse-values` resets to the chart's built-in values, applies the last release's values, then merges command-line overrides.

Chart authors: `--set` is less expressive than a file, so the best-practices guide advises structuring values as maps rather than lists of maps so `--set servers.foo.port=80` works.

## Checked

2026-11-08. Checked against the Helm 4 values and install/upgrade command pages (flag lists read as references, install and upgrade sections grepped for the cited flags). Removed unsourced claims.

Method: documentation only; no commands were run.
