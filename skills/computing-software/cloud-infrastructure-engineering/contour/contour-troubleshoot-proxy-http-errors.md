---
id: computing-software.cloud-infrastructure-engineering.contour.contour-troubleshoot-proxy-http-errors
name: contour-troubleshoot-proxy-http-errors
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [troubleshooting, 503, response-flags, uf, uh, nr, access-log, envoy-metrics, server-envoy]
level: practitioner
status: docs-checked
description: "Diagnosing unexpected HTTP errors through Contour and Envoy: server header check, access log response flags UF/UH/NR, duration and upstream time, Envoy stats, bypassing the proxy."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/troubleshooting/common-proxy-errors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting common proxy errors

Work through these steps:

1. Inspect the response with `curl -vvv`. A `server: envoy` header means the request reached Envoy, ruling out earlier proxies; then decide whether the body is from Envoy (for example `upstream connect error or disconnect/reset before headers. reset reason: connection failure`) or from the app.

2. Read the Envoy access log for that request. Default-format fields to check: method, `X-ENVOY-ORIGINAL-PATH`/path, `:AUTHORITY`, `%PROTOCOL%`, and:
   - `%RESPONSE_FLAGS%`: `UF` Envoy could not connect to the upstream; `UH` the Service has no healthy or ready pods; `NR` no configured route matches.
   - `%DURATION%` versus configured timeouts (a duration near 1998 ms with `UF` matches the 2s default connect timeout).
   - `%RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)%`: `-` means the request was never forwarded.
   - `%UPSTREAM_HOST%`: the exact pod IP selected.

3. For high-volume systems use Envoy metrics from `/stats/prometheus` on the admin interface:
   - listener: `downstream_cx_total`, `ssl.connection_error`.
   - HTTP: `downstream_cx_protocol_error`, `downstream_rq_rx_reset`, `downstream_rq_tx_reset`, `downstream_rq_timeout`, `downstream_rq_5xx`.
   - upstream: `upstream_cx_connect_fail`, `upstream_cx_connect_timeout`, `upstream_rq_timeout`.

4. Port-forward directly to the backend app. If that works, the fault is Contour configuration or Envoy rather than the application.

## Checked

2026-11-04. Confirmed against the Contour common proxy errors page (troubleshooting/common-proxy-errors.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
