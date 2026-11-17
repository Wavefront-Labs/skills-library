---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-python
name: opentelemetry-operator-instrumentation-python
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, python, musl, glibc, otel-python-platform, inject-python]
level: practitioner
status: docs-checked
description: "Inject Python auto-instrumentation and select the musl platform with the otel-python-platform annotation for Alpine style images, defaulting to glibc."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/python.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Python auto-instrumentation and musl images

Enable with the annotation:

```
instrumentation.opentelemetry.io/inject-python: "true"
```

Python auto-instrumentation also honors a platform annotation so it can run on images with a C library other than glibc:

```
instrumentation.opentelemetry.io/otel-python-platform: "glibc"   # default, may be omitted
instrumentation.opentelemetry.io/otel-python-platform: "musl"    # for Linux musl based images
```

Exporter port: Python auto-instrumentation uses http/proto by default. If your `Instrumentation` `exporter.endpoint` points at port 4317 (gRPC), the README says data must be sent to port 4318 instead, so override the endpoint in the language block:

```yaml
spec:
  python:
    env:
      - name: OTEL_EXPORTER_OTLP_ENDPOINT
        value: http://otel-collector:4318
```

The README example pins the Python image to `ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-python` with a version tag; override `spec.python.image` for a custom build. Python is enabled by default in the operator (`enable-python-instrumentation`), and supports init-container instrumentation and the `python-container-names` annotation for multi-instrumentation pods.

Related per-container controls from the multi-container docs: with multi-instrumentation enabled (the default), name the Python containers with `instrumentation.opentelemetry.io/python-container-names: "python1,python3"`, and Python is one of the languages whose annotation also accepts init container names. Without a container-names annotation, only the first regular container of the pod is instrumented.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/languages/python.md: `inject-python` and the `otel-python-platform` annotation with glibc default and musl. Confirmed against docs/auto-instrumentation/README.md: http/proto default with port 4318 required when the endpoint is 4317, the `spec.python.env` example, the versioned `autoinstrumentation-python` image and `spec.python.image`. Confirmed against feature-gates.md, init-containers.md, multi-container.md and multi-instrumentation.md for the default flag, init container support, `python-container-names` and the first-container rule. Nothing else removed.

Method: documentation only; no commands were run.
