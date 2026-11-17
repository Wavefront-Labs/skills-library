---
id: computing-software.cloud-infrastructure-engineering.observability.otel-exception-semantic-conventions
name: otel-exception-semantic-conventions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, exception-semconv, exception-attributes, record-exception, span-status, error-handling]
level: practitioner
status: docs-checked
description: "Record exceptions per OpenTelemetry semconv: exception attributes, span status, error.type, logs versus deprecated span events, migration opt-in and no duplicates."
sources: ["https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-spans/", "https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs/", "https://opentelemetry.io/docs/specs/otel/trace/api/#set-status", "https://opentelemetry.io/docs/specs/semconv/general/recording-errors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception semantic conventions

**Goal:** record errors so backends group, count and link them to traces consistently.

## Attributes
| Attribute | Notes |
|---|---|
| `exception.type` | Fully qualified type name; prefer the dynamic type. May record the inner type of a useless wrapper (for example Go errors wrapped with `%w`). Required if `exception.message` is absent. |
| `exception.message` | May contain sensitive information. Required if `exception.type` is absent. |
| `exception.stacktrace` | Recommended; string in the language's natural format (for example Python `traceback.format_exc()`, Java `Throwable.printStackTrace()`). |
| `exception.escaped` | Deprecated. Recording handled exceptions that do not escape a span is no longer recommended. |

## Span events versus logs
- The page for exceptions on spans is marked deprecated: the event named `exception` (stable) still exists, but the guidance is to record exceptions as log records through the Logger API, associated with the span context when a span exists.
- Migration: instrumentations add `OTEL_SEMCONV_EXCEPTION_SIGNAL_OPT_IN` with `logs` (logs only) or `logs/dup` (both, for phased rollout). Unset keeps span events. Users can route exception logs to span events at the SDK layer.
- Log event names (development status) describe the operation and end in `.exception`, for example `http.client.request.exception`; generic handlers use `exception`. Set severity number: ERROR 17 for unhandled, WARN 13 for expected-to-handle (timeouts, I/O), DEBUG 5 for non-problems such as a cancelled client request.

## Span status and error.type
- Leave status Unset when the operation succeeds. On failure set status Error and set `error.type`. Add a description only with Error; for exceptions use the exception message, and avoid repeating the status code or `error.type`.
- Status ordering is Ok > Error > Unset. Only developers or operators should set Ok; instrumentation libraries should not unless configured to.
- RecordException is a specialised AddEvent. The spec section does not say it sets the status, so set the status yourself.
- Put `error.type` on the operation duration histogram on failure, and omit it on success. Span and metric for one operation carry the same value.

## Duplicates and handled errors
- Errors that were retried or handled so the operation completed should not be recorded on that operation's spans or metrics.
- Record an exception once, when it reaches the caller. Do not record exceptions the instrumented library handles, nor artificial framework exceptions such as FastAPI HTTPException or Spring ResponseStatusException where avoidable.

## Verify
- [ ] A failed request has one exception record (log or event) with type, message and stack, and span status Error
- [ ] The duration metric splits by `error.type`
- [ ] Handled and retried errors leave the span status unset

## Checked

2026-11-08. Confirmed on all four pages: attribute requirement levels, stacktrace formats, deprecation of the span-event page, the OPT_IN values, log event naming and severity numbers, status rules and ordering, RecordException wording, recording-errors guidance on error.type, metrics, retried errors and recording once. Removed or changed: per-language record code samples (not in the spec pages), the claim that error.type applies to HTTP status strings (not stated), and the earlier advice to record exceptions as span events by default. The 404 client-side example was reworded to the page's context-dependent statement.
Method: documentation only; no commands were run.
