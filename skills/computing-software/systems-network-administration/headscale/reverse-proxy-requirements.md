---
id: computing-software.systems-network-administration.headscale.reverse-proxy-requirements
name: reverse-proxy-requirements
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, reverse-proxy, websocket, trusted-proxies, tailscale-control-protocol]
level: advanced
status: docs-checked
description: "What any reverse proxy in front of Headscale must do: WebSocket upgrade for the control protocol, TLS termination, trusted_proxies and client IP headers."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/integration/reverse-proxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverse proxy requirements

The reverse proxy docs are community-written and may be outdated. Test without a reverse proxy before raising an issue.

## Must-haves

- WebSocket support. Peculiarities: the upgrade uses the POST method, and the `Upgrade` header value is `tailscale-control-protocol`.
- STUN for the embedded DERP server is expected to be exposed directly or kept on localhost, not proxied; the page's limitations note says it requires udp/3478 to be served publicly.

## Base configuration

```yaml
server_url: https://<SERVER_NAME>
listen_addr: 127.0.0.1:8080
metrics_listen_addr: 127.0.0.1:9090
trusted_proxies:
  - 127.0.0.1/32
  - ::1/128
tls:
  cert_path: ""
  key_path: ""
```

Headscale does not terminate TLS here; the proxy does. Expected startup warning: `WRN listening without TLS but ServerURL does not start with http://`.

## Trusted proxies

Headscale ignores `True-Client-IP`, `X-Real-IP` and `X-Forwarded-For` unless the TCP peer matches `trusted_proxies`. The proxy must replace any client-supplied values. Precedence: `True-Client-IP`, then `X-Real-IP`, then `X-Forwarded-For`; the first valid IP is used.

## Gotchas

- Cloudflare Proxy and Tunnel are not supported (no WebSocket POSTs; issue 1468).
- The example configs answer `/generate_204` with 204 on port 80 (Tailscale captive portal detection).
- Examples: reverse-proxy-nginx, reverse-proxy-other-proxies.

## Checked

2026-11-04. Confirmed against the Headscale reverse-proxy page: community-documentation warning, WebSocket POST and Upgrade value, base configuration, the TLS warning line, trusted_proxies behaviour and header precedence, and Cloudflare non-support. Reworded the STUN and generate_204 lines to what the page says.
Method: documentation only; no commands were run.
