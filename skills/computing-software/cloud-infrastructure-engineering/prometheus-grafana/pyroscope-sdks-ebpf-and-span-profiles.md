---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.pyroscope-sdks-ebpf-and-span-profiles
name: pyroscope-sdks-ebpf-and-span-profiles
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-pyroscope, pyroscope-go-sdk, pyroscope-java-agent, pyroscope-python, alloy-pyroscope-ebpf, pyroscope-ebpf-alloy, span-profiles-setup, traces-to-profiles, flame-graph-analysis, profile-diff]
level: advanced
status: docs-checked
description: "Collect continuous profiles into Pyroscope via language SDKs or Alloy eBPF, link spans to profiles, and read flame graphs and diff views to find regressions."
sources: ["https://grafana.com/docs/pyroscope/latest/configure-client/", "https://grafana.com/docs/pyroscope/latest/configure-client/grafana-alloy/ebpf/", "https://grafana.com/docs/pyroscope/latest/configure-client/trace-span-profiles/", "https://grafana.com/docs/pyroscope/latest/view-and-analyze-profile-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pyroscope: SDKs, eBPF, span profiles, flame graphs

## SDKs (push to Pyroscope)
```go
pyroscope.Start(pyroscope.Config{
  ApplicationName: "checkout", ServerAddress: "http://pyroscope:4040",
  Tags: map[string]string{"env": "prod", "version": version},
  ProfileTypes: []pyroscope.ProfileType{pyroscope.ProfileCPU, pyroscope.ProfileAllocSpace, pyroscope.ProfileInuseSpace, pyroscope.ProfileGoroutines, pyroscope.ProfileMutexDuration},
})
```
- Java: `-javaagent:pyroscope.jar` with `PYROSCOPE_APPLICATION_NAME`, `PYROSCOPE_SERVER_ADDRESS`,
  `PYROSCOPE_PROFILER_EVENT` (itimer, cpu or wall; default itimer, with JFR format enabled via `PYROSCOPE_FORMAT=jfr`),
  `PYROSCOPE_PROFILER_ALLOC=512k` (allocation profiling is off until set; 512k is the suggested start).
- Python: `pyroscope.configure(application_name=..., server_address=..., tags={...})` (`pyroscope-io` package).
- Go alternative: Alloy `pyroscope.scrape` pulls the `/debug/pprof/*` endpoints (import `net/http/pprof` and the godeltaprof pprof package).

## eBPF via Alloy (no code changes, CPU profiles only)
```alloy
discovery.kubernetes "pods" { role = "pod" }
pyroscope.ebpf "default" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [pyroscope.write.default.receiver]
}
pyroscope.write "default" { endpoint { url = "http://pyroscope:4040" } }
```
Alloy must run as root in the host PID namespace; on Kubernetes the simplest option is `securityContext.privileged: true`,
or grant the specific capabilities listed in the `pyroscope.ebpf` reference and mount the kernel tracing path. eBPF does not
profile memory or lock contention. Supported: C/C++, Go, Rust, Zig, plus Java (HotSpot), .NET, Python, Ruby, PHP, Node.js
and Perl, each switchable in the component.

## Span profiles (traces -> profiles)
Span-aware instrumentation tags each sample with the active span (`span_id`, `trace_id` labels); spans that can have a
profile carry the `pyroscope.profile.id` span attribute, which Grafana uses to link a span to its profile. By default only
the local root span is labelled. Go: `otel.SetTracerProvider(otelpyroscope.NewTracerProvider(tp))` with
`github.com/grafana/otel-profiling-go`. Client packages exist for Go, Java, Ruby, .NET and Python. Configure the Tempo
data source in Grafana to discover linked traces and profiles. Very short spans can have no samples.

## Reading flame graphs
- Grafana's Profiles Drilldown app browses, analyses and compares profiles across labels or time periods; Explore and
  dashboards also display Pyroscope data.
- Compare like with like: filter by labels (pod, version) before comparing two periods, so different traffic mixes don't mislead.

## Verify
- [ ] Service appears in Pyroscope with CPU and memory profile types.
- [ ] A slow span in Tempo links to its profile.

## Checked
Date: 2026-10-28. Confirmed against the Pyroscope Go push, Java, Python, Go pull (Alloy), eBPF, span profiles and Go span profiles pages, the Alloy `pyroscope.ebpf` reference and the view-and-analyze page: Go `Config` fields and `ProfileType` constants, Java env variables and defaults, Python `pyroscope.configure` and the `pyroscope-io` package, `pyroscope.scrape` and `/debug/pprof/*`, eBPF requirements, language list and limits, `span_id`, `trace_id`, `pyroscope.profile.id`, `otelpyroscope.NewTracerProvider`. Fixed: the skill said the JVM needs perf maps for eBPF and that eBPF needs a DaemonSet with privileged; the docs list HotSpot JVM as supported and allow least-privilege capabilities. Removed unconfirmed claims: the `pyroscope-otel` Java extension name, the 'Trace to profiles' and 'Profiles for this span' UI labels, and the flame-graph reading and red/green diff rules.
Method: documentation only; no commands were run.
