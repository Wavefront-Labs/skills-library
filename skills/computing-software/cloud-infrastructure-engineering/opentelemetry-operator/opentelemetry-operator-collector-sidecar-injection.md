---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-collector-sidecar-injection
name: opentelemetry-operator-collector-sidecar-injection
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, sidecar-injection, inject-annotation, podtemplate, otel-resource-attributes, resourcedetection]
level: practitioner
status: docs-checked
description: "Inject a Collector sidecar by setting the sidecar.opentelemetry.io/inject pod annotation, and avoid the common mistake of annotating a Deployment instead of its pod template."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/collector/sidecar-injection.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inject a Collector sidecar into pods

A sidecar Collector is created by an `OpenTelemetryCollector` with `spec.mode: sidecar`, and injected into pods that carry the annotation `sidecar.opentelemetry.io/inject` set to `"true"` or to the name of a concrete resource.

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata:
  name: sidecar-for-my-app
spec:
  mode: sidecar
  config:
    receivers:
      jaeger:
        protocols:
          thrift_compact: {}
    exporters:
      debug: {}
    service:
      pipelines:
        traces:
          receivers: [jaeger]
          exporters: [debug]
```

Annotation values:
- `"true"`: inject the sidecar-mode Collector found in the pod's namespace.
- `"sidecar-for-my-app"`: a named OpenTelemetryCollector in the current namespace.
- `"my-other-namespace/my-instrumentation"`: name and namespace of a Collector in another namespace.
- `"false"`: do not inject.

When several sidecar-mode Collectors exist in a namespace you must use a concrete name; with exactly one, `"true"` selects it.

For Deployments, StatefulSets and similar, put the annotation under `spec.template.metadata.annotations` (the PodTemplate). The docs show the annotation on the Deployment's own metadata as WRONG and on the pod template as CORRECT.

In sidecar mode the Collector container gets the environment variable `OTEL_RESOURCE_ATTRIBUTES` with Kubernetes resource attributes, ready to be consumed by the `resourcedetection` processor.

## Checked

2026-11-04. Confirmed against docs/collector/sidecar-injection.md: the `sidecar.opentelemetry.io/inject` annotation and its four values, `mode: sidecar`, the rule for several sidecar Collectors in one namespace, the PodTemplate placement with the WRONG and CORRECT example, and the `OTEL_RESOURCE_ATTRIBUTES` variable for the resourcedetection processor. Nothing removed.

Method: documentation only; no commands were run.
