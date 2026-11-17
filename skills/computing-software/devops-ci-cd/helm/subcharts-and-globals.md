---
id: computing-software.devops-ci-cd.helm.subcharts-and-globals
name: subcharts-and-globals
category: computing-software
field: devops-ci-cd
product: helm
tags: [subcharts, global-values, values-scope, parent-chart, subchart-values, dependencies]
level: practitioner
status: docs-checked
description: "How subchart values work: stand-alone scope, parent overrides by chart name, global values and .Subcharts access."
sources:
  - "https://helm.sh/docs/chart_template_guide/subcharts_and_globals/"
  - "https://helm.sh/docs/topics/charts/"
  - "https://helm.sh/docs/chart_template_guide/builtin_objects/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A subchart is stand-alone: it never depends on its parent, so it cannot read the parent's values. The parent can override a subchart's values by nesting them under the subchart's name in the parent's `values.yaml`.

```yaml
# parent values.yaml
mysubchart:
  dessert: cake
```

Values from the parent take precedence over those in the subchart's own `values.yaml`.

Global values are shared by all charts. A `global:` map in the parent is visible as `.Values.global.*` in every subchart. Rules from the guide:

- If a subchart declares a global, it passes downward to its own subcharts but not upward to the parent.
- Parent globals take precedence over subchart globals.
- A subchart cannot influence the parent's values.
- Globals suit things like shared labels.

Templates in the parent can reach a subchart's scope with `.Subcharts.mySubChart.myValue`.

Because every subchart is a full chart, you can test it alone: `helm install --generate-name --dry-run --debug mychart/charts/mysubchart`.

Globals require explicit declaration: you cannot use an existing non-global as if it were one. Named templates are global across the parent and subcharts, so prefix them with the chart name. The guide advises against `block` for overriding, since which of several implementations is selected is unpredictable; use `include` instead. Schema validation also covers subcharts: the final values are checked against every subchart's `values.schema.json`, so a parent cannot circumvent a subchart's restrictions.

## Checked

2026-11-08. Read the Subcharts and Global Values page in full and the Charts topic and Built-in Objects pages. Claims confirmed; added the explicit-declaration rule and the guide's advice against block.

Method: documentation only; no commands were run.
