---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ingress-external-auth-oauth2-proxy
name: ingress-external-auth-oauth2-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ingress, oauth2-proxy, auth-url, ingress-nginx, oidc]
level: practitioner
status: docs-checked
description: "Protect apps behind ingress-nginx with external authentication via oauth2-proxy and auth-url/auth-signin annotations, passing identity headers upstream."
sources: ["https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#external-authentication", "https://kubernetes.github.io/ingress-nginx/examples/auth/oauth-external-auth/", "https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview", "https://oauth2-proxy.github.io/oauth2-proxy/configuration/integrations/nginx", "https://github.com/oauth2-proxy/manifests"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External auth with oauth2-proxy

ingress-nginx is retired (its README: best-effort maintenance until March 2026, no releases
or security fixes afterwards). The annotations below apply to clusters still running it;
for new work choose a Gateway API implementation and its own external-auth mechanism.

## Deploy oauth2-proxy
```bash
helm repo add oauth2-proxy https://oauth2-proxy.github.io/manifests
helm install oauth2-proxy oauth2-proxy/oauth2-proxy -n auth --create-namespace \
  --set config.clientID=$CLIENT_ID --set config.clientSecret=$CLIENT_SECRET \
  --set config.cookieSecret=$(openssl rand -base64 32 | tr -- '+/' '-_') \
  --set extraArgs.provider=oidc --set extraArgs.oidc-issuer-url=https://idp.example.com \
  --set extraArgs.email-domain=example.com --set extraArgs.cookie-domain=.example.com \
  --set extraArgs.whitelist-domain=.example.com --set extraArgs.set-xauthrequest=true \
  --set ingress.enabled=true --set ingress.className=nginx --set 'ingress.hosts[0]=auth.example.com'
```
The cookie-secret command is the OpenSSL variant from the oauth2-proxy docs (URL-safe base64
of 32 random bytes). The chart's `config.*`, `extraArgs` and `ingress.*` values are as in
the `oauth2-proxy/manifests` chart; `--set-xauthrequest` makes oauth2-proxy return the
`X-Auth-Request-User`, `-Groups`, `-Email` and `-Preferred-Username` headers.

## Protect an app
```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/auth-url: "https://auth.example.com/oauth2/auth"
    nginx.ingress.kubernetes.io/auth-signin: "https://auth.example.com/oauth2/start?rd=$scheme://$host$escaped_request_uri"
    nginx.ingress.kubernetes.io/auth-response-headers: "X-Auth-Request-User,X-Auth-Request-Email,X-Auth-Request-Groups"
```
Flow: nginx calls `auth-url` for each request (subrequest); a 2xx lets it through and copies the
listed response headers upstream; a 401 redirects the browser to `auth-signin`. The
ingress-nginx example serves oauth2-proxy on the app's own host, where
`auth-signin: https://$host/oauth2/start?rd=$escaped_request_uri` is enough; with a separate
auth host as above, the `rd` value must be a full URL on a domain allowed by
`--whitelist-domain`.

## Hardening
- Upstream apps must only trust `X-Auth-Request-*` headers coming through the ingress: block
  direct access with NetworkPolicy so clients cannot forge them.
- Cache auth results to cut latency: `nginx.ingress.kubernetes.io/auth-cache-key: $cookie__oauth2_proxy`
  (the default oauth2-proxy cookie is named `_oauth2_proxy`) and an `auth-cache-duration` such as
  `200 202 10m, 401 5m` (the documented default is `200 202 401 5m`). Cached results outlive
  session changes, so keep the 2xx duration short.
- Restrict by group with oauth2-proxy `--allowed-group`.
- Use the in-cluster Service as `auth-url` (for example
  `http://oauth2-proxy.auth.svc.cluster.local/oauth2/auth`; the chart's Service is `ClusterIP`
  on port 80) to avoid a hairpin through the load balancer.
- The oauth2-proxy nginx guide notes that `/oauth2/auth` returns 2xx for an authenticated
  request and 401 or 403 otherwise, and that redirects to sign-in are for browser routes
  only: API clients should get a plain 401/403.

## Verify
```bash
curl -sI https://app.example.com | head -3          # 302 to auth.example.com
curl -s -H "Cookie: _oauth2_proxy=..." https://app.example.com/headers   # identity headers present
```

## Checked
2026-10-27. Documentation releases: ingress-nginx controller v1.15.1 (annotations docs and example), oauth2-proxy v7.15.5 docs, oauth2-proxy/manifests chart values (main).
Confirmed: `auth-url`, `auth-signin`, `auth-response-headers`, `auth-cache-key`, `auth-cache-duration` semantics and default; the cookie-secret recipe; flags `--set-xauthrequest`, `--cookie-domain`, `--whitelist-domain`, `--email-domain`, `--allowed-group`, `--oidc-issuer-url`; default cookie name; chart value names, Service type and port; retirement text.
Method: documentation only; no commands were run.
