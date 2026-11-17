---
id: computing-software.cloud-infrastructure-engineering.kubernetes.operator-lifecycle-manager-packaging
name: operator-lifecycle-manager-packaging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, olm, operator-lifecycle-manager, clusterserviceversion, csv, operator-bundle, operator-sdk, bundle-validate, operatorhub, catalogsource, subscription, install-plan, channel, upgrade-graph, openshift, operatorframework]
level: advanced
status: docs-checked
description: "Package an operator for OLM: ClusterServiceVersion authoring, bundle format and validation, channels/catalogs, and upgrade-graph edges that don't strand users."
sources: ["https://olm.operatorframework.io/docs/concepts/crds/clusterserviceversion/", "https://olm.operatorframework.io/docs/concepts/olm-architecture/operator-catalog/creating-an-update-graph/", "https://olm.operatorframework.io/docs/reference/file-based-catalogs/", "https://sdk.operatorframework.io/docs/cli/operator-sdk_generate_bundle/", "https://sdk.operatorframework.io/docs/cli/operator-sdk_bundle_validate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator Lifecycle Manager packaging — shipping an operator as an installable, upgradable product

**Goal:** go from "an operator I can `kubectl apply` manifests for" to "an operator
a cluster admin installs from a catalog, with declared upgrade paths and no manual
RBAC/CRD bootstrapping." OLM also runs standalone on vanilla Kubernetes; skip this entirely for operators you
only ever install via your own Helm chart/Kustomize — see
`computing-software.cloud-infrastructure-engineering.kubernetes.operator-framework-selection`
for when OLM packaging is worth the overhead.

## 1. The core object: ClusterServiceVersion (CSV)
The CSV is the operator's manifest-of-manifests: it declares the CRDs owned, the
Deployment(s) to run, the RBAC OLM should create, install modes (can it run
`AllNamespaces`/`SingleNamespace`/`OwnNamespace`/`MultiNamespace`), and
human-facing metadata (description, icon, maintainers) shown in OperatorHub-style
UIs. `operator-sdk generate kustomize manifests` generates the kustomize bases in `config/manifests`
that `generate bundle` builds the CSV from; it asks interactively for UI metadata (display name and similar)
unless a base already exists or you pass `--interactive=false`. Those human-facing fields need deliberate
authoring, they're what a user actually reads before installing.
```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: ClusterServiceVersion
spec:
  install:
    strategy: deployment
    spec:
      deployments: [{name: widget-operator, spec: {...}}]  # from config/manager
      permissions: [...]        # namespaced RBAC
      clusterPermissions: [...] # cluster-scoped RBAC
  installModes:
  - {type: AllNamespaces, supported: true}
  - {type: SingleNamespace, supported: true}
  customresourcedefinitions:
    owned: [{name: widgets.apps.example.com, version: v1, kind: Widget}]
```

## 2. Bundle format
A **bundle** is the distributable unit: the CSV, the owned CRDs, and any
additional manifests, laid out under `bundle/manifests/` with an
`bundle/metadata/annotations.yaml` declaring the bundle's package name and
supported channels, built into an OCI image.
```bash
operator-sdk generate bundle --package widget-operator --version 0.3.0 \
  --channels stable --default-channel stable
operator-sdk bundle validate ./bundle --select-optional suite=operatorframework
docker build -f bundle.Dockerfile -t quay.io/you/widget-operator-bundle:0.3.0 .
```
`bundle validate` runs the required bundle validators, and
`--select-optional suite=operatorframework` adds the Operator Framework suite
(`--optional-values=k8s-version=<version>` checks against a Kubernetes version) — run it before pushing.

## 3. Channels, catalogs, and the upgrade graph
A **channel** (e.g. `stable`, `fast`, `alpha`) is a named sequence of bundles. In the current
File-Based Catalog (FBC) format, update graphs are defined by `olm.channel` blobs: each entry names a
bundle and its edges with `replaces`, `skips` or `skipRange`:
```yaml
schema: olm.channel
package: widget-operator
name: stable
entries:
- name: widget-operator.v0.3.0
  replaces: widget-operator.v0.2.0
  # skipRange: ">=0.1.0 <0.3.0"   # a direct (one hop) update from any version in range
```
Updates step through each version in a `replaces` chain (a Subscription on v1.0.0 reaches v1.0.2
through v1.0.1). `skipRange` needs semver `version` fields in the CSVs, and the skipped versions are
pruned from OLM's update graph, so they can no longer be installed with `spec.startingCSV`; to keep them
installable, use `skipRange` together with `replaces` pointing at the immediate previous version.
Cross-channel updates are not automated; the Subscription must change channel. A **CatalogSource**
exposes catalog packages and channels to the cluster (the SQLite index format is deprecated in favour of
FBC); a **Subscription** pins an install to a package and channel, and `installPlanApproval: Manual`
makes OLM wait for you to approve each **InstallPlan** (`spec.approved: true`) instead of upgrading automatically.

## 4. CRD compatibility across the upgrade graph
Every version bump packaged through OLM should keep the same additive-only CRD discipline as
`computing-software.cloud-infrastructure-engineering.kubernetes.crd-versioning-and-conversion-webhooks`;
OLM packaging adds an upgrade graph on top of it.

## Gotchas
- Only the tail of a channel's `replaces` chain may name a bundle that is not in the catalog
  (`opm validate` checks the channel invariants); validate the whole chain after pruning old bundles.
- The CSV declares `permissions` and `clusterPermissions` for the operator's service account; review
  them before approving an install or upgrade.
- Retire CRD versions only after the full deprecation window, same rule as standalone CRD versioning.
- Testing locally needs OLM installed (`operator-sdk olm install`) and `operator-sdk run bundle <bundle-image>`,
  which deploys the bundle with OLM and can take `--install-mode` and `--index-image`; plain
  `kubectl apply` of the CSV does nothing without OLM's controllers.

## Verify
- [ ] `operator-sdk bundle validate ./bundle --select-optional suite=operatorframework`
      passes with no errors.
- [ ] `operator-sdk run bundle <image>` on a scratch cluster installs cleanly via a
      real Subscription/InstallPlan, not a direct manifest apply.
- [ ] Upgrading from the previous published version through the channel succeeds
      without manual CRD intervention.
- [ ] The CSV's `installModes` match reality — an `AllNamespaces: true` CSV
      actually works when installed that way, not just in `OwnNamespace` testing.

## Checked

Checked on 2026-10-26 against `operator-framework/olm-docs` (CSV, Subscription, update-graph and file-based-catalog pages, pushed 2026-09-15) and the `operator-framework/operator-sdk` CLI reference pages `generate bundle`, `bundle validate`, `generate kustomize manifests`, `olm`, `run bundle`.
Confirmed: CSV `installModes`, `permissions`, `clusterPermissions`, owned CRDs; bundle layout with `annotations.yaml`; `generate bundle` flags `--package`, `--version`, `--channels`, `--default-channel`; `bundle validate --select-optional suite=operatorframework`; `olm.channel` entries with `replaces`, `skips`, `skipRange`; step-by-step updates; skipRange pruning warning; SQLite format deprecated; `installPlanApproval: Manual`; `operator-sdk olm install` and `run bundle`.
Wrong or outdated in the draft: `replaces` and `skipRange` live in FBC channel entries (not as a CSV `spec` skipRange field); `opm index add` belongs to the deprecated SQLite format.
Removed as unconfirmed: the OpenShift-dominance claim, the claim that OLM checks CRD supersets, and the unavailable-chain-strands claim.

Method: documentation only; no commands were run.
