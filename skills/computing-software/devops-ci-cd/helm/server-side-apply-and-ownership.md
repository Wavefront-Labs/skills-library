---
id: computing-software.devops-ci-cd.helm.server-side-apply-and-ownership
name: server-side-apply-and-ownership
category: computing-software
field: devops-ci-cd
product: helm
tags: [server-side-apply, force-conflicts, force-replace, take-ownership, field-manager, conflicts]
level: advanced
status: docs-checked
description: "Helm 4 apply modes: --server-side, --force-conflicts, --force-replace and --take-ownership."
sources:
  - https://helm.sh/docs/helm/helm_install/
  - https://helm.sh/docs/helm/helm_upgrade/
  - https://helm.sh/docs/topics/advanced/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Helm 4 reference pages for `helm install` and `helm upgrade` list four flags that control how objects are applied. The Helm 3 pages list none of the first three (Helm 3 has `--force` for replacement and `--take-ownership`).

- `--server-side`: object updates run on the server instead of the client. On `helm install` it is a boolean flag with default `true`. On `helm upgrade` it takes `true`, `false` or `auto`, and `auto` (the default) takes the value from the previous release's method.
- `--force-conflicts`: with server-side apply, force changes against conflicts.
- `--force-replace`: force resource updates by replacement.
- `--take-ownership`: install or upgrade ignores the check for Helm annotations and takes ownership of the existing resources.

Choosing between them (the flag descriptions are the only documentation on these pages, so the mapping is an interpretation):

- Another field manager conflicts with Helm on a field: decide which tool should own the field; `--force-conflicts` makes Helm's values win under server-side apply.
- An update cannot be applied in place: `--force-replace` replaces the resource instead.
- A resource already exists in the cluster and was not created by this release: by default Helm refuses with "resource already exists and is not owned by this release". It tracks ownership with Helm-managed annotations and labels such as `app.kubernetes.io/managed-by`. `--take-ownership` skips that check and adopts the existing objects into the release, so use it only when you intend to.

Taking ownership does not delete extra fields that were never in the chart; the three-way strategic merge (or server-side apply) still controls how live and chart values combine. Match names carefully and review the dry-run output first. Documented use cases: migrating manually applied manifests to a chart without deleting live resources, and recovering after annotations were removed or release history was lost. `helm template` also accepts `--take-ownership` for flag parity without contacting the cluster.

Run with `--dry-run=server` first. It simulates the operation on the server and requires cluster connectivity, while `--dry-run=client` avoids cluster connections. `--hide-secret` stops Secrets appearing in dry-run output.

## Checked

2026-11-08. Checked against the Helm 4 install and upgrade pages: --server-side (install default true; upgrade true|false|auto, default auto), --force-conflicts, --force-replace, --take-ownership, --rollback-on-failure and --wait strategies. Removed unsourced claims.

Method: documentation only; no commands were run.
