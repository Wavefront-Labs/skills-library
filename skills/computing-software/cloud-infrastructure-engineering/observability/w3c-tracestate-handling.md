---
id: computing-software.cloud-infrastructure-engineering.observability.w3c-tracestate-handling
name: w3c-tracestate-handling
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [tracestate, w3c-trace-context, context-propagation, consistent-probability-sampling, traceparent]
level: advanced
status: docs-checked
description: "Handle the W3C tracestate header: format and limits, vendor entries, the OpenTelemetry ot= entry for sampling thresholds, and proxy/gateway pitfalls."
sources: ["https://www.w3.org/TR/trace-context/#tracestate-header", "https://opentelemetry.io/docs/specs/otel/trace/tracestate-handling/", "https://opentelemetry.io/docs/specs/otel/trace/tracestate-probability-sampling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tracestate handling

`traceparent` carries trace id, span id and flags; `tracestate` carries vendor-specific data alongside it.

## Format (W3C)
`tracestate: vendor1=value1,vendor2=value2`
- Up to 32 list members; keys start with a lowercase letter or digit and may contain `a-z 0-9 _ - * / @` (up to 256 characters), so a `tenant@vendor` form is possible; values are up to 256 printable ASCII characters, excluding comma and `=`.
- A vendor that modifies an entry moves it to the beginning (left); unmodified entries keep their order, and a key must not appear twice. Vendors MUST send the received `tracestate` on outgoing requests (they may mutate it).
- Vendors SHOULD propagate at least 512 characters. If truncating, remove whole entries: entries longer than 128 characters first, then entries from the end.
- Deleting a key you did not create SHOULD be avoided, because it breaks correlation in other systems.

## OpenTelemetry entry `ot`
OTel values live in a single `ot` entry, a semicolon-separated list of `key:value` pairs, e.g. `ot=th:8;rv:9b8233f7e3a151`. The whole `ot` value must not exceed 256 characters:
- `th`: rejection threshold, 1 to 14 lowercase hex digits (trailing zeros may be omitted; `th:0` is 100% sampling, `th:c` is 25% sampling).
- `rv`: explicit randomness value, exactly 14 lowercase hex digits (56 bits), used instead of the low 56 bits of the trace ID.

## Where it matters
- `tracestate` entries are opaque, vendor-specific data; dropping them loses what those vendors stored.
- Consistent probability sampling across services, and adjusted counts for span metrics, depend on `ot=th` (and `rv` when present).

## Pitfalls
- Proxies, gateways or API frameworks that forward `traceparent` but strip unknown headers drop `tracestate`.
- Custom code that builds outgoing headers by hand often forgets it; use the propagator's `inject`.
- Keep your own entries short: W3C only asks vendors to propagate at least 512 characters of the combined header.

## Verify
- [ ] An end-to-end request shows the same tracestate entries (plus updated own entry) at every hop when logged in debug mode.

## Checked

2026-10-24. W3C Trace Context spec source (20-http_request_header_format.md) and OpenTelemetry specification trace/tracestate-handling.md and tracestate-probability-sampling.md (main branch). Confirmed: 32 list members, key and value grammar and limits, mutation and ordering rules, 512-character propagation and truncation order, `ot` entry format and 256-character limit, `th` and `rv` encodings, and the 25% example (`th:c`). Removed vendor-product claims.

Method: documentation only; no commands were run.
