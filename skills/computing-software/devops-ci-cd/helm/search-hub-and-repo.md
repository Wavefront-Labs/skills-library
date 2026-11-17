---
id: computing-software.devops-ci-cd.helm.search-hub-and-repo
name: search-hub-and-repo
category: computing-software
field: devops-ci-cd
product: helm
tags: [search, search-repo, search-hub, artifact-hub, versions, regexp]
level: intro
status: docs-checked
description: "Find charts with helm search repo (local repo index) and helm search hub (Artifact Hub), with version constraints."
sources:
  - "https://helm.sh/docs/helm/helm_search_repo/"
  - "https://helm.sh/docs/helm/helm_search_hub/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

There are two search commands with different data sources.

`helm search repo [keyword]` searches the repositories you have added, using locally cached metadata (refresh it with `helm repo update`). It shows the latest stable versions.

- `--devel` includes alpha, beta and release candidate versions (equivalent to version `>0.0.0-0`).
- `--version '^1.0.0'` filters by a semver constraint.
- `-l, --versions` lists every version of every chart on its own line.
- `-r, --regexp` treats the keyword as a regular expression.
- `--fail-on-no-result` makes an empty search exit non-zero.
- `-o` accepts table, json, yaml; `--max-col-width` defaults to 50.

```bash
helm search repo nginx-ingress --version ^1.0.0 -l
```

`helm search hub [keyword]` queries Artifact Hub (or your own hub instance). The default `--endpoint` is `https://hub.helm.sh`. The keyword may be a quoted rich query string; rich queries are not supported if the endpoint is a Monocular instance. `--list-repo-url` prints the chart repository URL so you can `helm repo add` it.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_search_repo/ and https://helm.sh/docs/helm/helm_search_hub/ (flags, --max-col-width default 50, --endpoint default, Monocular rich-query note, --list-repo-url). Removed: the closing remark about adding the repository before installing.
Method: documentation only; no commands were run.

