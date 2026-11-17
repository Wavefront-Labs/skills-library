---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-crd-version-graduation
name: opentelemetry-operator-crd-version-graduation
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, crd-graduation, conversion-strategy, storage-version, served-versions, identical-schemas]
level: sme
status: docs-checked
description: "Compare conversion-webhook and identical-schema strategies for graduating a CRD, using storage and served version semantics and the OpenTelemetry Collector experience."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/rfcs/crd-version-graduation-strategies.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CRD version graduation strategies

This supporting document for the Instrumentation v1beta1 RFC explains Kubernetes CRD versioning.

Basics. Only one version is the storage version persisted in etcd; others convert to and from it. `served: true` lets clients use a version; `served: false` returns 404 for its endpoint. Conversion `strategy: None` only swaps the `apiVersion` field and requires identical schemas; `Webhook` is needed when fields are renamed, restructured or removed (with None, renamed fields appear empty and restructured ones do not map).

Strategy 1, conversion webhook: seamless and non-forced migration, but needs TLS certificates, firewall rules on GKE private clusters (the default allows only 443 and 10250 from the control plane), and conversion code to maintain. Helm is awkward because CRDs hardcode the webhook Service name while Helm prefixes release names, producing errors such as "service opentelemetry-operator-webhook not found". The OpenTelemetryCollector v1alpha1 to v1beta1 conversion hit this and restricted OLM to the `AllNamespaces` install mode.

Strategy 2, identical schemas: make all breaking changes while still alpha, then graduate with identical schemas and `strategy: None`. The controller watches only the storage version with a single Go struct. Prometheus Operator chose this for ScrapeConfig graduation. Cost: breaking changes in alpha and manual `apiVersion` updates.

The doc also reviews cert-manager, which used conversion webhooks across `v1alpha2`, `v1alpha3`, `v1beta1` and `v1`, and offers `cmctl convert` for offline manifest migration.

## Checked

2026-11-04. Confirmed against docs/rfcs/crd-version-graduation-strategies.md: single storage version, `served` true and false behaviour, conversion `None` versus `Webhook` and the field-mapping consequences, Strategy 1 costs (TLS certificates, GKE private cluster firewall of 443 and 10250, conversion code, the Helm webhook Service name error and the OLM AllNamespaces restriction), Strategy 2 (identical schemas, single Go struct, Prometheus Operator ScrapeConfig example, costs), and the cert-manager review with `cmctl convert`. Nothing removed.

Method: documentation only; no commands were run.
