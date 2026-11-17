---
id: computing-software.messaging-and-integration.prosody.http-host-mapping-proxy
name: http-host-mapping-proxy
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, http, reverse-proxy, http-host, trusted-proxies]
level: advanced
status: docs-checked
description: "Prosody HTTP behind a reverse proxy: http_host, http_default_host, http_external_url and trusted_proxies, including the IP-spoofing risk of misconfiguring them."
sources:
  - https://prosody.im/doc/http
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP host mapping and reverse proxies

`http_host` on a VirtualHost maps an HTTP `Host` header to that XMPP host. Do not share one `http_host` between VirtualHosts. `http_default_host` (global) sends requests for unknown hosts to a named host; if that VirtualHost sets `http_host`, they must match.

```lua
VirtualHost "example.com"
http_host = "www.example.com"
http_default_host = "example.com"
```

Behind a reverse proxy, set the public URL modules advertise:

```lua
http_external_url = "https://www.example.com/"
```

`trusted_proxies` lists proxy IPs (CIDR allowed) whose `X-Forwarded-For` and `X-Forwarded-Proto` Prosody trusts:

```lua
trusted_proxies = { "127.0.0.1", "::1", "192.168.1.1" }
```

Misconfiguring it lets clients spoof their IP and bypass rate limits or access controls, so list only your proxies.

Verify: a module URL from `prosodyctl shell http list` shows the external URL, and logs record real client IPs.

## Checked

2026-11-04. Read the Prosody HTTP server page: http_host mapping and the duplicate http_host warning, http_default_host and its match rule, http_external_url, trusted_proxies with CIDR support and X-Forwarded-For and X-Forwarded-Proto handling, and the IP-spoofing risk from misconfiguration all match. Nothing removed.

Method: documentation only; no commands were run.
