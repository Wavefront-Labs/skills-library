---
id: computing-software.devops-ci-cd.helm.upgrade-command
name: upgrade-command
category: computing-software
field: devops-ci-cd
product: helm
tags: [upgrade, install-flag, reuse-values, reset-values, history-max, cleanup-on-fail]
level: practitioner
status: docs-checked
description: "Upgrade a release with helm upgrade, including upgrade --install, value reuse and reset behaviour, and failure handling flags."
sources:
  - "https://helm.sh/docs/helm/helm_upgrade/"
  - "https://helm.sh/docs/intro/using_helm/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm upgrade RELEASE CHART` applies a new chart version or new values to an existing release and creates a new revision.

```bash
helm upgrade --install myapp ./chart -f prod.yaml --wait --timeout 10m
```

Key flags from the upgrade reference:

- `-i, --install` runs an install when the release does not exist.
- `--create-namespace` works together with `--install`.
- `--reuse-values` reuses the last release's values and merges command line overrides.
- `--reset-values` resets to the values built into the chart.
- `--reset-then-reuse-values` resets to chart values, applies the last release's values, then merges overrides.
- `--history-max` limits stored revisions per release; the default is 10 and 0 means no limit.
- `--cleanup-on-fail` allows deletion of new resources created in this upgrade when it fails.
- `--rollback-on-failure` rolls back to the previous successful release when the upgrade fails; `--wait` defaults to the watcher strategy when it is set.
- `--no-hooks` prevents hooks from running during the upgrade.
- `--take-ownership`, `--force-replace` and `--force-conflicts` control how existing objects are adopted or replaced.
- `--timeout` defaults to 5m0s; `--skip-crds` applies only with `--install`.

Helm never installs CRDs on upgrade; it creates them only on install operations (charts topic page).

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_upgrade/ (flags, defaults, values handling) and https://helm.sh/docs/topics/charts/ (CRDs never installed on upgrade). Removed: the CI idempotence remark and the `--no-hooks` pre/post hook wording.
Method: documentation only; no commands were run.

