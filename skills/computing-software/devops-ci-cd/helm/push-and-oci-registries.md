---
id: computing-software.devops-ci-cd.helm.push-and-oci-registries
name: push-and-oci-registries
category: computing-software
field: devops-ci-cd
product: helm
tags: [push, oci, registry, login, digest, chart-registry, helm-push]
level: practitioner
status: docs-checked
description: "Store charts in OCI registries: helm registry login, helm push reference rules, oci:// support in other commands and digests."
sources:
  - "https://helm.sh/docs/topics/registries/"
  - "https://helm.sh/docs/helm/helm_push/"
  - "https://helm.sh/docs/helm/helm_registry_login/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The docs recommend OCI-capable container registries for storing and sharing charts.

Login: `helm registry login [host]` with `-u/--username` and `-p/--password`. The host must be only a hostname with optional port; a scheme (`https://ghcr.io`) or a path (`ghcr.io/myrepo`) is rejected. The reference example pipes a token: `echo "$GITHUB_TOKEN" | helm registry login ghcr.io -u $GITHUB_USER --password-stdin`. `helm registry logout HOST` removes credentials.

Push: `helm push mychart-0.1.0.tgz oci://localhost:5000/helm-charts`.

- It works only on `.tgz` files made by `helm package`.
- The reference must start with `oci://` and must not contain the chart name or tag; the name comes from the chart and the tag from its semantic version.
- Some registries need the namespace or repository to exist first.
- A `.prov` file next to the archive is uploaded automatically as an extra layer.

Other commands accepting `oci://`: `pull`, `show`, `template`, `install` and `upgrade`. For these, include the chart name and use `--version`.

Install by digest: `helm install rel oci://host/charts/app@sha256:<digest>`.

For dependencies, set `repository: "oci://host/myrepo"` (no chart name) in `Chart.yaml`.

The old ChartMuseum helm-push plugin was renamed `cm-push` at v0.10.0 to avoid clashing.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/topics/registries/ (host rules, push restrictions, .prov upload, oci:// dependencies, digest install, cm-push rename) and https://helm.sh/docs/helm/helm_push/. Removed: the "for immutability" rationale.
Method: documentation only; no commands were run.

