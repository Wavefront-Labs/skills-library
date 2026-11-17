---
id: computing-software.devops-ci-cd.helm.dependencies-in-chart-yaml
name: dependencies-in-chart-yaml
category: computing-software
field: devops-ci-cd
product: helm
tags: [dependencies, subcharts, alias, repository, chart-yaml, charts-dir]
level: practitioner
status: docs-checked
description: "Declare chart dependencies in Chart.yaml with name, version, repository (URL or @alias), alias and manual charts/ vendoring."
sources:
  - "https://helm.sh/docs/topics/charts/"
  - "https://helm.sh/docs/chart_best_practices/dependencies/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Dependencies are a list in `Chart.yaml`:

```yaml
dependencies:
  - name: apache
    version: 1.2.3
    repository: https://example.com/charts
  - name: awesomeness
    version: 1.0.0
    repository: "@fantastic-charts"
```

- `name` is the chart name, `version` the chart version; `repository` is the full URL, or the repo name as `@repo-name` or `alias:repo-name` for a repo added via `helm repo add`.
- `alias` lets the same chart appear several times under different names (three entries of `subchart` become `subchart`, `new-subchart-1`, `new-subchart-2`).
- `condition`, `tags` and `import-values` control loading and values.

`helm dependency update` downloads archives into `charts/` (for example `apache-1.2.3.tgz`).

Manual option: copy unpacked chart directories into `charts/`. Names starting with `_` or `.` are ignored by the loader. `helm pull` is the easy way to fetch one.

Best practices: prefer version ranges, with a patch-level match like `~1.2.3` (`>= 1.2.3, < 1.3.0`) as the suggested default. Use `https://` URLs first, then `http://`. `file://` is a special case for fixed pipelines. If `repository` is blank, Helm assumes the dependency is already in `charts/` and cannot manage it.

On install, the parent and its dependencies form a single release: all objects are aggregated, sorted by type then name, and applied in that order (install order of kinds is the InstallOrder list in Helm's kind_sorter.go).

## Checked

2026-11-08. Read the Charts topic and Dependencies best-practices pages in full. Removed an unsupported oci:// repository claim and the 'name and version are required' claim; corrected the install ordering statement (sorted by type then name, InstallOrder in kind_sorter.go).

Method: documentation only; no commands were run.
