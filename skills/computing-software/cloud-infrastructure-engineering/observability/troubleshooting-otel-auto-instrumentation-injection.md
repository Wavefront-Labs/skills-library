---
id: computing-software.cloud-infrastructure-engineering.observability.troubleshooting-otel-auto-instrumentation-injection
name: troubleshooting-otel-auto-instrumentation-injection
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [injection-troubleshooting, instrumentation-crd-config, inject-annotations, opentelemetry-operator, auto-instrumentation]
level: practitioner
status: docs-checked
description: "Fix OpenTelemetry Operator auto-instrumentation that does not inject or export: annotation placement, Instrumentation CR lookup, restarts, webhook errors and container selection."
sources: ["https://opentelemetry.io/docs/platforms/kubernetes/operator/troubleshooting/automatic/", "https://opentelemetry.io/docs/platforms/kubernetes/operator/automatic/", "https://github.com/open-telemetry/opentelemetry-operator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting auto-instrumentation injection

## Checklist
1. Annotation on the **pod template**, not the Deployment metadata:
```yaml
spec:
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-java: "true"     # or "my-ns/my-instrumentation"
```
Value `"true"` selects an Instrumentation resource; see the operator docs for the other forms.
2. An `Instrumentation` CR exists and is healthy: `kubectl describe otelinst -n <namespace>`.
3. Pods created **after** the Instrumentation and annotation: restart (`kubectl rollout restart deploy/x`); injection happens only at pod creation.
4. Webhook ran: `kubectl describe pod` shows init container `opentelemetry-auto-instrumentation` and env like `JAVA_TOOL_OPTIONS`, `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_ENDPOINT`. If missing, check operator logs (`kubectl logs -n opentelemetry-operator-system deploy/opentelemetry-operator-controller-manager`) and webhook reachability.
5. Multi-container pods: `instrumentation.opentelemetry.io/container-names: "app"`.
6. Exporting: the endpoint in the Instrumentation (`spec.exporter.endpoint`) must be reachable from the pod and match the protocol (the docs show .NET and Go defaulting to otlp over http/protobuf, so point them at port 4318; Python does too from operator v0.108.0).

## Language specifics
- .NET: the runtime annotation `instrumentation.opentelemetry.io/otel-dotnet-auto-runtime` supports `linux-x64` (default) and `linux-musl-x64`.
- Go: set `instrumentation.opentelemetry.io/otel-go-auto-target-exe` to the target executable path.

## Verify
- [ ] The pod shows injected env/init container and traces appear for the service name within a minute of traffic.

## Checked
- 2026-10-28. Checked against the OpenTelemetry Operator auto-instrumentation and troubleshooting pages and the operator repo manifests (docs and main, 2026-10).
- Confirmed: `inject-java`/`inject-python`/`inject-dotnet` annotations, `container-names`, init container name `opentelemetry-auto-instrumentation`, `kubectl describe otelinst`, .NET runtime annotation values, Go `otel-go-auto-target-exe`, 4318 http/protobuf defaults, operator controller-manager deployment name.
- Fixed: init container name had a `-java` suffix not in the docs. Removed (unconfirmed): `failurePolicy: Ignore` claim, annotation value forms, libc and bundling notes, privileged Go requirement, LimitRange and double-export gotchas.
Method: documentation only; no commands were run.
