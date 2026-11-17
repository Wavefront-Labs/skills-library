---
id: computing-software.devops-ci-cd.verdaccio.outbound-proxy-settings
name: outbound-proxy-settings
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [http-proxy, https-proxy, no-proxy, proxy-server, uplink-proxy, corporate-proxy]
level: practitioner
status: docs-checked
description: "Route Verdaccio's outbound registry traffic through an HTTP or HTTPS proxy with http_proxy, https_proxy and no_proxy, globally or per uplink."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/uplinks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Define a proxy at top level or per uplink; the uplink value wins.

```yaml
http_proxy: http://something.local/
https_proxy: https://something.local/
no_proxy: localhost,127.0.0.1
uplinks:
  npmjs:
    url: https://registry.npmjs.org/
    https_proxy: http://my.proxy.local/
```
Key rule: the proxy key must match the protocol of the uplink URL. For `https://registry.npmjs.org`, use `https_proxy`, even if the proxy itself speaks plain http.

`no_proxy` is a comma-separated list of domain extensions the proxy must not be used for. Uplinks also accept `no_proxy` individually.

The configuration page describes the top-level keys as the way to set an `X-Forwarded-For` header toward the remote.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Proxy) and Uplinks. Confirmed: top-level and per-uplink proxies with the uplink winning, matching the key to the uplink protocol, no_proxy as a comma list, and the X-Forwarded-For note. Removed or corrected: the verify paragraph about log lines and ECONNREFUSED.

Method: documentation only; no commands were run.
