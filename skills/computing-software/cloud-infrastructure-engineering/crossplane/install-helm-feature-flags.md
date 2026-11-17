---
id: computing-software.cloud-infrastructure-engineering.crossplane.install-helm-feature-flags
name: install-helm-feature-flags
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [install, helm, feature-flags, args, namespace]
level: intro
status: docs-checked
description: "Install Crossplane with Helm and enable alpha or beta features through the args value."
sources:
  - https://docs.crossplane.io/latest/get-started/install/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: a supported Kubernetes version and Helm v3.2.0 or later.

```shell
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update
helm install crossplane \
--namespace crossplane-system \
--create-namespace crossplane-stable/crossplane
```

Check with `kubectl get pods -n crossplane-system`: expect `crossplane` and `crossplane-rbac-manager`. Add `--dry-run --debug` to preview changes.

Alpha features are off by default and beta features are on. Set flags via the chart's `args` value:

```shell
--set args='{"--enable-operations","--enable-signature-verification"}'
```

Flags:

- Beta: `--enable-custom-to-managed-resource-conversion`, `--enable-deployment-runtime-configs`, `--enable-realtime-compositions`, `--enable-ssa-claims`, `--enable-usages`.
- Alpha: `--enable-dependency-version-downgrades`, `--enable-dependency-version-upgrades`, `--enable-function-response-cache`, `--enable-operations`, `--enable-pipeline-inspector`, `--enable-provider-deletion-protection` (requires `--enable-usages`), `--enable-signature-verification`.

List them with `crossplane core start --help`. Set them in `values.yaml` or with `--set`.

Pre-releases come from the `master` channel: add `https://charts.crossplane.io/master/` as `crossplane-master` and install with `--devel`. Use it only for testing and development, never production.

## Checked

Prerequisites, repo and install commands, expected pods, dry-run tip, default alpha and beta status, the full flag table and the master channel steps confirmed on the Install Crossplane page. Unsourced advice on upgrades, verifying args and pod restarts was removed.

Method: docs-checked 2026-11-09 against the raw Install Crossplane page (docs repo, current content folder), read in full.
