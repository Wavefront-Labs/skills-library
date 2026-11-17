---
id: computing-software.messaging-and-integration.ntfy.behind-proxy
name: behind-proxy
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, reverse-proxy, behind-proxy, nginx, websockets]
level: advanced
status: docs-checked
description: "Run ntfy behind nginx, Apache or Caddy: behind-proxy, forwarded headers, WebSocket forwarding and timeouts."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Behind a reverse proxy

Set `behind-proxy: true`. Without it all visitors count as one IP for rate limiting.

```yaml
behind-proxy: true
proxy-forwarded-header: "X-Client-IP"
proxy-trusted-hosts: "1.2.3.0/24, 1.2.2.2, 2001:db8::/64"
```

- `proxy-forwarded-header` defaults to `X-Forwarded-For` (`Forwarded` also works).
- `proxy-trusted-hosts` is only useful with multiple proxies.
- `visitor-prefix-bits-ipv4` defaults to 32, `visitor-prefix-bits-ipv6` to 64.

## WebSockets

Forward the `Connection` and `Upgrade` headers.

nginx key lines:

```
proxy_pass http://127.0.0.1:2586;
proxy_http_version 1.1;
proxy_buffering off;
proxy_request_buffering off;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
client_max_body_size 0;
proxy_connect_timeout 3m;
proxy_send_timeout 3m;
proxy_read_timeout 3m;
```

Apache 2.4.47 or newer: `ProxyPass / http://127.0.0.1:2586/ upgrade=websocket`, plus `ProxyPassReverse`, `SetEnv proxy-nokeepalive 1`, `SetEnv proxy-sendchunked 1`. Older Apache needs mod_rewrite with `ws://127.0.0.1:2586/$1 [P,L]`.

Caddy: `reverse_proxy 127.0.0.1:2586` handles HTTP and WebSockets automatically.

## Checked

2026-11-04. Confirmed against the ntfy config page (Behind a proxy, nginx/Apache2/caddy): `behind-proxy`, `proxy-forwarded-header` default and the `X-Client-IP` and `Forwarded` examples, `proxy-trusted-hosts`, prefix-bit defaults 32 and 64, nginx directives, Apache 2.4.47 split and directives, Caddy note. Removed: an unsupported TLS line and the Verify step.
Method: documentation only; no commands were run.
