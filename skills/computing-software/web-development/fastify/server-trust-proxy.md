---
id: computing-software.web-development.fastify.server-trust-proxy
name: server-trust-proxy
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, trust-proxy, reverse-proxy, security]
level: practitioner
status: docs-checked
description: "Use trustProxy so request.ip, ips, host and protocol reflect X-Forwarded headers only from trusted proxies."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Recommendations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Behind nginx, HAProxy or a cloud load balancer, enable `trustProxy` so Fastify reads `X-Forwarded-For`, `X-Forwarded-Host` and `X-Forwarded-Proto`.

Accepted values:
- `true`: trust all proxies
- `false`: default, do not trust any proxies
- an IP or CIDR string, for example `'127.0.0.1'`; may be a comma separated list such as `'127.0.0.1,192.168.1.1/24'`
- an array of IP/CIDR strings, for example `['127.0.0.1']`
- a function taking `address` first, for example `(address, hop) => address === '1.2.3.4' && hop === 0`

Numeric hop counts are disabled: they cannot validate the immediate peer and let direct clients spoof `X-Forwarded-*` values.

```js
const fastify = require('fastify')({ trustProxy: '10.0.0.0/8' })

fastify.get('/', (request) => ({
  ip: request.ip,
  ips: request.ips,
  host: request.host,
  protocol: request.protocol
}))
```

The Recommendations guide's nginx config sets `X-Real-IP`, `X-Forwarded-For` and `X-Forwarded-Proto` and notes you may set `trustProxy` to your nginx address so those fields are used. The Serverless guide's Cloud Run example uses `Fastify({ trustProxy: true })`.

Gotcha: `ip`, `ips`, `host` and `protocol` derive from socket/forwarding metadata and are untrusted unless the proxy chain is explicitly trusted and validated; do not use them directly for authorization. Custom trust functions must validate `address`. If a request has multiple `x-forwarded-host` or `x-forwarded-proto` headers, only the last one is used.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md, Recommendations.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
