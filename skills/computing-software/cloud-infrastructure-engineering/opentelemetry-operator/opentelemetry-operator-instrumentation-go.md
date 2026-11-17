---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-go
name: opentelemetry-operator-instrumentation-go
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, go, otel-go-auto-target-exe, ebpf-go, privileged-go, inject-go]
level: advanced
status: docs-checked
description: "Use Go auto-instrumentation, which needs the OTEL_GO_AUTO_TARGET_EXE path, runs privileged as root, is disabled by default and supports only one instrumented container."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/go.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/multi-container.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/init-containers.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/feature-gates.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Go auto-instrumentation requirements

Go auto-instrumentation has stricter requirements than other languages.

Enable it in the operator first: `enable-go-instrumentation` defaults to false.

Annotations:

```
instrumentation.opentelemetry.io/inject-go: "true"
instrumentation.opentelemetry.io/otel-go-auto-target-exe: "/path/to/container/executable"
```

`OTEL_GO_AUTO_TARGET_EXE` must hold a valid executable path. It can be given by the annotation or by an env var in the `Instrumentation` resource, and the annotation takes precedence. If it is missing, injection aborts and the original pod is left unchanged, so a Go pod that silently has no instrumentation usually lacks this.

Privileges: Go auto-instrumentation requires elevated permissions, and these are set automatically:

```yaml
securityContext:
  privileged: true
  runAsUser: 0
```

Account for this in Pod Security Admission and admission policies.

Other constraints:
- Go does not support multi-container pods. The first container should be the only one you want instrumented; the multi-instrumentation page shows `go-container-names: "go1"`, naming a single container.
- Go is not supported for init containers.
- Like Python and .NET, it uses http/proto by default, so set `OTEL_EXPORTER_OTLP_ENDPOINT` to port 4318 in `spec.go.env` if the common endpoint uses 4317.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/languages/go.md: `inject-go`, `otel-go-auto-target-exe`, the annotation taking precedence over the Instrumentation env, injection aborting with the pod unchanged when the path is missing, and the automatic `privileged: true` and `runAsUser: 0`. Confirmed against docs/reference/feature-gates.md: `enable-go-instrumentation` false by default. Confirmed against multi-container.md, multi-instrumentation.md and init-containers.md: no multi-container support, first container only, not supported for init containers. Confirmed against docs/auto-instrumentation/README.md: http/proto default and `spec.go.env` with port 4318. Softened the claim about `go-container-names` to what the page shows.

Method: documentation only; no commands were run.
