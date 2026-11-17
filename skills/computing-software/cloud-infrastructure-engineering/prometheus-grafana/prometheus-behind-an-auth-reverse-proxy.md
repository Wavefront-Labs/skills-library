---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-behind-an-auth-reverse-proxy
name: prometheus-behind-an-auth-reverse-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-reverse-proxy, oauth2-proxy-prometheus, prometheus-security, sso, web-external-url, route-prefix]
level: practitioner
status: docs-checked
description: "Put Prometheus behind oauth2-proxy or an ingress with SSO: bind to localhost, set --web.external-url and route prefix, and keep scrape and API paths working."
sources: ["https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://prometheus.io/docs/operating/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus behind an auth reverse proxy

Prometheus has only basic auth and TLS built in. For SSO, put an authenticating proxy in front.

## Prometheus flags
```bash
prometheus \
  --web.listen-address=127.0.0.1:9090 \        # or a ClusterIP only reachable by the proxy
  --web.external-url=https://prometheus.example.com/ \
  --web.route-prefix=/
```
If served under a sub-path: `--web.external-url=https://ops.example.com/prometheus/` (route prefix defaults to the URL path).

## oauth2-proxy
```bash
oauth2-proxy \
  --provider=oidc --oidc-issuer-url=https://idp.example.com/realms/ops \
  --client-id=prometheus --client-secret-file=/etc/secret \
  --cookie-secret-file=/etc/cookie --email-domain=example.com \
  --upstream=http://127.0.0.1:9090/ \
  --http-address=0.0.0.0:4180 \
  --skip-auth-route='^/-/(healthy|ready)$'
```
Restrict by group with `--allowed-group=sre` (provider support varies).

## Machine clients (Grafana, other Prometheus servers)
- Grafana should reach Prometheus on the internal address (not through SSO), or via the proxy with a bearer token the proxy accepts (`--skip-jwt-bearer-tokens` with an issuer you trust).
- Keep internal network policy so only Grafana/Thanos/federation can reach port 9090.

## Gotchas
- Wrong `--web.external-url` breaks the absolute links Prometheus generates back to itself (UI and alert links).
- Exposing the admin API (`--web.enable-admin-api`) to every SSO user lets them delete series; keep it off or restrict the path at the proxy.

## Verify
- [ ] Unauthenticated browser request redirects to the IdP; health endpoints still return 200 for probes.
- [ ] Alert notifications link to the external URL and open correctly.

## Checked
Date: 2026-10-28. Confirmed in the Prometheus command-line reference (`--web.external-url`, `--web.route-prefix` default), the Prometheus security page (built-in TLS and basic auth, `--web.enable-admin-api` disabled by default and exposing admin paths, advice to block mutating paths at a reverse proxy) and the oauth2-proxy configuration overview (`--provider`, `--oidc-issuer-url`, `--client-id`, `--client-secret-file`, `--cookie-secret-file`, `--email-domain`, `--upstream`, `--http-address`, `--allowed-group`, `--skip-auth-route`, `--skip-jwt-bearer-tokens`), and the `/-/healthy` and `/-/ready` endpoints in the Prometheus management API page. Removed the unconfirmed ingress-nginx annotation variant and the `generatorURL` field name.
Method: documentation only; no commands were run.
