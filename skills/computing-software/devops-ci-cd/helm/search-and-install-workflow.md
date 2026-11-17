---
id: computing-software.devops-ci-cd.helm.search-and-install-workflow
name: search-and-install-workflow
category: computing-software
field: devops-ci-cd
product: helm
tags: [workflow, install, upgrade-install, release-name, generate-name, create-namespace, rollback-on-failure, values-files]
level: intro
status: docs-checked
description: "Everyday Helm workflow: search, upgrade --install, namespaces, generate-name, values files and checking before applying."
sources:
  - https://helm.sh/docs/helm/helm_install/
  - https://helm.sh/docs/helm/helm_upgrade/
  - https://helm.sh/docs/intro/using_helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Find a chart first: `helm search hub NAME` searches Artifact Hub (add `--list-repo-url` to see the real repo URL), and `helm search repo NAME` fuzzy-matches repositories you added with `helm repo add NAME URL`; Helm 3 and later ship with no default repository, and `helm repo update` refreshes the local indexes. `helm show values CHART` lists what you can override.

A repeatable deployment pattern (flags below are from the Helm 4 reference pages; `--rollback-on-failure` and `--wait=watcher` do not exist in Helm 3, which uses `--atomic`):

```bash
helm upgrade --install myapp ./chart \
  --namespace web --create-namespace \
  -f values.yaml -f values-prod.yaml \
  --set image.tag=1.4.2 \
  --wait --timeout 5m --rollback-on-failure
```

Why each part:

- `upgrade --install` (`-i`) installs when the release does not exist and upgrades otherwise, so CI needs one command.
- `--create-namespace` creates the release namespace if absent; `-n` selects it.
- Later `-f` files override earlier ones, and `--set` overrides the files.
- `--wait` alone selects the `watcher` strategy (others: `hookOnly`, `legacy`; default when omitted is `hookOnly`) and waits up to `--timeout`. `--rollback-on-failure` rolls an upgrade back (or uninstalls a failed install) and defaults `--wait` to `watcher`.
- `--generate-name` (`-g`) omits the NAME argument and makes one; `--name-template` specifies a template for the name.
- A chart can come from a repo reference (`example/mariadb`), a packaged `.tgz`, an unpacked directory, an absolute URL, `--repo URL` plus a chart name, or an `oci://` reference; `--version` takes a constraint such as `^2.0.0`, and `--devel` includes prereleases.
- On upgrade, `--reuse-values` merges the last release's values with new overrides, `--reset-values` returns to the chart's built-in values, and `--reset-then-reuse-values` resets to the new chart's values, applies the last release's values, then your overrides.

Pre-flight: `helm lint` and a dry run (`--dry-run=client` avoids the cluster, `--dry-run=server` contacts it; add `--hide-secret` so Secrets are not printed). `--debug` gives verbose output.

After: `helm status RELEASE`, `helm get values RELEASE`, `helm history RELEASE`, and `helm rollback RELEASE REVISION`; each install, upgrade or rollback increments the revision (the first is 1). `helm upgrade --history-max` limits retained revisions (default 10).

Without `--wait` the guide says Helm does not wait until all resources are running before it exits.

## Checked

2026-11-08. Checked against the Helm 4 search, repo and install command pages. Removed unsourced flags and claims.

Method: documentation only; no commands were run.
