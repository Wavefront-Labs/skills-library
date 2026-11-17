---
id: computing-software.cloud-infrastructure-engineering.kyverno.upgrading-kyverno
name: upgrading-kyverno
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [upgrade, deprecations, crds, kyverno-migrate, breaking-changes, policyexception]
level: practitioner
status: docs-checked
description: "Upgrade Kyverno safely: never bump image tags, read each release's notes, and handle the v1.19 deprecations and v1.13 breaking changes."
sources:
  - https://kyverno.io/docs/installation/upgrading/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rules:
- Do not upgrade by changing image tags; new versions often change supporting resources including CRDs.
- Read the release notes of the target version, and of every minor version you skip.
- Helm upgrades from pre-1.10 to 1.10+ need manual steps (v2 to v3 chart migration guide).
- YAML installs have no direct upgrade path: uninstall with the manifest of the installed release, then reinstall.

v1.19 deprecations (removal in v1.20): `ClusterPolicy` and `Policy` (`kyverno.io/v1`) move to CEL policy types; `CleanupPolicy`/`ClusterCleanupPolicy` (`kyverno.io/v2`) to DeletingPolicy; the legacy `PolicyException` (`kyverno.io/v2`) to the `policies.kyverno.io` one; `v1alpha1` of `policies.kyverno.io` to `v1`. PolicyReport and EphemeralReport kinds are not deprecated; only `kyverno.io/v2alpha1` GlobalContextEntry is.

Storage: `policies.kyverno.io` stays `v1beta1` in v1.19 and moves to `v1` in v1.20; rewrite stored objects with `kyverno migrate --resource policyexceptions.kyverno.io`.

Helm: CRDs now come from the `kyverno-api` chart dependency, controlled by `crds.install`; review your workflow if you install CRDs separately.

CLI: `kyverno json scan` is removed; use ValidatingPolicy with `kyverno apply`, or kyverno-json.

v1.13 breaking changes: wildcard view permissions were replaced by a binding to the default `view` role (may affect reports and mutate/generate on custom resources); exceptions became enabled in all namespaces (CVE-2024-48921), so keep the old behaviour only with `--set features.policyExceptions.namespace="*"`, though limiting namespaces is recommended; without Helm hooks use kube-storage-version-migrator for dropped API versions.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
