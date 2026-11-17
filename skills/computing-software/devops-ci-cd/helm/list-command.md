---
id: computing-software.devops-ci-cd.helm.list-command
name: list-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [list, releases, filter, selector, pagination, output-format]
level: intro
status: docs-checked
description: "List releases with helm list: status filters, namespaces, regex filter, label selector, sorting and paging."
sources:
  - "https://helm.sh/docs/helm/helm_list/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm list` lists releases in the current namespace (or `-n`). By default it shows releases in any status.

Status filters can be combined: `--deployed`, `--failed`, `--pending`, `--superseded`, `--uninstalled` (only with `--keep-history` uninstalls) and `--uninstalling`.

```bash
helm list -A
helm list --deployed --failed
helm list --filter 'ara[a-z]+' -o json
helm list -l app=web --short
```

Other flags:

- `-A, --all-namespaces` lists every namespace.
- `-f, --filter` is a Perl-compatible regular expression applied to release names.
- `-l, --selector` filters on labels with `=`, `==` and `!=`; it works only for the secret (default) and configmap storage backends.
- `-d, --date` sorts by release date and `-r, --reverse` flips the order; the default sort is alphabetical.
- `-m, --max` caps results (default 256) and `--offset` pages through them.
- `-q, --short` prints names only; `--no-headers` drops the header row.
- `-o` accepts table, json or yaml.
- `--time-format` formats times with a Go layout.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_list/ (status filters, -m default 256, selector limits, sort, time-format). Removed: the `--max 0` behaviour claim and the exit-code claim (not on the page).
Method: documentation only; no commands were run.

