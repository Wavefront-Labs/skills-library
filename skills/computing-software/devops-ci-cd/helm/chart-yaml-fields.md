---
id: computing-software.devops-ci-cd.helm.chart-yaml-fields
name: chart-yaml-fields
category: computing-software
field: devops-ci-cd
product: helm
tags: [chart-yaml, api-version, app-version, metadata, annotations, maintainers, deprecated]
level: practitioner
status: docs-checked
description: "Every Chart.yaml field: required versus optional, apiVersion v2, appVersion quoting, maintainers, deprecation and annotations."
sources:
  - "https://helm.sh/docs/topics/charts/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`Chart.yaml` is required. Fields:

- Required: `apiVersion`, `name`, `version`.
- Optional: `kubeVersion`, `description`, `type`, `keywords`, `home`, `sources`, `dependencies`, `maintainers`, `icon`, `appVersion`, `deprecated`, `annotations`.

`apiVersion` should be `v2` for charts needing Helm 3 or later. `v1` charts are still installable. v2 added the `dependencies` field (v1 used a separate `requirements.yaml`) and the `type` field.

`appVersion` is informational, unrelated to `version`, and need not be SemVer. Quote it: YAML reads `1.0` as a float and `1234e10` as scientific notation. `helm create` has quoted the default since Helm 3.5.0.

`maintainers` entries need a `name`; `email` and `url` are optional.

`icon` is a URL to an SVG or PNG.

`deprecated: true` on the newest version marks the whole chart deprecated. Workflow: mark it in `Chart.yaml` and bump the version, release it to the repository, then remove the chart from source control. The name can be reused later by publishing a non-deprecated version.

Since Helm v3.3.2 additional fields are not allowed; put custom metadata in `annotations`. Unknown fields are dropped and are not visible in `.Chart` inside templates.

The `Chart` object exposes these fields to templates, for example `{{ .Chart.Name }}-{{ .Chart.Version }}`.

## Checked

2026-11-08. Read the Charts topic page in full (helm-www v3 docs source); the field list, apiVersion v1/v2 differences, appVersion quoting, v3.3.2 and v3.5.0 notes, deprecation workflow and annotations all match. No changes.

Method: documentation only; no commands were run.
