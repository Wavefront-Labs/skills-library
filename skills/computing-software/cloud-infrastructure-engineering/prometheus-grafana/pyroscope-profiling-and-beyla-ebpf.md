---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.pyroscope-profiling-and-beyla-ebpf
name: pyroscope-profiling-and-beyla-ebpf
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, pyroscope, grafana-pyroscope, continuous-profiling, profiling, flame-graph, pprof, ebpf, ebpf-instrumentation, beyla, grafana-beyla, zero-code, auto-instrumentation, alloy-pyroscope, pyroscope-ebpf, profiles-to-traces, span-profiles, cpu-profile, memory-profile, diff-flame-graph, kernel-requirements, btf, otel-ebpf-instrumentation]
level: advanced
status: docs-checked
description: "Zero-code signals: continuous profiling with Grafana Pyroscope (SDK, Alloy, eBPF) and RED metrics and traces from eBPF with Beyla, with kernel, BTF and privilege requirements."
sources: ["https://grafana.com/docs/pyroscope/latest/", "https://grafana.com/docs/pyroscope/latest/configure-client/", "https://grafana.com/docs/alloy/latest/reference/components/pyroscope/pyroscope.ebpf/", "https://grafana.com/docs/beyla/latest/", "https://opentelemetry.io/docs/zero-code/obi/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Pyroscope continuous profiling and Beyla eBPF instrumentation

**Goal:** answer "which function burns the CPU" and "what are this un-instrumented service's latency and error rates"
without changing application code.

## Part A: Pyroscope

### A1. Three ways to send profiles (Pyroscope client docs)
1. **Auto-instrumentation with Grafana Alloy** (preferred collector; Grafana Agent is deprecated). Alloy supports
   profiling with eBPF, Java and Golang in pull mode, with no application changes.
2. **SDK instrumentation**: Pyroscope SDKs (pip, npm, Ruby gem and others) push profiles to the Pyroscope server; use
   them for full control, such as profiling specific sections of code with labels.
3. **SDK through Alloy**: SDKs send to Alloy's `pyroscope.receive_http` component, which forwards to the server. Benefits:
   lower latency to a local Alloy, authentication and routing handled in Alloy, and enrichment with infrastructure
   labels such as Kubernetes metadata.

eBPF supports some languages (for example Go, Python) better than others, per the client docs.
Tag/label names must match `[a-zA-Z_][a-zA-Z0-9_]`; a period is not valid in Pyroscope tags and labels.

### A2. Alloy `pyroscope.ebpf`
- Embeds the grafana/opentelemetry-ebpf-profiler (a fork of open-telemetry/opentelemetry-ebpf-profiler). It collects
  CPU profiles.
- Must run as root and inside the host PID namespace. On Kubernetes the simplest option is
  `securityContext.privileged: true`; least-privilege capabilities are `BPF`, `PERFMON`, `SYS_PTRACE`,
  `CHECKPOINT_RESTORE` (kernel 5.9+, else `SYS_ADMIN`), `SYS_RESOURCE`, `DAC_READ_SEARCH` and `SYSLOG`, plus read-only
  mounts of `/sys/kernel/tracing` (older kernels may need `/sys/kernel/debug`).
- Needs writable storage at `/tmp/symb-cache` for the symbol cache.
- Supported: native code (C/C++, Rust, Zig, Go) and HotSpot JVM, .NET, Python, Ruby, PHP, Node.js (V8), Perl. Each
  language has an enable flag: `go_enabled`, `hotspot_enabled`, `python_enabled`, `dotnet_enabled`, `ruby_enabled`,
  `php_enabled`, `perl_enabled`, `v8_enabled`, all default true.
- Frame pointers are not required: the profiler uses `.eh_frame` data for unwinding (Pyroscope client docs); see the
  Pyroscope "Troubleshooting unknown symbols" page for extra requirements.
- Key arguments: `forward_to` (required), `targets`, `collect_interval` (default `15s`), `sample_rate` (default 19 per
  second), `off_cpu_threshold` (default 0, which disables off-CPU profiling), `pid_label`, `kernel_frames` (default true).
  Several cache-size arguments are deprecated no-ops. `no_kernel_version_check` is risky: only for old kernels with
  backported eBPF features.
- Defining more than one `pyroscope.ebpf` component is not recommended (extra memory and CPU).
- Debug metrics include `pyroscope_ebpf_active_targets` and `pyroscope_ebpf_profiling_sessions_failing_total`; the
  component is unhealthy if the session fails to start, for example from missing privileges or an unsupported kernel.

## Part B: Beyla (eBPF auto-instrumentation)
OpenTelemetry eBPF Instrumentation (OBI) is the OpenTelemetry project counterpart; the Beyla docs include a page on
using OBI instead of Beyla.

### B1. What it gives
Without code changes, Beyla captures trace spans and RED metrics for Linux HTTP/S and gRPC services using eBPF on
application executables and the OS networking layer. It exports OpenTelemetry format and native Prometheus metrics,
decorates telemetry with Kubernetes Pod and Service metadata, and integrates with Grafana Alloy. Because it observes at
the kernel network level, its latency includes request queue time, unlike library instrumentation that measures service
time.

### B2. Requirements
- Linux kernel 5.8 or higher with BTF enabled (check that `/sys/kernel/btf/vmlinux` exists; BTF is default on most
  distributions with kernel 5.14+).
- HTTP header-based trace context propagation needs kernel 5.17 or higher (`bpf_loop` helper).
- RHEL 8 family ships kernel 4.18 with backported eBPF patches and is supported.
- Go programs: Go 1.17 or later at minimum, and a Go major version no more than 3 behind current stable.
- Administrative rights; finer-grained capabilities `CAP_DAC_READ_SEARCH`, `CAP_SYS_PTRACE`, `CAP_PERFMON`, `CAP_BPF`,
  `CAP_CHECKPOINT_RESTORE`, `CAP_NET_RAW`; network observability with Linux Traffic Control also needs
  `CAP_NET_ADMIN`.

### B3. When to use which (Beyla compatibility matrix)
- Beyla is strongest as a zero-code baseline for RED metrics and service graphs. SDKs remain the default for detailed
  distributed tracing.
- Beyla tracing: recommended for Go HTTP/gRPC; supported with limitations for Java thread-pool, Node.js, Python,
  Ruby and .NET (a .NET entry-point service may not trace correctly); not recommended for reactive Java.
- If a service already uses an OTel SDK, Beyla disables its own tracing; set `span.metrics.skip=true` via
  `OTEL_RESOURCE_ATTRIBUTES` to stop duplicate span metrics when Beyla also generates span metrics or service graphs.
- Do not run Beyla tracing and SDK tracing in parallel for the same service without verifying behaviour.
- Beyla only provides generic metrics and transaction-level spans; language agents or manual instrumentation are
  still recommended for custom spans and business attributes.
- Profiles and OBI traces: `pyroscope.ebpf` has `obi_process_context_enabled` (default true) to correlate profiles with
  traces from OBI-compatible components.

## Gotchas
- `pyroscope.ebpf` without root, host PID namespace or the capabilities above fails to start and reports unhealthy.
- Some Beyla trace support is weak for async or reactive frameworks: validate before production.
- Check metric cardinality (Beyla and OBI docs have cardinality pages) and route handling before wide rollout; look
  up the exact route-decorator settings in the Beyla configuration docs.

## Verify
- [ ] The Alloy `pyroscope.ebpf` component reports healthy and `pyroscope_ebpf_profiling_sessions_failing_total`
      stays flat.
- [ ] CPU profiles for the target appear in Pyroscope and a time-range comparison highlights a changed function.
- [ ] `/sys/kernel/btf/vmlinux` exists on each node before deploying Beyla.
- [ ] Measure the agents' own CPU on a node and record it before rollout.

## Checked
2026-11-08: confirmed against the Pyroscope client configuration page, the Alloy pyroscope.ebpf reference, the Beyla
overview (requirements, capabilities, compatibility matrix) and the OBI overview. Fixed: eBPF profiling does not need
frame pointers, and the `sample_rate` default is 19, not 97. Removed: Helm commands, Alloy pprof-scrape and Go SDK
code samples, data source settings, flame-graph and span-profile UI behaviour, profile type list, overhead claims,
the Beyla YAML (discovery, routes, exporters, env var names), and cloud node-image BTF claims, because the fetched
pages did not state them.
Method: documentation only; no commands were run.
