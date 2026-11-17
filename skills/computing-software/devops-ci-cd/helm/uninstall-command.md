---
id: computing-software.devops-ci-cd.helm.uninstall-command
name: uninstall-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [uninstall, keep-history, cascade, ignore-not-found, release, delete]
level: practitioner
status: docs-checked
description: "Remove a release with helm uninstall, keeping history, choosing cascade mode, and what happens to hook-created resources."
sources:
  - "https://helm.sh/docs/helm/helm_uninstall/"
  - "https://helm.sh/docs/topics/charts/"
  - "https://helm.sh/docs/howto/charts_tips_and_tricks/"
  - "https://helm.sh/docs/intro/using_helm/"
  - "https://helm.sh/docs/topics/charts_hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm uninstall RELEASE_NAME [...]` removes all resources associated with the last release; `--keep-history` retains the release history.

Flags from the reference:

- `--keep-history` removes the resources and marks the release deleted but keeps its history. Such releases show in `helm list --uninstalled`.
- `--dry-run` shows what would be uninstalled.
- `--cascade` is `background` (default), `orphan` or `foreground`. Use `--cascade foreground` together with `--wait` so resources with finalizers are fully deleted before the command returns.
- `--ignore-not-found` treats a missing release as a successful uninstall, handy in idempotent scripts.
- `--no-hooks` prevents hooks from running.
- `--wait`, `--timeout` (default 5m0s).
- `--description` adds a custom description.

Things not removed automatically:

- Resources annotated `helm.sh/resource-policy: keep` are skipped on delete and become orphaned.
- CRDs are never deleted by Helm.

The `uninstalling` status is listed by `helm list --uninstalling`.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_uninstall/ (flags, --cascade, --ignore-not-found, --keep-history), helm list (--uninstalling), topics/charts (CRDs never deleted) and charts_tips_and_tricks (resource-policy keep). Removed: the hook-created resources and hook-delete-policy claim, the name-reuse claim, and the pre/post-delete hook wording.
Method: documentation only; no commands were run.

