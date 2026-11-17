---
id: computing-software.devops-ci-cd.helm.chart-directory-structure
name: chart-directory-structure
category: computing-software
field: devops-ci-cd
product: helm
tags: [chart-structure, chart-yaml, values-yaml, templates-dir, charts-dir, crds-dir, helm-create]
level: intro
status: docs-checked
description: "The files and directories a Helm chart expects, which names Helm reserves, and what helm create scaffolds."
sources:
  - "https://helm.sh/docs/topics/charts/"
  - "https://helm.sh/docs/helm/helm_create/"
  - "https://helm.sh/docs/chart_template_guide/named_templates/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A chart is a directory whose name is the chart name (without version). Helm expects:

```text
wordpress/
  Chart.yaml          required metadata
  LICENSE             optional
  README.md           optional, shown by hubs
  values.yaml         default configuration values
  values.schema.json  optional JSON Schema for values
  charts/             dependency charts
  crds/               Custom Resource Definitions
  templates/          templates rendered with values
  templates/NOTES.txt optional usage notes
```

Helm reserves `charts/`, `crds/` and `templates/` and the listed file names; other files are left as they are but only non-excluded ones are readable through `.Files`.

`helm create NAME` scaffolds a chart: `.helmignore` (patterns to ignore when packaging), `Chart.yaml`, `values.yaml`, `charts/`, `templates/` and `templates/tests/`. Existing directories are not wiped: conflicting files are overwritten but others are left. `-p, --starter` uses a starter scaffold by name or absolute path.

Most files in `templates/` are treated as Kubernetes manifests; `NOTES.txt` is an exception. Files whose names begin with an underscore (conventionally `_helpers.tpl`) hold partials and are not rendered to manifests.

Unknown fields in `Chart.yaml` are dropped, so a chart cannot carry arbitrary metadata there; use `annotations`.

## Checked

2026-11-08. Read the Charts topic, helm create and Named Templates pages in full. Added the underscore-file rule from Named Templates and its source. Other claims confirmed.

Method: documentation only; no commands were run.
