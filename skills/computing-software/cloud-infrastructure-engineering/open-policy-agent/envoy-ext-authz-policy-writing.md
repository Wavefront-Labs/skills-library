---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.envoy-ext-authz-policy-writing
name: envoy-ext-authz-policy-writing
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [envoy, ext-authz, jwt, authorization, envoy-authz-allow]
level: advanced
status: docs-checked
description: "Write a Rego policy for Envoy's External Authorization filter: package envoy.authz, default allow false, JWT checks with io.jwt.decode_verify and glob path matching."
sources:
  - https://www.openpolicyagent.org/docs/envoy/primer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authorise HTTP requests that Envoy forwards to OPA through its External Authorization filter.

Request data arrives under `input.attributes.request.http` (`method`, `path`, `headers`). Start every policy with the safe default and decompose the decision:

```rego
package envoy.authz

import input.attributes.request.http

default allow := false

allow if {
    is_token_valid
    action_allowed
}

is_token_valid if {
    token.valid
    now := time.now_ns() / 1000000000
    token.payload.nbf <= now
    now < token.payload.exp
}

action_allowed if {
    http.method == "GET"
    token.payload.role == "admin"
    glob.match("/people/*", ["/"], http.path)
}

token := {"valid": valid, "payload": payload} if {
    [_, encoded] := split(http.headers.authorization, " ")
    [valid, _, payload] := io.jwt.decode_verify(encoded, {"secret": "secret"})
}
```

Notes:
- With no `path` set in the OPA-Envoy configuration, the decision path defaults to `envoy/authz/allow`, so `data.envoy.authz.allow` is queried.
- `io.jwt.decode_verify` verifies and parses the JWT; the example's literal `"secret"` is for illustration, so load real keys from data or a bundle.
- Dot access never throws; a missing path yields `undefined`, which with the default becomes deny.
- Parsed request bodies are available as `input.parsed_body`, for example `lower(input.parsed_body.firstname)`.
- OPA has over 150 built-ins listed in the policy reference.

For richer replies (status, headers, body) see envoy-custom-response-controls.

Check: evaluate with a sample `input` JSON using `opa eval` and confirm an expired token (`exp` in the past) yields false.

## Checked

2026-11-04. Confirmed against the OPA docs Envoy page Policy Primer via Examples: package envoy.authz, import input.attributes.request.http, default allow := false, the token and time checks with io.jwt.decode_verify, glob.match path matching, default decision path envoy/authz/allow, dot access never throwing, 150+ built-ins, and input.parsed_body. The skill trims the docs' three action_allowed rules to one admin rule as an illustration. Nothing removed.

Method: documentation only; no commands were run.
