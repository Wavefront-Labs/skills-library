---
id: computing-software.systems-network-administration.headscale.reverse-proxy-other-proxies
name: reverse-proxy-other-proxies
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, apache, caddy, envoy, istio, cloudflare]
level: advanced
status: docs-checked
description: "Headscale behind Apache, Caddy, Envoy or Istio: the upgrade settings each needs, and why Cloudflare Proxy and Tunnel do not work."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/integration/reverse-proxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Other reverse proxies

## Apache

```apache
<VirtualHost *:80>
    ServerName <SERVER_NAME>
    RedirectMatch 204 ^/generate_204$
    RedirectMatch permanent "^/(.*)$" "https://<SERVER_NAME>/$1"
</VirtualHost>

<VirtualHost *:443>
    ServerName <SERVER_NAME>
    SSLEngine On
    SSLCertificateFile <PATH_TO_TLS_CERT>
    SSLCertificateKeyFile <PATH_TO_TLS_KEY>
    RequestHeader set True-Client-IP "%{REMOTE_ADDR}s"
    RequestHeader set X-Real-IP "%{REMOTE_ADDR}s"
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8080/ upgrade=any
</VirtualHost>
```

`upgrade=any` is required so non-WebSocket upgrades (the Tailscale control protocol) are forwarded.

## Caddy

```
<SERVER_NAME> {
	reverse_proxy 127.0.0.1:8080 {
		header_up True-Client-IP {remote_host}
		header_up X-Real-IP {remote_host}
	}
}
```

Caddy provisions certificates, forces HTTPS and proxies WebSockets automatically. The docs add an `http://<SERVER_NAME>` block returning 204 for `/generate_204` and redirecting the rest.

## Envoy and Istio

Add an `upgrade_type` named `tailscale-control-protocol` to the HTTP connection manager. In Istio use an `EnvoyFilter` that MERGEs `upgrade_configs` with `upgrade_type: tailscale-control-protocol` into `envoy.filters.network.http_connection_manager`.

## Cloudflare

Cloudflare Proxy and Cloudflare Tunnel are not supported: Cloudflare does not allow the WebSocket POSTs Tailscale needs (issue 1468).

## Gotcha

Headscale ignores the client IP headers unless the TCP peer matches `trusted_proxies`, so set it to the proxy's address.

## Checked

2026-11-04. Confirmed against the Headscale reverse-proxy page (community documentation, may be outdated): the Apache and Caddy examples, `upgrade=any`, Envoy and Istio upgrade_type, and the Cloudflare non-support with issue 1468.
Method: documentation only; no commands were run.
