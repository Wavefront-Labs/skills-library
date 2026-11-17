---
id: computing-software.cloud-infrastructure-engineering.contour.contour-debug-logs-and-pprof
name: contour-debug-logs-and-pprof
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [debug-logging, kubernetes-debug, envoy-log-level, pprof, port-6060, tls-debugging]
level: practitioner
status: docs-checked
description: "Enabling Contour --debug and --kubernetes-debug, Envoy --log-level debug for TLS failures, and Contour pprof on 127.0.0.1:6060 via port-forward."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/troubleshooting/contour-debug-log.md", "https://github.com/projectcontour/contour/blob/main/site/content/docs/main/troubleshooting/envoy-debug-log.md", "https://github.com/projectcontour/contour/blob/main/site/content/docs/main/troubleshooting/profiling-contour.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debug logging and profiling

Contour (`contour serve`):
- `--debug` enables general debug logging showing how API resources are processed.
- `--kubernetes-debug=<int>` enables verbose Kubernetes client logging; a higher number means more detail. Use it to debug interaction with the API server.

Envoy: the `envoy` container takes `--log-level` (default `info`). Edit the `envoy` DaemonSet in `projectcontour` and replace `--log-level info` with `--log-level debug`. This is particularly useful for TLS connection failures.

Profiling: Contour exposes net/http/pprof handlers on `127.0.0.1:6060` by default (`--debug-http-address`/`--debug-http-port` change it). Reach it with:

```bash
CONTOUR_POD=$(kubectl -n projectcontour get pod -l app=contour -o name | head -1)
kubectl -n projectcontour port-forward $CONTOUR_POD 6060
```

Then use `go tool pprof` or `go tool trace` against that port.

## Checked

2026-11-04. Confirmed against the Contour debug log, Envoy debug log and profiling troubleshooting pages and the configuration reference (--debug-http-address/port): the fields, defaults, flags and behaviours stated above. Removed: the heap-profile URL example, the /debug/dag remark and the closing advice about verbose logs (not on the pages).

Method: documentation only; no commands were run.
