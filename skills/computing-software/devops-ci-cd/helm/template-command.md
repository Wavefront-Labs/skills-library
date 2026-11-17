---
id: computing-software.devops-ci-cd.helm.template-command
name: template-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [template, render, api-versions, show-only, kube-version, output-dir, include-crds]
level: practitioner
status: docs-checked
description: "Render charts locally with helm template: faked cluster lookups, Capabilities flags, show-only and output-dir."
sources:
  - "https://helm.sh/docs/helm/helm_template/"
  - "https://helm.sh/docs/chart_template_guide/debugging/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm template [NAME] [CHART]` renders chart templates locally and prints the output. Values that would normally be looked up in-cluster are faked, and none of the server-side validity testing (such as whether an API exists) is done.

```bash
helm template myrel ./chart -f values.yaml --api-versions networking.k8s.io/v1 --kube-version 1.30.0
```

Flags worth knowing:

- `-a, --api-versions` supplies `Capabilities.APIVersions` (repeat or comma-separate).
- `--kube-version` sets `Capabilities.KubeVersion`.
- `-s, --show-only templates/deploy.yaml` renders only the named templates.
- `--output-dir` writes rendered files to a directory; `--release-name` includes the release name in that path.
- `--include-crds` adds CRDs to the output; `--skip-tests` omits test hooks.
- `--is-upgrade` sets `.Release.IsUpgrade` instead of `.Release.IsInstall`.
- `--no-hooks`, `--create-namespace`, `--dependency-update`, `--post-renderer`.
- `--dry-run` accepts `client` (default, no cluster connection) or `server` (simulates and validates on the server, so it needs cluster connectivity).

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_template/ (synopsis on faked values and skipped server-side validity testing, flags, --dry-run values and default). Removed: the `lookup` always-empty claim and the closing CI and `kubectl diff` advice.
Method: documentation only; no commands were run.

