---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.basic-auth-setup
name: basic-auth-setup
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, basic-auth, authentication, consumer, credential, plugin]
level: intro
status: docs-checked
description: "Enable basic-auth on an APISIX route: consumer credential fields, hide_credentials, anonymous_consumer, realm, forwarded headers and the two 401 messages."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/basic-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# basic-auth setup

Consumer credential attributes (both required):
- `username`: unique per consumer.
- `password`: stored AES-encrypted in etcd; may be an `env://` or `secret://` reference.

Route attributes:
- `hide_credentials`: false; true drops the `Authorization` header before the upstream.
- `anonymous_consumer`: consumer name that bypasses authentication.
- `realm`: `basic` (APISIX 3.15.0+), used in the `WWW-Authenticate` header on 401.

Enable on a route with `"basic-auth":{}` and add the credential to a consumer (for example `johndoe`).

Tests:
- `curl -i "http://127.0.0.1:9080/anything" -u johndoe:<PASSWORD>` returns 200.
- Wrong password: 401 `{"message":"Invalid user authorization"}`.
- No credentials: 401 `{"message":"Missing authorization in request"}`.
- A pre-encoded `Authorization: Basic <base64>` header works too.

The upstream receives `X-Consumer-Username` and `X-Credential-Identifier`. A consumer `custom_id` label adds `X-Consumer-Custom-Id`.

An anonymous consumer can carry a stricter plugin such as `limit-count`; in the page's test, five requests gave 200 x3 and 429 x2 for the authenticated consumer, and 200 x1 and 429 x4 for anonymous.

## Checked

2026-11-04. Confirmed against the APISIX basic-auth plugin page: credential attributes and AES storage, env:// and secret:// references, hide_credentials, anonymous_consumer, realm default and its 3.15.0 gate, both 401 messages, the custom id header, the 3/2 and 1/4 limit-count results. Nothing removed.

Method: documentation only; no commands were run.
