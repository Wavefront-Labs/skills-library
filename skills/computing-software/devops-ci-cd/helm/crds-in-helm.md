---
id: computing-software.devops-ci-cd.helm.crds-in-helm
name: crds-in-helm
category: computing-software
field: devops-ci-cd
product: helm
tags: [crds, custom-resource-definitions, crds-dir, upgrade, install, cr]
level: advanced
status: docs-checked
description: "How Helm treats CRDs in crds/: installed first, never templated, never upgraded or deleted, and the documented workarounds."
sources:
  - https://helm.sh/docs/topics/charts/
  - https://helm.sh/docs/chart_best_practices/custom_resource_definitions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

CRD YAML files go in the chart's `crds/` directory. They cannot be templated and must be plain YAML documents. Several CRDs may be in one file (separated by YAML document markers), and Helm attempts to load all files in the directory.

Install behaviour:

- Helm uploads the CRDs, pauses until the API server makes them available, then starts the template engine and renders the rest of the chart. Because of that order, CRD information is available in the `.Capabilities` object and templates can create instances of the new kinds (the docs example puts a `CronTab` CRD in `crds/` and a `CronTab` resource in `templates/`).
- CRDs are installed by default on `helm install`. If a CRD already exists it is skipped with a warning. `--skip-crds` skips the step.- `--dry-run` on `helm install` and `helm upgrade` is not supported for CRDs: Helm cannot install the CRD in a dry run, so the discovery client does not know the custom resource and validation fails. The best-practices guide suggests moving CRDs to their own chart as an alternative.

Limitations (explicit in the chart guide):

- CRDs are never reinstalled: if the CRDs in `crds/` are already present, regardless of version, Helm does not install or upgrade them.
- CRDs are never installed on upgrade or rollback; Helm creates them only on installation.
- CRDs are never deleted, because deleting a CRD deletes all of its custom resources across all namespaces.

Operators who want to upgrade or delete CRDs are told to do it manually and with great care. The best-practices guide says this was a deliberate decision after community discussion because of the risk of unintentional data loss, and that there is no consensus on CRD lifecycle management yet. Templating was removed from CRDs so that Helm always has valid information about the cluster's available APIs; the older Helm 2 `crd-install` hooks are gone.

Two documented methods:

1. Method 1: the `crds/` directory (above).
2. Method 2: put the CRD declaration in one chart and the resources that use it in another chart. Each chart is installed separately, which can suit cluster operators who have admin access to the cluster.

Distinguish the declaration (kind `CustomResourceDefinition`) from resources that use it; the declaration must be registered, which can take a few seconds, before those resources can be created.

## Checked

2026-11-08. Checked against the Helm charts topic page (crds/ directory) and the custom resource definitions best-practices page, read in full. Removed unsourced claims.

Method: documentation only; no commands were run.
