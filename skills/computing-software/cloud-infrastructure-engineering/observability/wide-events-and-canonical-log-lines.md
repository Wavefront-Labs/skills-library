---
id: computing-software.cloud-infrastructure-engineering.observability.wide-events-and-canonical-log-lines
name: wide-events-and-canonical-log-lines
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [canonical-log-line, wide-event-design, structured-logging, high-cardinality, telemetry-signals]
level: advanced
status: docs-checked
description: "Design wide events / canonical log lines: one rich structured record per request per service, emitted in a finally block, with stable schema, streaming and sampling."
sources: ["https://stripe.com/blog/canonical-log-lines", "https://opentelemetry.io/docs/concepts/signals/", "https://charity.wtf/2019/02/05/logs-vs-structured-events/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wide events and canonical log lines

Stripe's canonical log line and Honeycomb-style wide events are the same idea: in addition to normal logs, each unit of work emits one long, information-dense structured record at the end, collecting its key telemetry. Charity Majors' formulation: arbitrarily wide structured events describing the request and its context, one event per request per service.

## What goes in (Stripe's list, plus the wide-event advice)
- HTTP method, path and status; request ID and team or tenant identifiers.
- Authenticated user, how they authenticated, API key ID.
- Rate limiter result: allowed or not, quota, remaining allowance.
- Timing: total duration and time in database queries; number of database queries; objects allocated by the VM.
- High-cardinality context: unique IDs, headers, full and normalised queries, timings of outbound calls.

## Emitting
- Create the event when the request enters, add context throughout, write it when the request exits or errors.
- Stripe does it in middleware, with other modules adding to the request environment, and logs in an `ensure` block so a line is emitted even when an exception unwinds the stack. The logging code has its own begin/rescue so a logging failure never fails a request, and engineers are notified when it does.

## Rules
- One event per request per service; keep the field names stable. Stripe defines the schema as a protocol buffer.
- Log levels are called obsolete by Majors. Keep raw events, not pre-aggregates, so percentiles and breakdowns stay accurate.
- Stream events to a remote service rather than local disk; sample, ideally dynamically, to control cost.
- Keep secrets and personal data out (your data policy; not discussed on the pages).

## Querying and storage
Everything in one line makes questions easier and faster: counting rate-limited requests by user shows whether limiting comes from a few users or many, and filtering by user, endpoint and non-4xx statuses graphs latency percentiles. Stripe sends serialised lines asynchronously to Kafka, batches them into S3 and loads Presto and Redshift. Canonical lines are less quick to reference than metrics but flexible and cheap to aggregate.

## OpenTelemetry context
OpenTelemetry lists traces, metrics, logs and baggage as supported signals, with events (a type of log) and profiles in development or proposal.

## Verify
- [ ] A slow request found in a metric can be located as a single event by request ID
- [ ] Failures still emit the event

## Checked

2026-11-08. Confirmed from the Stripe post (fields, ensure block, schema, pipeline, querying), Majors' post (one event per request per service, raw data, high cardinality, streaming, sampling, levels) and the OpenTelemetry signals page. Removed as not on the pages: the claim that an OTel span is a wide event, ClickHouse/BigQuery/Loki storage advice and the LogQL queries, the sample_rate field, the 50 to 300 field count, flat-typed-fields rule, and the Go snippet.
Method: documentation only; no commands were run.
