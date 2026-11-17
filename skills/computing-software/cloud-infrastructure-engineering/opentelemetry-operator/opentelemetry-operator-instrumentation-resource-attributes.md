---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-resource-attributes
name: opentelemetry-operator-instrumentation-resource-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, resource-attributes, uselabelsforresourceattributes, service-name, attribute-priority, resource-annotations]
level: advanced
status: docs-checked
description: "Set service.name and other resource attributes from annotations, labels and pod metadata, and apply the documented first-found-wins priority order."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/resource-attributes.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/instrumentations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Resource attributes and their priority

The operator can set resource attributes following the Kubernetes semantic conventions.

Annotations. Any annotation with the prefix `resource.opentelemetry.io/` becomes an attribute, for example `resource.opentelemetry.io/service.name: "my-service"` or `.../deployment.environment.name: "production"`.

Labels. With explicit opt-in `spec.defaults.useLabelsForResourceAttributes: true` on the Instrumentation, these labels are used (first entry wins): `app.kubernetes.io/instance` and `app.kubernetes.io/name` become `service.name`, and `app.kubernetes.io/version` becomes `service.version`.

Priority, per attribute, first found wins:
1. `OTEL_RESOURCE_ATTRIBUTES` and `OTEL_SERVICE_NAME` environment variables.
2. `resource.opentelemetry.io/` annotations.
3. Labels, when `useLabelsForResourceAttributes` is true.
4. Attributes calculated from pod metadata (for example `k8s.pod.name`).
5. Attributes in the Instrumentation `spec.resource.resourceAttributes`.

Because it is applied per attribute, some can come from annotations and others from labels.

Related Instrumentation fields: `spec.resource.addK8sUIDAttributes` (collect UIDs such as `k8s.deployment.uid`) and `spec.resource.resourceAttributes` (a map such as `environment: dev`).

To debug a wrong service name, check whether `OTEL_RESOURCE_ATTRIBUTES` or `OTEL_SERVICE_NAME` is set, since the page gives those environment variables the highest priority.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/resource-attributes.md: the `resource.opentelemetry.io/` annotation prefix and examples, the label list with first entry wins, the opt-in `defaults.useLabelsForResourceAttributes`, the five-step priority applied per attribute, and the mixed annotation and label note. Confirmed against the Instrumentation API reference (docs/api/instrumentations.md, read as raw Markdown because the GitHub page view is a stub): `spec.defaults.useLabelsForResourceAttributes` (default false), `spec.resource.addK8sUIDAttributes` (for example `k8s.deployment.uid`) and `spec.resource.resourceAttributes` (map, for example `environment: dev`). Reworded the debugging advice, which went beyond the page.

Method: documentation only; no commands were run.
