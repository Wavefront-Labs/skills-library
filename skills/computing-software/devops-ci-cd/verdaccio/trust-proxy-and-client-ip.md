---
id: computing-software.devops-ci-cd.verdaccio.trust-proxy-and-client-ip
name: trust-proxy-and-client-ip
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [trust-proxy, x-forwarded-for, client-ip, express-trust-proxy, rate-limiting, cidr-whitelist]
level: advanced
status: docs-checked
description: "Set server.trustProxy when Verdaccio sits behind a reverse proxy so rate limiting and token CIDR whitelists see the real client address."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/reverse-proxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Behind a reverse proxy or load balancer every request appears to come from the proxy.

```yaml
server:
  trustProxy: '127.0.0.1'
```
The value goes straight to Express `trust proxy`: an address, a subnet, a comma-separated list or a hop count.

Two features depend on it:
- rate limiting, which otherwise counts all users as one client and throttles them together;
- the CIDR whitelist of npm tokens, which cannot enforce anything if it only ever sees the proxy address.

Also forward `X-Forwarded-Proto` (protocol) and `Host` (domain) from the proxy; those headers are used to build public URLs.

Gotcha: only list addresses you control. Trusting an address means believing the `X-Forwarded-For` header it sends.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Running behind a proxy) and Reverse Proxy. Confirmed: server.trustProxy and its Express forms, the rate-limit and CIDR whitelist dependencies, only trusting addresses you control, and the Host and X-Forwarded-Proto headers. Removed or corrected: the verify paragraph about per-client IPs in the log.

Method: documentation only; no commands were run.
