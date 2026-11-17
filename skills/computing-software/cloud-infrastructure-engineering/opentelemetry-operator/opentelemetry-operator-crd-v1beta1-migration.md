---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-crd-v1beta1-migration
name: opentelemetry-operator-crd-v1beta1-migration
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, v1beta1, crd-migration, storedversions, olm-allnamespaces, conversion-webhook]
level: advanced
status: docs-checked
description: "Migrate stored OpenTelemetryCollector resources from v1alpha1 to v1beta1, including patching storedVersions and the OLM AllNamespaces install-mode restriction."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/crd-changelog.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/rfcs/crd-version-graduation-strategies.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrate OpenTelemetryCollector to v1beta1

No immediate user action is required for v1beta1: the operator keeps supporting existing `v1alpha1` resources, and any newly applied `v1alpha1` resource is converted and stored as `v1beta1`. Support for `v1alpha1` is planned to be removed in a future version, so migrate promptly. Full migration:

1. Update manifests kept outside the cluster, for example in an infrastructure git repository.
2. Apply them so every object is stored as `v1beta1`.
3. Tell the CRD to store only `v1beta1`:

```bash
kubectl patch customresourcedefinitions opentelemetrycollectors.opentelemetry.io   --subresource='status' --type='merge'   -p '{"status":{"storedVersions":["v1beta1"]}}'
```

The changelog refers to the Kubernetes documentation for why this works; the graduation RFC names it as the Kubernetes page on upgrading existing objects to a new stored version.

Operator Lifecycle Manager on OpenShift: only the `AllNamespaces` install mode is supported now, because of the conversion webhook between `v1beta1` and `v1alpha1`. The graduation RFC adds that conversion webhooks are cluster-scoped, which is incompatible with `OwnNamespace` mode.

Also note the collector image decision recorded here: the project intends eventually to use the Collector distribution aimed at Kubernetes workloads as the default image instead of the core distribution, but decided not to do it in v1beta1 and to roll it out gradually with more warning.

## Checked

2026-11-04. Confirmed against docs/reference/crd-changelog.md: no immediate action, v1alpha1 resources still supported and converted to v1beta1 when applied, planned removal of v1alpha1, the three migration steps, the `storedVersions` patch command, and the OLM AllNamespaces-only note. Confirmed against docs/rfcs/crd-version-graduation-strategies.md: cluster-scoped conversion webhooks versus OwnNamespace. Removed the name `otelcol-k8s`, which the changelog page text does not state, and reworded the Kubernetes documentation pointer.

Method: documentation only; no commands were run.
