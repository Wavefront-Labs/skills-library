---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.upstream-hash-on
name: upstream-hash-on
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, hash-on, hash-fallback, sticky-sessions, consistent-hashing, upstreams]
level: advanced
status: docs-checked
description: "Kong Upstream hash_on options for consistent-hashing (none, consumer, ip, header, cookie), the fallback attribute, companion fields and failover limits."
sources:
  - https://developer.konghq.com/gateway/entities/upstream/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upstream hash_on

Used with `algorithm: consistent-hashing`.

`hash_on` defaults to `none` (hashing disabled; round-robin is used instead).

`hash_on` options: `none`, `consumer` (falls back to the Credential ID if there is no Consumer), `ip`, `header`, `cookie`.

A fallback attribute (`hash_fallback`) is used when the primary input is missing. It cannot be used when `cookie` is the primary.

Companion fields:
- `hash_on_header` (or `hash_fallback_header`): the header name when hashing on a header
- `hash_on_cookie` and `hash_on_cookie_path`: cookie name and path; if the cookie is absent the response sets it with a random UUID value

Sticky sessions are a separate algorithm (`sticky-sessions`, v3.11+) using a cookie managed by the browser.

Failover Targets do not work with `consistent-hashing` or `sticky-sessions`.

## Checked

2026-11-04. Confirmed against the Upstream entity page: hash_on options none, consumer, ip, header, cookie and their companion fields, primary and fallback attributes, cookie behaviour, sticky-sessions from 3.11, failover Target limits. Removed path, query_arg and uri_capture options, their companion fields, the hash_fallback default and the cookie path default: the page does not list them.

Method: documentation only; no commands were run.
