---
id: computing-software.qa-testing-engineering.exploratory-testing.server-logs-and-traces-for-bug-evidence
name: server-logs-and-traces-for-bug-evidence
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [log-analysis-for-testers, bug-investigation, distributed-tracing, correlation-id, observability]
level: practitioner
status: docs-checked
description: "Find bug evidence in server logs and traces as a tester: W3C traceparent ids, LogQL line filters and parsers, KQL field queries and quoting evidence."
sources:
  - https://grafana.com/docs/loki/latest/query/
  - https://www.elastic.co/docs/explore-analyze/query-filter/languages/kql
  - https://www.w3.org/TR/trace-context/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading server logs and traces for bug evidence

**Goal:** connect a symptom in the UI to what happened on the server, so the report points at the cause.

## Get the correlation key
- W3C Trace Context defines the `traceparent` HTTP header, which identifies the incoming request in a tracing system: `traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01`. Its fields are version, trace-id (32 lowercase hex, 16 bytes, not all zeros), parent-id and trace-flags. `tracestate` carries optional vendor-specific data.
- The sampled flag (the only flag in version 00) tells downstream components that the caller marked the request for recording. A trace may therefore not exist for every request.
- Error pages often show a reference id; otherwise note the exact timestamp (UTC), user and endpoint.
- Whether your system emits `traceparent` or another id header is a question for the team; the cited pages only define `traceparent`.

## Query examples
Grafana Loki (LogQL): a query is `{ log stream selector } | log pipeline`. The selector is mandatory and uses labels with `=`, `!=`, `=~`, `!~`; Loki indexes only the timestamp and labels, not the line content. Line filters: `|=` contains, `!=` does not contain, `|~` regex match, `!~` regex no match. Parsers include json, logfmt, pattern, regexp and unpack; label filters use `==`, `!=`, `>`, `>=`, `<`, `<=` with `and` and `or`.
```
{service_name="checkout"} |= "0af7651916cd43dd8448eb211c80319c" | json | level="error"
```
(Here `service_name` is Loki's default label; the `level` field depends on your log format.)

Kibana (KQL): a condition is field, operator and value; KQL only filters, it does not aggregate or sort.
```
http.response.status_code: (400 OR 401 OR 404)
response: 200 OR extension: php
```
Substitute your own field names for the page's examples.

## What to look for
- First error in time, not the loudest; later errors are often consequences.
- Warnings just before the failure (timeouts, retries, validation messages).
- Whether the error is new after the deploy: compare with the release timestamp.

## Report it
Quote the key log lines with timestamps and the trace id; link the saved query rather than pasting thousands of lines. Remove personal data and secrets.

## Gotchas
- Time zones: UI in local time, logs in UTC.
- Sampling: the sampled flag means not every request is recorded.
- Log levels in test environments may hide debug detail; ask for a temporary increase.

## Verify
The defect report links the log query or trace id for the exact failing request and names the failing service and first error.

## Checked
2026-11-09: checked against the Loki LogQL overview (query structure, selector, filter, parser and format sections), the Kibana KQL overview (read in full; the KQL source URL was updated to its current location) and the W3C Trace Context spec (overview, traceparent format and sampled flag; the sections on tracestate details and privacy were not read). Removed because the pages do not state them: `x-request-id` and `x-amzn-trace-id` headers, the `count_over_time` metric query, the `trace.id` and `log.level` KQL fields, CloudWatch Logs Insights, `kubectl logs`, Jaeger, Tempo and Datadog advice, and the forcing-sampling tip.

Method: documentation only; no commands were run.
