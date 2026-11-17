---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.data-api-policy-queries
name: data-api-policy-queries
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rest-api, data-api, v1-data, input-document, decision-id]
level: practitioner
status: docs-checked
description: "Query an OPA policy decision through POST /v1/data with an input document, query parameters such as explain and strict-builtin-errors, status codes and undefined results."
sources:
  - https://www.openpolicyagent.org/docs/rest-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ask a running OPA server for a decision.

```
POST /v1/data/opa/examples/allow_request HTTP/1.1
Content-Type: application/json

{"input": {"example": {"flag": true}}}
```

The path after `/v1/data/` is the package and rule, with `/` for `.`. The body wraps your input under the key `input`. Headers: `Content-Type` is `application/json` or `application/yaml`; `Content-Encoding: gzip` and `Accept-Encoding: gzip` are supported.

Query parameters:
- `pretty=true` human-formatted output
- `explain` with `notes`, `fails`, `full` or `debug`
- `metrics` and `instrument` for performance metrics (`instrument` returns a superset)
- `provenance=true` adds build and version information
- `strict-builtin-errors` treats built-in call errors as fatal and returns immediately
- `rule_labels=true` includes merged `# METADATA` labels of evaluated rules

Response fields: `result` (the document; omitted when the path is undefined), `metrics`, and `decision_id` when decision logging is on, which you can use to correlate with the decision log.

Status codes: 200 for success, 400 for a bad request such as malformed input JSON, 500 for a server error. An undefined document returns 200 without a `result`, so clients should handle a missing `result` explicitly, for example by treating it as deny, or define `default allow := false`.

Extra top-level body keys beyond `input` are request metadata, readable by custom builtins and logged under `custom.request_metadata`. Namespace such keys, for example `com.example.opa/metadata`, because future versions may add top-level keys.

Check: query a path with a false and a true input and an undefined path, and confirm the third response has no `result`.

## Checked

2026-11-04. Confirmed against the OPA docs REST API page, Get a Document with Input: request body shape, Content-Type, Content-Encoding and Accept-Encoding headers, query parameters (pretty, provenance, explain values, metrics, instrument, strict-builtin-errors, rule_labels), 200/400/500 status codes, undefined path returning 200 without result, decision_id, and request metadata (custom.request_metadata, namespaced key advice). Reworded the undefined-result advice as guidance rather than a documented requirement.

Method: documentation only; no commands were run.
