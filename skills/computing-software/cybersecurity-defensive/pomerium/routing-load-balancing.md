---
id: computing-software.cybersecurity-defensive.pomerium.routing-load-balancing
name: routing-load-balancing
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [route-matching, lb-policy, active-health-checks, outlier-detection, host-header]
level: practitioner
status: docs-checked
description: "Define Pomerium routes with from and to URLs, path matchers, host header handling, load balancing policies, health checks and match order."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Basics**: `from` is the external URL (`https`, `tcp+https` or `udp+https` only); `to` is one URL or a list (`http://`, `https://`, `http+unix://`, `tcp://`, `udp://`), with an optional `,weight`. A trailing slash on `to` changes path forwarding. `redirect` is an alternative to `to`.

**Matchers**: exact path, `regex` (Go RE2), `prefix`, with `prefix_rewrite` and regex rewrite pattern and substitution.

**Host header** (mutually exclusive): `preserve_host_header` (default false), `host_rewrite`, `host_rewrite_header`, or `host_path_regex_rewrite_pattern` and substitution. `set_request_headers` cannot change `Host` or `:` pseudo-headers.

**Headers**: `set_request_headers`, `remove_request_headers`, `rewrite_response_headers`.

**Websockets**: `allow_websockets` skips global timeouts (route `timeout` still applies); long-lived connections can be abused in DoS.

**Load balancing**: several `to` URLs are balanced. Use active checks (`health_checks` entries holding `http_health_check` with `path`, or `tcp_health_check`; `timeout`, `interval`, `healthy_threshold`, `unhealthy_threshold`) and/or passive `outlier_detection` (empty object valid). `lb_policy`: `ROUND_ROBIN` (default), `LEAST_REQUEST`, `RING_HASH`, `RANDOM`, `MAGLEV`.

**Match order**: config file routes first, in order; Console or Ingress Controller routes after, by host ascending, then path, regex and prefix descending. First match wins.

**Certificates**: `certificates` list of `cert`/`key`, or `certificate_file` and `certificate_key`; sources are additive.

## Checked

2026-11-04. Confirmed against the Routing page: from and to schemes, weights, trailing slash, matchers, host header options, header settings, websockets, health checks, outlier_detection, lb_policy values and default, match order, certificate settings. Added the health_checks key the page uses.

Method: documentation only; no commands were run.
