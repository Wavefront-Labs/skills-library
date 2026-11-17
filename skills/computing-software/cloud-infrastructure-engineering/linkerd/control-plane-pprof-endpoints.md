---
id: computing-software.cloud-infrastructure-engineering.linkerd.control-plane-pprof-endpoints
name: control-plane-pprof-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, pprof, profiling, debug, control-plane]
level: advanced
status: docs-checked
description: "Enable the pprof endpoints on Linkerd control plane components and fetch profiles over the admin-http port."
sources:
  - https://linkerd.io/2.19/tasks/using-debug-endpoints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd control plane components can serve Go profiling data at `/debug/pprof`. The endpoint is disabled by default. Enable it when installing or upgrading with `--set enablePprof=true`, or set the Helm value `enablePprof=true`.

The data is served on the `admin-http` port. Find that port from the pod spec; for the identity pod:

```bash
kubectl -n linkerd get po \
    $(kubectl -n linkerd get pod -l linkerd.io/control-plane-component=identity \
        -o jsonpath='{.items[0].metadata.name}') \
    -o=jsonpath='{.spec.containers[*].ports[?(@.name=="admin-http")].containerPort}'
```

Then `kubectl port-forward` that port and request the paths you need. Available profiles:

- `allocs`: sampling of all past memory allocations
- `block`: stack traces that led to blocking on synchronization primitives
- `cmdline`: the program's command line
- `goroutine`: stack traces of all current goroutines
- `heap`: sampling of live allocations; the `gc` GET parameter runs GC first
- `mutex`: holders of contended mutexes
- `profile`: CPU profile; use the `seconds` GET parameter for duration
- `threadcreate`: stack traces that led to new OS threads
- `trace`: execution trace; use `seconds` and read it with `go tool trace`

Analyse CPU and other profiles with `go tool pprof`, which can output PDF, DOT, PNG and other formats. Turn pprof back off after collecting data.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/using-debug-endpoints/.

Removed or reworded: Nothing.

Method: documentation only; no commands were run.
