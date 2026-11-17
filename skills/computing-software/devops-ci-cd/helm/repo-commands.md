---
id: computing-software.devops-ci-cd.helm.repo-commands
name: repo-commands
category: computing-software
field: devops-ci-cd
product: helm
tags: [repo, repo-add, repo-update, repo-list, repo-remove, chart-repository]
level: intro
status: docs-checked
description: "Manage classic chart repositories with helm repo add, update, list and remove, and the repositories.yaml file."
sources:
  - "https://helm.sh/docs/helm/helm_repo_add/"
  - "https://helm.sh/docs/helm/helm_repo_update/"
  - "https://helm.sh/docs/helm/helm_repo_list/"
  - "https://helm.sh/docs/helm/helm_repo_remove/"
  - "https://helm.sh/docs/helm/helm/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A classic chart repository is added by name and URL, then cached locally.

```bash
helm repo add bitnami https://charts.example.com
helm repo update
helm repo list -o json
helm repo remove bitnami
```

- `helm repo add NAME URL` registers a repository. Flags: `--force-update` replaces an existing entry, `--timeout` bounds the index download (default 2m0s), and `--allow-deprecated-repos` overrides the default refusal to add official repos that have been permanently deleted. Credential and TLS flags (`--username`, `--password`, `--ca-file`, `--cert-file`, `--key-file`, `--insecure-skip-tls-verify`, `--pass-credentials`) are also available.
- `helm repo update [REPO ...]` fetches the latest index for all or named repos; the cached information is what `helm search repo` uses.
- `helm repo list` lists repositories; `-o` accepts table, json or yaml and `--no-headers` drops headers.
- `helm repo remove REPO [...]` removes one or more.

Configuration lives in the file given by `--repository-config` or `HELM_REPOSITORY_CONFIG` (default `~/.config/helm/repositories.yaml` on Linux), and cached indexes in `--repository-cache` or `HELM_REPOSITORY_CACHE`.

A `dependencies` entry in `Chart.yaml` can use `@repo-name` as the repository alias, but the repo must have been added first with `helm repo add`.

## Checked

2026-11-03. Confirmed against the helm repo add, update, list and remove reference pages on helm.sh (flags, defaults, -o values) and the helm reference (default repository paths).
Method: documentation only; no commands were run.

