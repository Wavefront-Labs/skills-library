---
id: computing-software.devops-ci-cd.helm.builtin-objects
name: builtin-objects
category: computing-software
field: devops-ci-cd
product: helm
tags: [built-in-objects, release, values, chart, files, capabilities, template, subcharts]
level: practitioner
status: docs-checked
description: "Objects available in every template: Release, Values, Chart, Subcharts, Files, Capabilities and Template with their fields."
sources:
  - "https://helm.sh/docs/chart_template_guide/builtin_objects/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Top-level objects are available to templates; names start with a capital letter.

- `.Release`: `.Name`, `.Namespace`, `.IsUpgrade`, `.IsInstall`, `.Revision` (1 on install), `.Service` (always `Helm`).
- `.Values`: values from `values.yaml`, `-f` files and `--set`. By default `Values` is empty.
- `.Chart`: contents of `Chart.yaml`, for example `.Chart.Name`, `.Chart.Version`, `.Chart.AppVersion`.
- `.Subcharts`: reach subchart scope, for example `.Subcharts.mySubChart.myValue`.
- `.Files`: access non-template files in the chart, except those excluded by `.helmignore` (see accessing files). It cannot be used to read templates. Functions: `Get`, `GetBytes`, `Glob`, `Lines`, `AsSecrets`, `AsConfig`.
- `.Capabilities`: `.APIVersions` (with `.Has "apps/v1"`), `.KubeVersion` (with `.Major`, `.Minor`, `.Version`) and `.HelmVersion`.
- `.Template`: `.Name` (path of the current template, such as `mychart/templates/mytemplate.yaml`) and `.BasePath` (`mychart/templates`).

The built-in values always begin with an uppercase letter, which is Go's exported-name convention. Your own values should start lowercase to be told apart.

Check capabilities before using newer APIs: `{{ if .Capabilities.APIVersions.Has "policy/v1" }}`.

## Checked

2026-11-08. Read the Built-in Objects page in full. Removed an unsupported Helm 4 values claim, an unsupported Chart.yaml access claim and a $.Release.Name tip; added the Files function list.

Method: documentation only; no commands were run.
