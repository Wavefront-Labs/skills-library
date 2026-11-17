---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-init-containers
name: opentelemetry-operator-instrumentation-init-containers
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, init-containers, init-container-instrumentation, instrumentation-ordering, container-names-init]
level: advanced
status: docs-checked
description: "Instrument init containers by listing them in container-names; the operator inserts its instrumentation init container before the target, and Go, Apache and Nginx are unsupported."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/init-containers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Instrument init containers

Init containers are instrumented by naming them in the `container-names` annotation. When an init container is targeted, the operator inserts the instrumentation init container before the target init container in the pod's init sequence, so the agent files are present when the target runs.

Supported for init containers: Java, Python, Node.js, .NET and SDK-only injection.
Not supported: Go (it does not support multi-container pods), Apache HTTPD and Nginx.

Kubernetes guarantees that container names are unique across `initContainers` and `containers` in a pod spec, so the operator can tell unambiguously which kind a name refers to.

Example combining both kinds:

```yaml
metadata:
  annotations:
    instrumentation.opentelemetry.io/inject-python: "true"
    instrumentation.opentelemetry.io/container-names: "my-init-job,myapp"
spec:
  initContainers:
    - name: my-init-job
      image: my-python-init-image
  containers:
    - name: myapp
      image: my-python-app-image
```

Both `my-init-job` and `myapp` receive Python auto-instrumentation.

With multi-instrumentation, the per-language annotations such as `python-container-names` and `java-container-names` also accept init container names for these same languages. Without any container-names annotation, only the first regular container is instrumented, never an init container.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/init-containers.md: instrumenting init containers through the container-names annotation, the instrumentation init container inserted before the target, the supported list (Java, Python, Node.js, .NET, SDK-only), the unsupported list (Go, Apache HTTPD, Nginx), unique container names across the pod, and the example. Confirmed against multi-instrumentation.md and multi-container.md: per-language annotations accept init container names for those languages, and the first container from `.spec.containers` (not init containers) is used when no annotation is set. Nothing removed.

Method: documentation only; no commands were run.
