---
id: computing-software.systems-network-administration.healthchecks.docker-reverse-proxy
name: docker-reverse-proxy
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, reverse-proxy, x-forwarded-for, x-forwarded-proto, csrf-403]
level: advanced
status: docs-checked
description: "Front a Healthchecks container with a TLS reverse proxy: required X-Forwarded-For and X-Forwarded-Proto handling for NGINX and HAProxy, and the CSRF 403 symptom."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_docker.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Docker images do not handle TLS. Put a TLS-terminating reverse proxy or load balancer in front for public exposure. It must:

- Set `X-Forwarded-For`. Healthchecks uses it for client IPs; without it, clients can spoof their IP and bypass IP-based login rate limiting.
- Discard any client-sent `X-Forwarded-Proto` and set it to the original protocol (`http` or `https`). Otherwise you may see HTTP 403 "CSRF verification failed" errors.

NGINX:

```
proxy_set_header X-Forwarded-Proto $scheme;
```

HAProxy:

```
http-request set-header X-Forwarded-Proto https if { ssl_fc }
http-request set-header X-Forwarded-Proto http unless { ssl_fc }
```

Related settings:
- `SITE_ROOT`: public base URL (use https).
- `SECURE_PROXY_SSL_HEADER` (default None): header name and value that mark a request as HTTPS behind a proxy.
- `REMOTE_USER_HEADER`: external-auth header; the proxy must strip spoofed copies.
- `ALLOWED_HOSTS`: domains the site may serve.

Telegram needs `SITE_ROOT` on https.

## Checked

2026-11-04. Confirmed against the Healthchecks Docker documentation and server configuration page: no TLS in the images, X-Forwarded-For requirement and rate-limit bypass, X-Forwarded-Proto handling and the CSRF 403 symptom, the NGINX and HAProxy snippets, SECURE_PROXY_SSL_HEADER, REMOTE_USER_HEADER and Telegram https requirement. Nothing removed.

Method: documentation only; no commands were run.
