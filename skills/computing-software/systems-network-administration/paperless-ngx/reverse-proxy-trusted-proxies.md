---
id: computing-software.systems-network-administration.paperless-ngx.reverse-proxy-trusted-proxies
name: reverse-proxy-trusted-proxies
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, reverse-proxy, trusted-proxies, x-forwarded-for, rate-limiting, allauth]
level: advanced
status: docs-checked
description: "Configure proxy headers and trusted proxies so Paperless-ngx sees real client IPs and login rate limiting does not return 403 errors."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/setup/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverse proxy settings

## Why it matters in v3
Allauth changed how it determines the client IP address for login rate limiting. Behind a reverse proxy you may need to set the settings below to avoid `403 Forbidden` errors on login.

## Settings
- `PAPERLESS_TRUSTED_PROXIES`: IP address(es) of your proxies. It may be needed to prevent IP address spoofing if you use something like fail2ban with log entries for failed authorization attempts. By default it also sets the allauth trusted proxy count to the number of entries listed.
- `PAPERLESS_ALLAUTH_TRUSTED_PROXY_COUNT`: the number of trusted proxy hops represented in each `X-Forwarded-For` header, not the number of IP addresses through which the proxies can be reached. A single dual-stack proxy with an IPv4 and an IPv6 address listed is one hop. Defaults to the number of entries in `PAPERLESS_TRUSTED_PROXIES`.
- `PAPERLESS_ALLAUTH_TRUSTED_CLIENT_IP_HEADER`: use when the proxy sets a dedicated header for the real client IP, for example `X-Real-IP` (nginx) or `CF-Connecting-IP` (Cloudflare). When set, it takes precedence over the proxy count.
- `PAPERLESS_USE_X_FORWARD_HOST` and `PAPERLESS_USE_X_FORWARD_PORT`: map to Django's `USE_X_FORWARDED_HOST` and `USE_X_FORWARDED_PORT`, which may be needed behind a proxy. Both default to false.
- `PAPERLESS_PROXY_SSL_HEADER`: maps to Django's `SECURE_PROXY_SSL_HEADER`; a JSON list such as `'["HTTP_X_FORWARDED_PROTO", "https"]'`. Setting it has security implications, so read the Django documentation first.

Only trust `X-Forwarded-For` when untrusted clients cannot connect directly to Paperless-ngx.

## Related settings
- Set `PAPERLESS_URL` to your domain when behind a reverse proxy (the setup guide says so).
- Share links: if the proxy adds an authentication layer, you may want an exception that bypasses it so share links are truly publicly accessible. Do so with caution.

## Checked
Date: 2026-11-07
Pages read in full: configuration, migration-v3, usage, setup (docs/*.md from the paperless-ngx repository). The setup page was read in full including the Docker and bare-metal sections.
Corrections: reworded the trusted-proxy and client-IP-header entries to the configuration text; replaced "exempt /share/ paths" with the usage page tip wording (the page does not name the path pattern as an exemption); tied the PAPERLESS_URL line to the setup guide and added usage and setup to sources.
Method: documentation only; no commands were run.
