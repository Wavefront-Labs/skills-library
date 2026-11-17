---
id: computing-software.networking-hardware-and-wireless.caddy.tracing-opentelemetry
name: tracing-opentelemetry
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [tracing, opentelemetry, otlp, trace-id, span-attributes, w3c-tracecontext, caddyfile]
level: practitioner
status: docs-checked
description: "Enable OpenTelemetry tracing in Caddy with the tracing directive: span names and attributes, trace IDs in logs and headers, OTEL environment variables."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/tracing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: emit distributed traces for selected routes.

The directive integrates with opentelemetry-go. It propagates an existing trace context or starts a new one, exports using gRPC, and uses W3C tracecontext and baggage propagators. The trace and span IDs appear in access logs as `traceID` and `spanID`, and as the placeholders `{http.vars.trace_id}` and `{http.vars.span_id}`, which you can forward, for example `request_header X-Trace-Id {http.vars.trace_id}`.

Syntax: `tracing { span <span_name>  span_attributes { <attr> <value> ... } }`. Many span attributes are set by default per OpenTelemetry's HTTP span semantic conventions (request, response and client details). Placeholders can be used in names and attributes, but the span name is set before the request is forwarded, so only request placeholders work in it; every placeholder works in attributes.

Exporter configuration comes from the standard OpenTelemetry SDK environment variables, not the Caddyfile. The page's examples: `export OTEL_EXPORTER_OTLP_HEADERS="myAuthHeader=myToken,anotherHeader=value"` and `export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=https://my-otlp-endpoint:55680`.

Example: in `handle /api*` use `tracing { span api }` then `reverse_proxy localhost:8081`; in the fallback `handle` use `tracing { span app  span_attributes { user_id {http.request.cookie.user-id} } }`. Using separate spans per branch makes traces distinguish API and app traffic.

## Checked

2026-11-03: read caddyfile/directives/tracing against this skill. Confirmed: opentelemetry-go integration, gRPC exporter, W3C tracecontext and baggage, traceID/spanID log fields and placeholders, span and span_attributes syntax, placeholder timing rule, OTEL environment variables, examples.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
