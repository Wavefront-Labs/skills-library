---
id: computing-software.devops-ci-cd.helm.dependency-conditions-tags-import
name: dependency-conditions-tags-import
category: computing-software
field: devops-ci-cd
product: helm
tags: [condition, tags, import-values, exports, dependencies, subchart-toggle]
level: advanced
status: docs-checked
description: "Enable or disable subcharts with condition and tags, and pull child values into the parent with import-values."
sources:
  - "https://helm.sh/docs/topics/charts/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Every dependency loads by default. `condition` and `tags` change that.

```yaml
dependencies:
  - name: subchart1
    version: 0.1.0
    repository: http://localhost:10191
    condition: subchart1.enabled,global.subchart1.enabled
    tags: [front-end, subchart1]
```

- `condition` holds one or more comma-separated YAML paths. Only the first path that exists in the top parent's values and resolves to a boolean applies; if none exist, it has no effect.
- `tags` are labels. In the parent values, `tags: {front-end: false}` disables every chart with that tag. A chart is enabled if any of its tags is true.
- Conditions override tags. Both must be set in the top-level parent's values; `tags:` must be a top-level key (no nested or global tags).
- Override from the CLI: `--set tags.front-end=true --set subchart2.enabled=false`.

`import-values` copies values from a child to the parent:

- Exports format: the child's `values.yaml` has an `exports:` map; `import-values: [data]` merges `exports.data` into the parent's root values (the `data` key itself is not kept).
- Child-parent format: `import-values: [{child: default.data, parent: myimports}]` copies values at the child path to the parent path.

Example: with `default.data` in the child holding `myint: 999` and `mybool: true`, and the parent's `myimports` holding `myint: 0`, `mybool: false`, `mystring: "helm rocks!"`, the parent ends with `myint: 999`, `mybool: true`, `mystring: "helm rocks!"`.

## Checked

2026-11-08. Read the Charts topic page in full. Removed an unsupported statement about templates and final values and an overstated 'overriding' claim; replaced with the page's child-parent import example.

Method: documentation only; no commands were run.
