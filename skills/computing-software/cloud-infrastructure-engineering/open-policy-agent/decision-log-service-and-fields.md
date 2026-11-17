---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.decision-log-service-and-fields
name: decision-log-service-and-fields
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [decision-logs, audit, upload-size-limit-bytes, decision-id, console-logging]
level: practitioner
status: docs-checked
description: "Enable OPA decision logs to the console or a remote service, the gzip JSON upload contract, key event fields, retry on non-2xx, and upload_size_limit_bytes."
sources:
  - https://www.openpolicyagent.org/docs/management-decision-logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: record every policy decision for audit and offline debugging.

Quickest option, no server needed:

```yaml
decision_logs:
  console: true
```

This dumps all decisions to the console. With decision logging on, API calls that return decisions include a `decision_id` field.

Remote service: OPA POSTs to `/logs` by default, or to the path set in `decision_logs.resource`, with `Content-Encoding: gzip` and `Content-Type: application/json`. The body is a gzip-compressed JSON array, one element per decision.

Useful event fields:
- `decision_id`, plus `trace_id` and `span_id` (W3C trace-context hex strings)
- `labels`: key-value pairs identifying the OPA instance
- `bundles[_].revision`: bundle revision that produced the decision
- `path` (for example `http/example/authz/allow`), `input`, `result`, `requested_by`, `timestamp`
- `query` for ad-hoc Query API calls, `metrics` when requested
- `erased` and `masked`: JSON Pointers removed or changed (see decision-log-masking-policy)

Your receiver must answer 2xx. On any non-2xx OPA requeues the last chunk for the next upload and applies exponential backoff.

`upload_size_limit_bytes` bounds the gzip-compressed message size. OPA adapts an uncompressed limit: it scales up when chunks are under 90 percent of the limit, scales down and re-encodes when over, and holds between 90 and 100 percent, so early chunks are smaller. If an event with `nd_builtin_cache` will not fit, OPA drops that key and retries.

Check: enable `console: true`, query a policy, and confirm a log line with a matching `decision_id`.

## Checked

2026-11-04. Confirmed against the OPA docs Decision Logs page: console option, decision_id in API responses, POST to /logs or decision_logs.resource with gzip and application/json, the event field table (labels, decision_id, trace_id, span_id, bundles, path, query, input, result, requested_by, timestamp, metrics, erased, masked), non-2xx requeue with exponential backoff, and the upload_size_limit_bytes adaptive limit (90 percent scale-up threshold, scale-down with re-encode, equilibrium, dropping nd_builtin_cache). Nothing removed.

Method: documentation only; no commands were run.
