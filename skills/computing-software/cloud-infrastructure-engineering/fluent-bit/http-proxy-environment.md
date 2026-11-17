---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.http-proxy-environment
name: http-proxy-environment
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, http-proxy, http-proxy-env, connect-tunnel, egress, net-proxy-env-ignore]
level: practitioner
status: docs-checked
description: "Route Fluent Bit egress HTTP and HTTPS traffic through a proxy using the HTTP_PROXY environment variable."
sources: ["https://docs.fluentbit.io/manual/administration/http-proxy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP proxy through the environment

Fluent Bit routes egress HTTP and HTTPS traffic through a proxy when `HTTP_PROXY` or `http_proxy` is set; if both are set, `HTTP_PROXY` is preferred. Format: `SCHEME://USER:PASS@HOST:PORT`.

- `SCHEME` is `http` or `https`. Use `https` when the connection to the proxy itself must be TLS-encrypted. There is no separate `HTTPS_PROXY` variable; the scheme lives inside the same variable.
- `USER` and `PASS` are for basic authentication; omit them when not needed.
- `HOST` and `PORT` locate the proxy.

```text
HTTP_PROXY='http://example_user:example_pass@proxy.example.com:8080'
HTTP_PROXY='http://proxy.example.com:8080'
```

This is the same convention containerised environments and Go applications use. `NO_PROXY` / `no_proxy` is a comma-separated list of host names or IP addresses that bypass the proxy; `NO_PROXY` takes precedence when both are set.

To ignore these variables for a plugin, set `net.proxy_env_ignore: true` on it (default `false`).

The HTTP output plugin also has its own proxy configuration. That works, but do not combine it with the `HTTP_PROXY` environment variable.

For TLS to the proxy itself, see `computing-software.cloud-infrastructure-engineering.fluent-bit.https-proxy-tls`.

## Checked

2026-11-03. Confirmed on the Fluent Bit HTTP proxy page and the Networking page: variable format and examples, no HTTPS_PROXY variable, HTTP_PROXY precedence, NO_PROXY, HTTP CONNECT tunnelling, the HTTP output caveat, and net.proxy_env_ignore default false. Removed: an unsourced verification step.

Method: documentation only; no commands were run.
