---
id: computing-software.devops-ci-cd.helm.named-templates-and-include
name: named-templates-and-include
category: computing-software
field: devops-ci-cd
product: helm
tags: [named-templates, define, template, include, block, helpers-tpl, partials, nindent]
level: practitioner
status: docs-checked
description: "Define reusable named templates with define in _helpers.tpl and call them with include (not template) to pipe the output."
sources:
  - "https://helm.sh/docs/chart_template_guide/named_templates/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Named templates are declared with `define` and are global: names are shared by the chart and all subcharts, so prefix them with the chart name to avoid collisions.

```yaml
{{- define "mychart.labels" }}
labels:
  generator: helm
  date: {{ now | htmlDate }}
{{- end }}
```

Convention: store them in `templates/_helpers.tpl`. Files whose name begins with `_` are not rendered as manifests.

Call them with:

- `{{ template "mychart.labels" . }}`: inserts the output; it is an action, not a function, so you cannot pipe its result.
- `{{ include "mychart.labels" . }}`: a function returning a string, so `{{ include "mychart.labels" . | nindent 4 }}` works. Prefer `include`.
- `block` is the third declaring action besides `define` and `template` (covered in the flow-control section of the guide, not here).

The dot you pass is the scope. Pass `.` to give the template access to `.Chart`, `.Values` and `.Release`; passing nothing leaves it empty, so `.Chart.Name` renders blank. Inside the named template `$` refers to the scope you passed in, not a global scope.

Gotchas:

- Template names are global. With two definitions of the same name, whichever loads last is used. Subchart templates are compiled together with the parent's. The same applies across versions of a chart, so a version in the name (`mychart.v1.labels`) can work around it.
- `template` inserts text unchanged, so indentation is wrong when the output is nested; `include ... | nindent N` fixes it. The guide says to prefer `include` over `template` for this reason.
- By convention a `define` has a short documentation block, `{{/* Generate basic labels */}}`.

## Checked

2026-11-08. Read the Named Templates page in full. Removed unsupported claims (alphabetical load order with subcharts first, dict example, doc-comment format) and the block bullet; added the documented global-name, versioned-name, scope and nindent facts.

Method: documentation only; no commands were run.
