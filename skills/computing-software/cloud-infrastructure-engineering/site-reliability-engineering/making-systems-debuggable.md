---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.making-systems-debuggable
name: making-systems-debuggable
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [debuggability, troubleshooting-tooling, troubleshooting, debug-endpoints, observability, zpages]
level: practitioner
status: docs-checked
description: "Make services easier to troubleshoot: white-box metrics and structured logs from the start, a unique request identifier across RPCs, Go pprof endpoints and OpenTelemetry zPages."
sources: ["https://sre.google/sre-book/effective-troubleshooting/", "https://pkg.go.dev/net/http/pprof", "https://opentelemetry.io/docs/collector/troubleshooting/#zpages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Making systems easier to troubleshoot

SRE Book (Effective Troubleshooting), "Making Troubleshooting Easier":
- build observability, both white-box metrics and structured logs, into each component from the ground up;
- design systems with well-understood, observable interfaces between components;
- make information consistent across the system, for example a unique request identifier throughout the
  span of RPCs from different components, which removes the need to work out which upstream log entry
  matches which downstream one and speeds diagnosis and recovery.

## Go profiling endpoints (`net/http/pprof`)
- Importing the package registers handlers under `/debug/pprof/` (as of Go 1.22, GET only). If you do not
  use `DefaultServeMux`, register the handlers on your own mux.
- `/debug/pprof/` lists available profiles; `/debug/pprof/heap` serves the heap profile;
  `/debug/pprof/profile` returns a CPU profile lasting the `seconds` GET parameter (30 s by default);
  `/debug/pprof/cmdline`, `/symbol` and `/trace` also exist.
```go
mux := http.NewServeMux()
mux.HandleFunc("/debug/pprof/", pprof.Index)
mux.HandleFunc("/debug/pprof/profile", pprof.Profile)
```
Serve it on a listener that is not publicly reachable; who may reach profiling is your decision.

## OpenTelemetry Collector zPages
The zPages extension is exposed locally on port 55679 and inspects live data from the Collector's receivers
and exporters; its TraceZ page at `/debug/tracez` helps debug trace operations. The page notes zPages may
contain error logs the Collector does not emit itself.

## Practical checklist (judgement, not quoted rules)
- Include the request identifier in logs and error responses so a user report maps to a trace.
- Error messages name the dependency and operation that failed.
- Expose the running version and flags on an internal status page.

## Verify
- [ ] From a request ID, on-call can find that request's logs and trace.
- [ ] Profiling and status endpoints exist and are reachable only from internal networks.

## Checked
2026-11-01. Confirmed against the SRE Book Effective Troubleshooting chapter, the Go `net/http/pprof`
package page and the OpenTelemetry Collector troubleshooting page (zPages). Removed: W3C `traceparent`,
RED metric prescription, log field list, `app_build_info`, JVM `jcmd` and py-spy, `/statusz`, the DoS
warning, cardinality advice and the 2 minute target, none stated on those pages.
Method: documentation only; no commands were run.
