---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.alloy-pyroscope-scrape-pprof-pull
name: alloy-pyroscope-scrape-pprof-pull
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [pyroscope, pyroscope-scrape, pprof-pull, grafana-alloy, go-pprof, kubernetes-annotations]
level: advanced
status: docs-checked
description: "Pull pprof profiles from Go and other pprof endpoints with Grafana Alloy pyroscope.scrape, discover Kubernetes targets with relabeling, and forward to Pyroscope."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/pyroscope/pyroscope.scrape/", "https://grafana.com/docs/pyroscope/latest/configure-client/grafana-alloy/go_pull/", "https://grafana.com/docs/alloy/latest/reference/components/pyroscope/pyroscope.write/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pulling pprof with Alloy pyroscope.scrape

**Goal:** continuous profiles from services that expose `/debug/pprof/*` endpoints, collected by Alloy in pull mode (no Pyroscope SDK).

## App side (Go)
The Pyroscope Go pull guide has the app import `net/http/pprof` and the godeltaprof handler at start-up:
```go
import _ "net/http/pprof"
import _ "github.com/grafana/pyroscope-go/godeltaprof/http/pprof"
```
(fetch the package with `go get github.com/grafana/pyroscope-go/godeltaprof@latest`). If you do not use `http.DefaultServeMux`, register the handlers on your own mux, e.g. `mux.Handle("/debug/pprof/", http.DefaultServeMux)`.

## Alloy config
Minimum is a `pyroscope.write` and a `pyroscope.scrape` block. With godeltaprof the guide enables the `godeltaprof_*` profile blocks and disables the plain `memory`, `mutex` and `block` ones:
```alloy
pyroscope.write "write_job_name" {
  endpoint { url = "http://localhost:4040" }
}

pyroscope.scrape "scrape_job_name" {
  targets    = [{"__address__" = "localhost:4040", "service_name" = "example_service"}]
  forward_to = [pyroscope.write.write_job_name.receiver]

  profiling_config {
    profile.process_cpu { enabled = true }
    profile.godeltaprof_memory { enabled = true }
    profile.memory { enabled = false }
    profile.godeltaprof_mutex { enabled = true }
    profile.mutex { enabled = false }
    profile.godeltaprof_block { enabled = true }
    profile.block { enabled = false }
    profile.goroutine { enabled = true }
  }
}
```
Kubernetes targets: `discovery.kubernetes "all_pods" { role = "pod" }`, then `discovery.relabel` over `discovery.kubernetes.all_pods.targets` (the guide drops pods whose `__meta_kubernetes_pod_phase` is `Succeeded|Failed|Completed`, copies namespace, pod, node and container labels, and builds `service_name` from `__meta_kubernetes_namespace` and `__meta_kubernetes_pod_container_name` with `separator = "@"`, `regex = "(.*)@(.*)"`, `replacement = "${1}/${2}"`), and pass `discovery.relabel.<name>.output` as `targets`.

## Notes (pyroscope.scrape reference)
- Every target needs `__address__` (host:port); `service_name` is required: set it, or the component infers it from the `pyroscope.io/service_name` pod annotation, then namespace + container name, then Docker names, else `unspecified`.
- Defaults: `scrape_interval` "15s", `scrape_timeout` "10s", `scheme` "http", `delta_profiling_duration` "14s". For delta profiles (default for `profile.process_cpu`) Alloy adds a `seconds` query parameter, default `scrape_interval` minus 1 (so `/debug/pprof/profile?seconds=14`); `scrape_interval` must be at least 2s, and the timeout is extended by `scrape_interval` minus 1s for these requests.
- Default profile blocks enabled: `profile.process_cpu` (`/debug/pprof/profile`), `profile.memory` (`/debug/pprof/allocs`), `profile.block`, `profile.mutex`, `profile.goroutine`. `profile.fgprof` and the `godeltaprof_*` blocks are off by default (paths `/debug/pprof/delta_heap`, `delta_mutex`, `delta_block`).
- A long `scrape_interval` with delta profiles risks hitting the target's HTTP server timeouts (the reference's example: 60s interval against a 30s server timeout fails).
- Custom endpoint: `profile.custom "<type>" { enabled = true  path = "<path>" }` (both required, `delta` optional, default false).
- Authentication to Pyroscope (for example Grafana Cloud): add a `basic_auth` block inside the `endpoint` block of `pyroscope.write` (the Go pull guide shows `username` and `password`).
- A scrape counts as successful on HTTP 200 with a valid pprof body; the component's debug UI shows failure details and last successful scrape.

## Verify
- [ ] The `pyroscope.scrape` component's debug view in Alloy shows a successful last scrape for each target, and the service appears in Pyroscope with the profile types you enabled.

## Checked
Date: 2026-11-07. Read in full: the Pyroscope "Set up Go profiling in pull mode" guide and the `pyroscope.scrape` reference (arguments, targets/special labels, scrape_interval/scrape_timeout, profile.* blocks with defaults, delta argument, examples). `pyroscope.write` was read for its endpoint/basic_auth structure only (searched by headings; not every argument read). Removed as unconfirmed on these pages: the `profiles.grafana.com/cpu.scrape` and `cpu.port` annotation convention and its relabel rules, the `go http.ListenAndServe(":6060")` snippet, the "enable mutex/block rates" advice, "keep scrape_interval at 15 s or more" (the page says at least 2s for delta profiling), the in-cluster pyroscope URL, and the Alloy UI `:12345` verify step. Unopened: the discovery.kubernetes and discovery.relabel reference pages.
Method: documentation only; no commands were run.
