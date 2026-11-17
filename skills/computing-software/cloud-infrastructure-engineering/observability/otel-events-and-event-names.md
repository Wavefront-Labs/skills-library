---
id: computing-software.cloud-infrastructure-engineering.observability.otel-events-and-event-names
name: otel-events-and-event-names
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [events-api, otel-events, otel-logs, event-name, log-events]
level: advanced
status: docs-checked
description: "OpenTelemetry events: log records with an EventName, when to use events versus spans or plain logs, naming rules, severity, attributes and body, and Logger emit/Enabled."
sources: ["https://opentelemetry.io/docs/specs/otel/logs/data-model/#field-eventname", "https://opentelemetry.io/docs/specs/semconv/general/events/", "https://opentelemetry.io/docs/specs/otel/logs/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTel events

An event is a LogRecord with a non-empty EventName (an optional string). EventName identifies the class of the event and should identify its structure, covering both attributes and body. Events are OpenTelemetry's standardised format for LogRecords, and semantic conventions for logs should be formatted as events. Not every LogRecord has to be an event. The events semantic convention page is in Development status.

## When to use
Events mark named occurrences at a point in time: checkpoints, state changes, outcomes within long or asynchronous operations, lifecycle moments like startup and shutdown. They need no trace context of their own and can be emitted inside or outside a trace. Use spans for operations with duration, span attributes for properties of a whole operation, plain log records for unstructured diagnostics.

## Emitting
Events go through the Logger emit operation with the optional Event Name parameter. Emit accepts Timestamp, Observed Timestamp, Context (defaults to the current Context with implicit support), Severity Number, Severity Text, Body, Attributes, Event Name, and may accept an Exception. A Logger should offer Enabled(Context, Severity Number, Event Name) so callers can skip building expensive records; the result can change over time, so cached values may go stale. An ergonomic API for events is in Development status.

## Naming
Names must uniquely identify the structure, follow the general naming guidelines, be fully qualified and domain-specific, and must not contain dynamic values; put identifiers and values in attributes.

## Fields
- Timestamp is when the occurrence happened; conventions must not set ObservedTimestamp.
- Conventions give a default severity number from expected impact and document context-dependent conditions; they must not define severity text.
- SeverityNumber ranges: 1-4 TRACE, 5-8 DEBUG, 9-12 INFO, 13-16 WARN, 17-20 ERROR, 21-24 FATAL. 17 or higher indicates an erroneous situation.
- Reuse existing attributes, prefer flat ones, include `error.type` for failures, document sensitive or large attributes, and do not copy every span attribute onto the event.
- Conventions must not define a body, except a string display message. Exception details follow the exception-in-logs conventions.

## Verify
- [ ] The event name is constant across occurrences and documented with its attributes
- [ ] Failure events carry `error.type`
- [ ] The record carries the current trace context when emitted inside a span

## Checked

2026-11-08. Confirmed on all three pages: EventName definition, semantic-convention event guidance, severity table, attribute and body rules, Logger emit parameters, Enabled, ergonomic API status. Removed as not on those pages: the Python and Java snippets, the history of the deprecated Events API, example semconv events (gen_ai, feature_flag, device.app.lifecycle), past-tense naming and Weaver registry advice, the claim about span events being dropped under sampling, and Loki/Elastic field names.
Method: documentation only; no commands were run.
