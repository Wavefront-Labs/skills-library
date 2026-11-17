---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-sidecar-annotation-precedence
name: opentelemetry-operator-sidecar-annotation-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, annotation-precedence, namespace-annotation, pod-annotation, sidecar-opt-out, cross-namespace-sidecar]
level: practitioner
status: docs-checked
description: "Resolve which sidecar annotation wins when both namespace and pod set sidecar.opentelemetry.io/inject, including opt-out with false and cross-namespace references."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/collector/sidecar-injection.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sidecar annotation precedence

The `sidecar.opentelemetry.io/inject` annotation can be set on a namespace or on a pod, and the most specific annotation wins. The documented resolution order:

1. The pod annotation is used when it is set to a concrete instance name or to `"false"`.
2. The namespace annotation is used when the pod annotation is absent or set to `"true"`, and the namespace annotation is a concrete instance name or `"false"`.

Reading this as a table:
- Pod `"false"`: never injected, whatever the namespace says. This is the opt-out for a single workload.
- Pod `"my-collector"`: that Collector, regardless of the namespace value.
- Pod absent or `"true"` with namespace `"my-collector"`: the namespace's named Collector is used.
- Pod absent or `"true"` with namespace `"false"`: no injection.
- Pod `"true"` and no namespace annotation: the single sidecar-mode Collector in the pod's namespace.

Values may reference a Collector in another namespace with `namespace/name`.

Failure mode to check first: if more than one sidecar-mode Collector exists in the namespace and the annotation is just `"true"`, the page says to use a concrete name. Remember the annotation belongs on the pod template of workload controllers.

## Checked

2026-11-04. Confirmed against docs/collector/sidecar-injection.md: pod or namespace annotation, the two-step most-specific-wins order, the four value forms (`true`, a name, `namespace/name`, `false`), concrete names needed with several sidecar-mode Collectors in a namespace, the single-instance case for `true`, and the annotation placement on the PodTemplate. Removed the inferred platform-team and central-definition remarks and softened the failure-mode wording.

Method: documentation only; no commands were run.
