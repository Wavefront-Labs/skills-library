---
id: computing-software.devops-ci-cd.helm.install-command
name: install-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [install, release, chart, generate-name, create-namespace]
level: intro
status: docs-checked
description: "Install a chart with helm install: release naming, chart references, namespace creation and the flags that change install behaviour."
sources:
  - "https://helm.sh/docs/helm/helm_install/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm install [NAME] [CHART]` creates a release. The chart argument can be a chart reference (`repo/chart`), a packaged `.tgz`, an unpacked chart directory, a URL or an `oci://` reference.

```bash
helm install myredis ./redis
helm install --generate-name ./redis
helm install myapp repo/app --version 1.2.3 -n prod --create-namespace
```

Useful flags from the install reference:

- `-g, --generate-name` omits the NAME argument; `--name-template` sets a template for the name.
- `--create-namespace` creates the release namespace if missing.
- `--dependency-update` fetches missing dependencies before installing.
- `--version` takes an exact version or a constraint such as `^2.0.0`; `--devel` is equivalent to version `>0.0.0-0`.
- `--description` stores a custom description on the release.
- `--hide-notes` suppresses NOTES output; `--render-subchart-notes` renders subchart notes with the parent.
- `--skip-crds` skips the `crds/` directory; `--no-hooks` skips hooks.
- `--replace` reuses a name that is a deleted release still in history; the docs call it unsafe in production.
- `--take-ownership` ignores the Helm ownership annotation check on existing resources.
- `-l, --labels` adds labels to release metadata.
- `--timeout` defaults to 5m0s.

Values come from `-f/--values` (repeatable, the rightmost file wins) and `--set` flags; `--set` values are merged into `--values` with higher precedence.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_install/ (flags, defaults, --devel, --replace, --take-ownership, values priority) and https://helm.sh/docs/intro/using_helm/ (--set precedence). Removed: the `--dry-run` testing advice.
Method: documentation only; no commands were run.

