---
id: computing-software.systems-network-administration.varnish-cache.backend-definitions
name: backend-definitions
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [backend-declaration, backend-attributes, max-connections, connection-pool]
level: practitioner
status: docs-checked
description: "Declare VCL backends: .host or .path, host_header, per-backend timeouts, max_connections, wait_limit, proxy_header, via, and how backend connections are pooled."
sources:
  - https://www.varnish.org/docs/reference/vcl-backend/
  - https://www.varnish.org/docs/users-guide/vcl-backends/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# backend definitions

```vcl
backend default {
    .host = "backend.example.com:8080";   # or .host plus .port
    .host_header = "example.com";
    .connect_timeout = 1.4s;
    .max_connections = 1000;
    .wait_limit = 100;
    .wait_timeout = 1s;
}
backend sock { .path = "/path/to/http.sock"; }   # or "@abstract"
backend default none;                             # always fails with 503
```

- Specify exactly one of `.host` or `.path`. A host name may resolve to at most one IPv4 and one IPv6 address.
- A backend named `default` is used unless another is set; otherwise the first defined backend is the default.
- `.max_connections` caps simultaneous connections; `.wait_limit` caps queued transactions (defaults from `backend_wait_limit`, 0 means no queueing) and `.wait_timeout` should never exceed a couple of seconds.
- `.proxy_header = 1 | 2` sends a PROXY header and makes each connection single-use, which can exhaust local ports.
- `.via = proxy_backend` connects through a PROXY2 endpoint; `.authority` sets the SNI-like authority.
- Connections are pooled across VCLs and backends by host/port or path. Add `Connection: close` in `vcl_backend_fetch` to avoid reuse.
- A `none` backend evaluates false in a boolean test.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: nothing needed removing.

Method: documentation only; no commands were run.
