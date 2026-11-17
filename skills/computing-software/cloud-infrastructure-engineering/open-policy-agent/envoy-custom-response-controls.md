---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.envoy-custom-response-controls
name: envoy-custom-response-controls
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [envoy, ext-authz, response-headers, status-code, dynamic-metadata]
level: advanced
status: docs-checked
description: "Return more than a boolean from an Envoy ext-authz policy: headers, response_headers_to_add, request_headers_to_remove, body, status_code, dynamic_metadata and query parameters."
sources:
  - https://www.openpolicyagent.org/docs/envoy/primer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control the HTTP reply or the upstream request from the policy decision.

The boolean `allow` is the minimal result. Alongside it, the policy can produce an object with these fields:
- `headers`: string keys and string values. On deny it is the set of HTTP response headers sent to the downstream client; on allow the docs say it is the set of additional request headers sent to the upstream.
- `response_headers_to_add`: string-to-string object of response headers sent downstream when the request is allowed.
- `request_headers_to_remove`: array of header names removed from the original request before it goes upstream, when allowed.
- `body`: string response body sent downstream when the request is denied.
- `status_code`: number, the HTTP status sent downstream when the request is denied.
- `dynamic_metadata`: object with string keys and values that may be booleans, strings, numbers, arrays or objects; it sets `DynamicMetadata` in the `CheckResponse` for consumption by other Envoy filters.
- `query_parameters_to_set`: object whose values are strings or arrays of strings, adding or modifying query parameters on the request dispatched upstream.

Pattern: keep the decision in `allow`, and define these variables alongside it in the same `envoy.authz` package. The docs then show a `result` object that assembles them with partial object rules so undefined variables leave no key. In that output document the status key is named `http_status` (the rule variable is `status_code`), the decision key is `allowed`, and there is also an optional `query_parameters_to_remove` array.

Design guidance:
- Tie `status_code` and `body` to the reason a request failed (the docs example returns 401 when the token is invalid and 403 otherwise) rather than a single message.
- Put request mutations (`request_headers_to_remove`, `query_parameters_to_set`) only on allowed paths, since they apply when the request goes upstream.

Check: send a denied request and confirm the client sees your `status_code`, `body` and `headers`; send an allowed one and confirm `response_headers_to_add` appears.

## Checked

2026-11-04. Confirmed against the OPA docs Envoy page Policy Primer via Examples, section Example Policy with Additional Controls and Output Document: the field types and the allow versus deny behaviour of headers, response_headers_to_add, request_headers_to_remove, body, status_code, dynamic_metadata and query_parameters_to_set. Corrected the allowed-case meaning of headers, removed the unsupported advice to add a default, and noted that the page names the same value status_code in the rules but http_status in the output document (the page is inconsistent between those two sections).

Method: documentation only; no commands were run.
