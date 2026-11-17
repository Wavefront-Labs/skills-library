---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-resource-attribute-derivation
name: opentelemetry-operator-resource-attribute-derivation
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, service-instance-id, service-version, service-namespace, derivation-order, image-tag]
level: advanced
status: docs-checked
description: "Know the exact fallback chains the operator uses to compute service.name, service.version, service.instance.id and service.namespace from pod metadata."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/resource-attributes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# How service.name and friends are derived

When nothing overrides them, the operator computes these attributes from pod metadata, choosing the first value found.

service.name:
1. annotation `resource.opentelemetry.io/service.name`
2. label `app.kubernetes.io/name`, only if `useLabelsForResourceAttributes` is enabled (the same page's label section also lists `app.kubernetes.io/instance` ahead of `name`, but this calculation list names only `name`)
3. `k8s.deployment.name`
4. `k8s.replicaset.name`
5. `k8s.statefulset.name`
6. `k8s.daemonset.name`
7. `k8s.cronjob.name`
8. `k8s.job.name`
9. `k8s.pod.name`
10. `k8s.container.name`

service.version:
1. annotation `resource.opentelemetry.io/service.version`
2. label `app.kubernetes.io/version`, if labels are enabled
3. the container image tag, but only when the tag contains no `/`

service.instance.id:
1. annotation `resource.opentelemetry.io/service.instance.id`
2. otherwise the dot-joined string of `k8s.namespace.name`, `k8s.pod.name` and `k8s.container.name`

service.namespace:
1. annotation `resource.opentelemetry.io/service.namespace`
2. otherwise `k8s.namespace.name`

Practical use: with no annotation, label or environment variable, the chain above picks the first workload name found, so a pod owned by a Deployment named `checkout` is expected to get `service.name=checkout`. The annotation (or `OTEL_SERVICE_NAME`, which the priority list ranks highest) picks a different name.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/resource-attributes.md: the four fallback chains for service.name (ten steps), service.version (annotation, label, image tag without a slash), service.instance.id (annotation, then namespace, pod and container names joined with a dot) and service.namespace (annotation, then namespace name), and the priority list that ranks environment variables first. Noted that the labels section lists `app.kubernetes.io/instance` as well as `name` for service.name while the calculation list names only `name`. Removed the unconfirmed claims that the instance id is unique per container and that a Deployment-owned pod resolves to the Deployment name beyond what the chain implies.

Method: documentation only; no commands were run.
