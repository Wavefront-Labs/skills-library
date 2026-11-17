---
id: computing-software.systems-network-administration.varnish-cache.backend-and-client-timeouts
name: backend-and-client-timeouts
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [connect-timeout, first-byte-timeout, idle-timeout, between-bytes-timeout]
level: practitioner
status: docs-checked
description: "Know the Varnish timeout parameters and their defaults for backend connect, first byte, between bytes, idle connections, client idle and pipe, and override them per backend."
sources:
  - https://www.varnish.org/docs/reference/varnishd/
  - https://www.varnish.org/docs/reference/vcl-backend/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# backend and client timeouts

Backend side (varnishd defaults):

- `connect_timeout` 3.5s: give up connecting.
- `first_byte_timeout` 60s: wait for the first response byte.
- `between_bytes_timeout` 60s: gap between received bytes.
- `backend_idle_timeout` 60s: close unused pooled backend connections.

`first_byte_timeout` and `between_bytes_timeout` do not apply to piped requests. VCL values on a backend take precedence:

```vcl
backend slow {
    .host = "192.0.2.10";
    .connect_timeout = 1.4s;
    .first_byte_timeout = 20s;
    .between_bytes_timeout = 10s;
}
```

Client side:
- `timeout_idle` 5s (max 3600s): idle until full request headers are received.
- `timeout_linger` 0.05s (experimental): how long a worker lingers on an idle session before handing it to the waiter.
- `pipe_timeout` 60s: idle timeout for PIPE sessions.
- `send_timeout` and `cli_timeout` also exist.

Runtime: `varnishadm param.set <name> <value>`.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the claim that connect_timeout does not apply to piped requests (page says this only for first_byte_timeout and between_bytes_timeout) and the example timeout value.

Method: documentation only; no commands were run.
