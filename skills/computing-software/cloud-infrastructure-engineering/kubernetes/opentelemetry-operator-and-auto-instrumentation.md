---
id: computing-software.cloud-infrastructure-engineering.kubernetes.opentelemetry-operator-and-auto-instrumentation
name: opentelemetry-operator-and-auto-instrumentation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, opentelemetry, otel-operator, opentelemetrycollector, instrumentation-crd, sidecar-injection, auto-instrumentation, otlp, distributed-tracing, collector, daemonset-mode, gateway-mode]
level: advanced
status: docs-checked
description: "Running the OpenTelemetry Operator in Kubernetes: Collector CRD deployment modes, auto-instrumentation injection via webhook, and where traces get silently dropped."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/collector/deployment-modes.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/collector/sidecar-injection.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/resource-attributes.md", "https://opentelemetry.io/docs/platforms/kubernetes/operator/automatic/", "https://opentelemetry.io/docs/collector/internal-telemetry/", "https://opentelemetry.io/docs/collector/deploy/gateway/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTelemetry Operator: Collector modes and auto-instrumentation in k8s

**Goal:** stand up traces (and metrics/logs) in a cluster using the Operator's two separate
mechanisms — the `OpenTelemetryCollector` CRD and the `Instrumentation` CRD — and know which
layer is responsible when a service's traces never show up in the backend.

## 1. Two CRDs, two jobs — don't conflate them
- **`OpenTelemetryCollector`** — deploys and configures the Collector itself (receivers,
  processors, exporters pipeline). The Operator can run it in several `mode:` values:
  - `deployment` (default) — a standalone Collector, apps send OTLP to its Service; simplest,
    but a single point of failure/bottleneck unless replicated, and loses the "always
    co-located with the app" locality.
  - `daemonset` — one Collector per node, apps send to `$(HOST_IP):4317`; keeps traffic
    local, but every node pays the Collector's resource cost even if idle.
  - `sidecar` — injected into each pod needing it (opt-in via the pod-template annotation
    `sidecar.opentelemetry.io/inject: "true"`, or the name of a specific sidecar-mode
    Collector when a namespace has several); tightest locality, highest per-pod overhead,
    and the sidecar's own restarts/crashes are invisible unless you watch that specific
    container.
  - `statefulset` — for Collectors that need stable identity.
  A common production pattern is **two tiers**: DaemonSet "agent" Collectors (local
  receive, light processing) forwarding via OTLP to a `deployment`-mode "gateway" Collector
  tier doing tail-sampling, batching and the actual export — look for this when inheriting an
  unfamiliar setup before assuming there's only one Collector to check.

- **`Instrumentation`** — a CRD that configures the Operator's **mutating admission
  webhook** to inject a language-specific auto-instrumentation agent (Java, Node.js, Python
  and .NET through an init container; Go through an eBPF agent sidecar that also needs
  `OTEL_GO_AUTO_TARGET_EXE`) into pods annotated
  `instrumentation.opentelemetry.io/inject-<lang>` (`java`, `nodejs`, `python`, `dotnet`, `go`,
  or `sdk` for env-only injection). Values: `"true"` (the Instrumentation in the pod's
  namespace), `"my-instrumentation"` (by name in the same namespace),
  `"other-namespace/my-instrumentation"`, or `"false"`. The annotation can also be set on a
  namespace. Injection happens when a pod is created, so **existing pods are not
  instrumented**; roll the Deployment (`kubectl rollout restart`) after adding the annotation.
  The `Instrumentation` object must exist before the pods are created.

## 2. Where traces actually go missing
Diagnose in this order, since each layer fails silently into the next:
1. **App never emits spans** — check the app's own OTEL SDK logs (`OTEL_LOG_LEVEL=debug`) or,
   for auto-instrumentation, confirm the init container actually ran:
   `kubectl get events -n <ns>` should show `Created` and `Started` for the
   `opentelemetry-auto-instrumentation` init container, and the main container's env should
   include `OTEL_EXPORTER_OTLP_ENDPOINT` from the `Instrumentation` — if not, the webhook never
   matched (check the annotation key and value, that it is on the pod template, and that the
   `Instrumentation` existed before the pod was created).
