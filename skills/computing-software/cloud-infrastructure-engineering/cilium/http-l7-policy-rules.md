---
id: computing-software.cloud-infrastructure-engineering.cilium.http-l7-policy-rules
name: http-l7-policy-rules
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, http-policy, path, method, host, headers, layer7]
level: practitioner
status: docs-checked
description: "Write Cilium HTTP L7 allow rules matching path, method, host and headers with extended POSIX regex, plus the docs GET /public example behaviour."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP L7 rules

Match fields (all optional, omitted means allow):
- `path`: extended POSIX regex, must begin with `/`.
- `method`: extended POSIX regex, e.g. GET, POST, PUT, PATCH, DELETE.
- `host`: extended POSIX regex against the Host header, e.g. `foo.com`.
- `headers`: headers that must be present. `headerMatches` additionally matches header values; a `mismatch` field says what to do on no match.

Docs examples:
- `env=prod` to `app=service`: allow `GET /public` only; other URLs or methods are rejected; requests on ports other than 80 are dropped.
- `app=myService` receives only on TCP 80, and the only API calls are `GET /path1` and `PUT /path2` with header `X-My-Header` set to `true`.

Because paths are regexes, anchor or escape intentionally; the page does not state implicit anchoring, so test with real requests.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/layer7/. 

Method: documentation only; no commands were run.
