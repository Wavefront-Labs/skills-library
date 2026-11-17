---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-troubleshooting-missing-spans
name: jaeger-troubleshooting-missing-spans
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, missing-spans, otel-traces-sampler, network-connectivity, bypass-collectors]
level: practitioner
status: docs-checked
description: "Work through the documented checklist when no spans appear: sampling, bypassing intermediaries, networking, logs and metrics."
sources:
  - https://www.jaegertracing.io/docs/2.22/operations/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find why spans do not reach Jaeger.

1. Verify sampling first. Sample every trace while diagnosing. OpenTelemetry SDKs default to `parentbased_always_on`; change with `OTEL_TRACES_SAMPLER`. Use the SDK's stdout exporter to confirm spans are actually recorded.
2. Remote sampling: confirm the SDK uses it, points to the correct address and that address is reachable; check the strategy with `curl "jaeger-collector:14268/api/sampling?service=foobar"`.
3. Bypass intermediate collectors (such as an OpenTelemetry Collector host agent): send directly to Jaeger to narrow the problem.
4. Network connectivity. Typical container mistakes: not exposing the right ports (the collector listens on :4317 inside the container but it is not reachable outside), using localhost as the host name for server endpoints (use 0.0.0.0 in containers), and not making Jaeger's host name visible to the application's network namespace (for Docker, same network or the `--link` option).
5. Raise log verbosity to debug.
6. Check `/metrics`: `curl -s http://jaeger-collector:8888/metrics`. `otelcol_receiver_accepted_spans` should rise when traces are received, and `otelcol_exporter_sent_spans` should rise at the same rate when storage writes succeed.
7. Service mesh: if mesh-generated spans are missing, use the mesh's own troubleshooting guide, for example Istio's.

## Checked

2026-11-03. Confirmed against the Troubleshooting page: the parentbased_always_on default and OTEL_TRACES_SAMPLER, the sampling curl check, bypassing intermediate collectors, the container networking mistakes (ports, localhost versus 0.0.0.0, --link), debug logs, the /metrics counters and the service mesh note. Nothing removed.
Method: documentation only; no commands were run.
