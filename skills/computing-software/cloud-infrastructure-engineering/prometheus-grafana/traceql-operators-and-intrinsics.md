---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.traceql-operators-and-intrinsics
name: traceql-operators-and-intrinsics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [traceql-comparison-operators, traceql-regex, traceql-intrinsics, root-service-name, traceql, tempo]
level: practitioner
status: verified
description: "Use TraceQL comparison, regex and existence operators with intrinsics (name, status, kind, duration, rootServiceName, traceDuration) and typed attribute values."
sources: ["https://grafana.com/docs/tempo/latest/traceql/construct-traceql-queries/", "https://grafana.com/docs/tempo/latest/traceql/", "https://grafana.com/docs/tempo/latest/traceql/metrics-queries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TraceQL operators and intrinsics

## Intrinsics (fields every span/trace has)
| Intrinsic | Scope syntax (newer) | Example |
|---|---|---|
| `name` | `span:name` | `{ name = "GET /api/orders" }` |
| `status` (`ok`, `error`, `unset`) | `span:status` | `{ status = error }` |
| `statusMessage` | `span:statusMessage` | `{ statusMessage =~ ".*timeout.*" }` |
| `kind` (`server`, `client`, `producer`, `consumer`, `internal`) | `span:kind` | `{ kind = server }` |
| `duration` | `span:duration` | `{ duration > 2s }` |
| `rootServiceName`, `rootName`, `traceDuration` | `trace:rootService`, `trace:rootName`, `trace:duration` | `{ trace:duration > 10s }` |
| event/link/instrumentation scopes | `event:name`, `link:traceID`, `instrumentation:name` | `{ event:name = "exception" }` |

## Operators
- Comparison: `=`, `!=`, `>`, `>=`, `<`, `<=`.
- Regex: `=~`, `!~` (Go RE2 syntax), **fully anchored**: `{ name =~ "HTTP" }` matched nothing while `{ name =~ "HTTP.*" }` matched (the Tempo docs say an unanchored `"bar"` is treated as `"^bar$"`).
- Existence: `{ span.http.route != nil }` (attribute present), `= nil` absent.
- Boolean within a span: `&&`, `||`; across spansets: `{ A } && { B }` (same trace has both), `{ A } || { B }`.
- Typed values: strings in quotes, numbers, durations (`300ms`), booleans, status/kind keywords without quotes.
- `instrumentation:name` (colon) is the intrinsic and matched; `instrumentation.name` (dot) looks up a scope attribute called `name` and matched nothing.
- Comments such as `# note` are not part of TraceQL: a query ending in `# comment` returns a parse error, so strip the annotations used in examples.

```traceql
{ resource.service.name = "api" && kind = server && span.http.response.status_code >= 500 }
{ rootServiceName = "frontend" } && { resource.service.name = "payments" && status = error }
{ span.http.route =~ "/api/v1/orders/.*" && duration > 1s }
```

## Gotchas
- Status keyword vs attribute: `status = error` is the span status, not an HTTP code.
- Comparing an int attribute to a string (`= "500"`) matches nothing; match the stored type.
- Regex across all spans of large time ranges is slow; filter by service first (regexes are already anchored).

## Verify
- [ ] Queries return expected spans in Explore; type mismatches identified by checking a span's attribute types in the trace view.

## Checked
Ran Tempo 3.1.1 (windows-amd64, single binary, local backend, OTLP/HTTP receiver) and pushed 12 synthetic traces through `/v1/traces` (frontend root span, payments child with an `exception` event on 4 error traces, checkout database spans, instrumentation scope names, int and string attributes), then queried `/api/search`, `/api/metrics/query_range` and `tempo-cli` 3.1.1. Verified by running: `span:name`, `span:status`, `span:statusMessage`, `span:kind`, `span:duration`, `trace:duration`, `trace:rootService`, `trace:rootName` and the older `rootServiceName`, `rootName`, `traceDuration` forms, `event:name`, `event.exception.type`, `link:traceID` (syntax only, no links in the data), `instrumentation:name`, existence (`!= nil`, `= nil`), regex anchoring, `&&`/`||` between spansets, the int-versus-string mismatch (`= "500"` matched nothing, `>= 500` matched 4 spans) and the three example queries. Docs read: Tempo traceql/construct-traceql-queries (intrinsics table, anchored regex) at tag v3.1.1.
