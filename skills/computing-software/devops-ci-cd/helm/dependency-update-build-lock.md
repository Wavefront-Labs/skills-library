---
id: computing-software.devops-ci-cd.helm.dependency-update-build-lock
name: dependency-update-build-lock
category: computing-software
field: devops-ci-cd
product: helm
tags: [dependency-update, dependency-build, chart-lock, dependency-list, skip-refresh, reproducible]
level: practitioner
status: docs-checked
description: "Differences between helm dependency update, build and list, and how Chart.lock gives reproducible dependency trees."
sources:
  - https://helm.sh/docs/helm/helm_dependency_update/
  - https://helm.sh/docs/helm/helm_dependency_build/
  - https://helm.sh/docs/helm/helm_dependency_list/
  - https://helm.sh/docs/helm/helm_install/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Three subcommands manage a chart's dependencies; each takes a CHART argument.

`helm dependency update CHART` updates the on-disk dependencies to mirror `Chart.yaml`. It verifies the required charts are present in `charts/` and at an acceptable version, pulls down the latest charts that satisfy the dependencies, and cleans up old dependencies. On success it generates a lock file that can later rebuild the dependencies to exact versions. Dependencies need not be listed in `Chart.yaml`, so update removes a chart only if it is in `Chart.yaml` but at the wrong version.

`helm dependency build CHART` rebuilds `charts/` from the `Chart.lock` file, to the state the lock records. It does not re-negotiate dependencies the way update does. If no lock file is found, it mirrors the behaviour of update.

`helm dependency list CHART` lists the dependencies declared in a chart directory or archive. It never alters the chart and errors if the chart cannot be loaded. `--max-col-width` (default 80) sets the table width.

Flags on update and build (identical lists): `--skip-refresh` does not refresh the local repository cache, `--verify` verifies packages against signatures, `--keyring` names the keyring of public keys (default `~/.gnupg/pubring.gpg`), plus `--username`, `--password`, `--ca-file`, `--cert-file`, `--key-file`, `--insecure-skip-tls-verify` and `--plain-http` for the download.

Practical pattern (inference from the above): commit `Chart.lock`, run `helm dependency build` for repeatable builds, and run `helm dependency update` deliberately when you want to bump versions.

`helm install` also offers `--dependency-update`, which updates dependencies if they are missing before installing the chart.

## Checked

2026-11-08. Checked against the Helm 4 dependency update, build and list pages and the install page (--dependency-update). Removed unsourced claims and aliases.

Method: documentation only; no commands were run.