2. **Collector receiver never gets the OTLP call** — wrong endpoint (sidecar mode needs
   `localhost:4317`, daemonset mode needs the node's `$(HOST_IP)`, deployment mode needs the
   Collector's Service DNS name) is the single most common misconfiguration when copying a
   sidecar-mode example into a daemonset-mode cluster or vice versa.
3. **Collector pipeline drops the span** — a misconfigured or over-aggressive
   `tail_sampling`/`probabilistic_sampler` processor, or a `memory_limiter` processor
   refusing data under pressure (watch `otelcol_receiver_refused_spans`; the Collector exposes
   its own metrics in Prometheus format on port 8888 by default and should be scraped).
4. **Exporter fails to the backend** — auth/TLS to the trace backend; check Collector logs
   for exporter errors, `otelcol_exporter_send_failed_spans` and `otelcol_exporter_queue_size`.

## 3. Context propagation gaps
Auto-instrumentation only patches supported libraries (HTTP clients/servers, common DB
drivers, messaging clients) — a custom thread pool, a fire-and-forget goroutine, or a queue
hop through a broker without W3C `traceparent` propagation **breaks the trace into
disconnected fragments** with no error anywhere; this looks like "tracing is broken" but is
actually a propagation gap the instrumentation agent cannot see across. For service-mesh
environments layering their own spans (Envoy/Istio), see the mesh's documentation for how its
spans relate to app-level spans — mixing mesh-origin and app-origin trace IDs without
matching propagation headers produces two separate trace trees instead of one.

## Gotchas
- The Operator's webhook only fires at **pod creation**; a namespace-wide
  `Instrumentation` default annotation added after pods already exist needs those
  Deployments rolled, not just the namespace patched.
- Without `OTEL_SERVICE_NAME`, a `resource.opentelemetry.io/service.name` annotation or
  (when enabled) `app.kubernetes.io/name` labels, the Operator derives `service.name` from the
  pod's metadata, such as the owning Deployment's name — a renamed Deployment changes
  `service.name` in the backend, breaking existing dashboards/alerts built on the old name.
- Sidecar mode doubles pod count's worth of sidecar containers across the cluster — budget
  CPU/memory requests for it explicitly; it is not free and not optional once injected (a pod
  without enough headroom for the sidecar can go `Pending`).
- The Operator's install manifest expects cert-manager to issue the webhook's TLS
  certificate — a broken or expired certificate here stops injection with no
  application-level symptom until someone notices traces went flat.

## Verify
- [ ] A test pod's events show the injected init container started and the OTLP env vars are set.
- [ ] `otelcol_receiver_accepted_spans` increments on the Collector matching app traffic (the
      Collector omits the Prometheus `_total` suffix by default).
- [ ] `otelcol_exporter_sent_spans` increments with no matching `otelcol_exporter_send_failed_spans` growth.
- [ ] A synthetic end-to-end trace (client → service A → service B) appears as one connected trace in the backend, not fragments.

## Checked
2026-10-27 against the opentelemetry-operator docs (main: deployment modes, sidecar injection,
resource attributes, README) and opentelemetry.io (main: Operator auto-instrumentation,
Collector internal telemetry). Confirmed: the four modes with `deployment` as default, the
sidecar annotation values, the `inject-<lang>` annotation names and values, Go's eBPF sidecar,
the `opentelemetry-auto-instrumentation` init container and ordering requirement, the
`service.name` precedence, cert-manager in the install steps, and the internal metric names,
port 8888 and the `_total` suffix default. Fixed: `otelcol_processor_dropped_spans` is not a
listed metric, the `_total` metric names in Verify, the "LD_PRELOAD" description, and an
`Instrumentation` namespace selector that does not exist.
Method: documentation only; no commands were run.
