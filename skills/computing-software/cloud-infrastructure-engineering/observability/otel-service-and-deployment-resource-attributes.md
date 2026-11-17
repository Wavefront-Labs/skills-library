---
id: computing-software.cloud-infrastructure-engineering.observability.otel-service-and-deployment-resource-attributes
name: otel-service-and-deployment-resource-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [service-name-attribute, deployment-environment-attribute, semantic-conventions, resource-attributes, service-instance-id]
level: practitioner
status: docs-checked
description: "Set service.name, service.namespace, service.version, service.instance.id and deployment.environment.name correctly, and how backends map them to job, instance and labels."
sources: ["https://opentelemetry.io/docs/specs/semconv/resource/#service", "https://opentelemetry.io/docs/specs/semconv/resource/deployment-environment/", "https://prometheus.io/docs/guides/opentelemetry/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service and deployment resource attributes

## The set every service needs
| Attribute | Example | Notes |
|---|---|---|
| `service.name` | `checkout` | always set it |
| `service.namespace` | `shop` | groups services; part of identity |
| `service.version` | semantic version or git hash | exact artifact version string |
| `service.instance.id` | UUID | unique per instance; regenerate when a resource attribute changes |
| `deployment.environment.name` | `prod`, `staging` | does not affect service uniqueness; the older key was `deployment.environment` |

## Setting
```bash
OTEL_SERVICE_NAME=checkout
OTEL_RESOURCE_ATTRIBUTES=service.namespace=shop,service.version=1.4.2,deployment.environment.name=prod
```
Kubernetes: the OTel Operator maps pod labels such as `app.kubernetes.io/name` (or `app.kubernetes.io/instance`) to `service.name` and `app.kubernetes.io/version` to `service.version`.
Never compute `service.name` per pod (no pod suffix).

## Backend mapping
- **Prometheus OTLP**: per the Prometheus OpenTelemetry guide, all resource attributes except `service.instance.id`, `service.namespace` and `service.name` become labels on `target_info` by default; promote others with `promote_resource_attributes` under the `otlp` config (see the guide). `target_info` needs `service.name` and `service.instance.id`.
- Check how each other backend (Loki, Tempo, vendors) maps these attributes in its own docs.

## Gotchas
- Changing `service.name` breaks dashboards and alert history; treat as an API.
- Mixed old/new `deployment.environment` keys during migration: set both temporarily or transform in the collector (OTTL `set` on `resource.attributes`).

## Checked
- 2026-10-28. Checked against the semantic conventions resource pages (service, deployment environment), the Prometheus OpenTelemetry guide, the OTel Operator automatic-instrumentation page and Collector exporter docs (main, 2026-10).
- Confirmed: `service.namespace`, `service.version` string semantics, `service.instance.id` uniqueness, `deployment.environment.name` uniqueness note, `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES`, operator label mapping, Prometheus `target_info` behaviour and `promote_resource_attributes`.
- Removed (unconfirmed): `unknown_service:<exe>` default, "semconv 1.27" rename version, job/instance mapping formula, Loki, Tempo and Grafana label claims, part-of/pod-UID mapping, service-graph merge claim.
Method: documentation only; no commands were run.
