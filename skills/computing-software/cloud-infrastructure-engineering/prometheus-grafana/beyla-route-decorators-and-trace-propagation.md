---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.beyla-route-decorators-and-trace-propagation
name: beyla-route-decorators-and-trace-propagation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [beyla, beyla-routes, beyla-traces, ebpf, route-cardinality, context-propagation]
level: advanced
status: docs-checked
description: "Configure Grafana Beyla route patterns, ignored routes and the unmatched mode to keep http.route cardinality low, and enable eBPF trace context propagation."
sources: ["https://grafana.com/docs/beyla/latest/configure/routes-decorator/", "https://grafana.com/docs/beyla/latest/distributed-traces/", "https://grafana.com/docs/beyla/latest/configure/options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Beyla routes and trace propagation

**Goal:** low-cardinality `http.route` values on metrics and traces from eBPF auto-instrumentation, and connected traces across services.

## Routes
The `routes` section must be configured in the YAML file. Without it Beyla creates a default routes stage that uses the `heuristic` decorator.
```yaml
routes:
  patterns:
    - /users/{id}/orders/{orderId}
    - /api/v1/products/:sku
  ignored_patterns:
    - /health
    - /metrics
  ignore_mode: all
  unmatched: heuristic
```
- `patterns`: URL path patterns that set `http.route`. Tags are `:name` or `{name}`. A trailing `*` matches path prefixes (`/user/*` matches `/user` and everything under it).
- `ignored_patterns`: events matching them are discarded; same format as `patterns`. `ignore_mode` is `all` (default; metrics and traces), `traces` (metrics still recorded) or `metrics` (traces still recorded).
- `unmatched` (default `heuristic`): `unset` leaves `http.route` unset; `path` copies the raw path (can cause cardinality explosion); `wildcard` sets a generic `/**`; `heuristic` replaces components that contain numbers or characters outside ASCII letters, `-` and `_`, and alphabetical components that do not look like words, with `wildcard_char`; `low-cardinality` extends heuristic by collapsing any path segment whose children exceed `max_path_segment_cardinality` into a wildcard.
- `wildcard_char` defaults to `"*"` (quoted, single character); `max_path_segment_cardinality` defaults to 10. The low-cardinality route database is per service, in memory, and resets on every Beyla restart.
- The heuristic decorator is best effort and can still explode cardinality (the page's example is GitHub-style paths); consider `low-cardinality` there.

## Distributed traces
- Propagation uses the W3C `traceparent` header. Beyla reads incoming trace context, tracks execution flow and adds `traceparent` to outgoing HTTP/gRPC requests; if the app already adds it, Beyla uses that value; if no incoming context exists, Beyla generates one per the W3C spec.
- Network-level propagation is disabled by default. Enable it with `BEYLA_BPF_CONTEXT_PROPAGATION=all` or:
```yaml
ebpf:
  context_propagation: "all"
```
Other values: `headers`, `tcp`, `headers,tcp` (same as `all`), `disabled`. `headers` injects `traceparent` into HTTP headers and interoperates with OpenTelemetry SDK-instrumented services; `tcp` sends trace and span IDs in TCP option kind 25 and needs Beyla on both ends. Network header injection is limited to unencrypted HTTP/2 traffic.
- For Go applications Beyla can also write headers at library level (HTTP, HTTP/2, HTTPS, gRPC) using `bpf_probe_write_user`.

## Gotchas
- HTTP header-based context propagation requires Linux kernel 5.17 or higher (Beyla's general minimum is 5.8).
- If the kernel is in integrity lockdown mode (typical with Secure Boot), the Go library-level approach is unavailable: if `/sys/kernel/security/lockdown` exists and the mode is not `[none]`, Beyla cannot perform that propagation. In containers mount `/sys/kernel/security` from the host, otherwise Beyla assumes no integrity mode.
- Network-level propagation on Kubernetes: the page's recommended deployment is a DaemonSet with `hostNetwork: true` and `hostPID: true`, host `/sys/fs/cgroup` and `/sys/kernel/tracing` mounted, and the `CAP_NET_ADMIN` capability (the example also adds BPF, SYS_PTRACE, NET_RAW, CHECKPOINT_RESTORE, DAC_READ_SEARCH, PERFMON and SYS_ADMIN). Without the cgroup mount some requests may not have their context propagated.
- TCP propagation does not survive proxies or load balancers that terminate the original TCP connection.

## Verify
- [ ] The set of `http.route` values for the service is small and contains your patterns (or wildcard values), not raw paths.
- [ ] A trace spanning two instrumented services shares one trace ID.

## Checked
Date: 2026-11-07. Read in full: the Beyla routes decorator page and the Beyla distributed traces page; the Beyla global configuration page (read lines 1-95 of ~115; it covers selection, trace_printer, enforce_sys_caps and eBPF options and has nothing about exporters). Corrections: the draft listed a context propagation mode `ip` (IP options); the page lists `all`, `headers`, `tcp`, `headers,tcp` and `disabled` (TCP option kind 25, not IP options). Removed as not on these pages: `otel_traces_export` and sampler examples, the metric name `http.server.request.duration`, "Go frameworks report routes automatically", the TLS library-level claim, "ignoring routes in Beyla is cheaper than in the collector", the `CAP_SYS_ADMIN`-only requirement and the Tempo/Prometheus verify specifics.
Method: documentation only; no commands were run.
