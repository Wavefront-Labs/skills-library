---
id: computing-software.systems-network-administration.paperless-ngx.url-allowed-hosts-csrf
name: url-allowed-hosts-csrf
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, paperless-url, allowed-hosts, csrf, cors, subpath]
level: practitioner
status: docs-checked
description: "Set PAPERLESS_URL to configure allowed hosts, CORS and CSRF origins at once, and host Paperless-ngx under a subpath."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL, allowed hosts and CSRF

## PAPERLESS_URL
Set it to the public address, with no trailing slash and no path, for example `https://paperless.domain.com`. It can set three options, and their values are combined with any you set separately:
- `PAPERLESS_ALLOWED_HOSTS`
- `PAPERLESS_CORS_ALLOWED_HOSTS` (default `http://localhost:8000`)
- `PAPERLESS_CSRF_TRUSTED_ORIGINS` (as of Django 4.0 required to access the Django admin via the web)

It defaults to an empty string, which leaves the other settings unaffected. The value cannot contain a path, even if you host at a subpath.

The usage page also says to set it (or the corresponding settings) for password reset, and the `{{doc_url}}` workflow placeholder requires it. The OAuth email callback uses it unless `PAPERLESS_OAUTH_CALLBACK_BASE_URL` is set.

## Allowed hosts
If Paperless faces the internet, set the domain name explicitly; the default `*` (all hosts) leaves you open to HTTP host header attacks. It is a comma-separated list: `example.com` and `example.com,www.example.com` are fine, but not ` example.com` or `example.com,`. `localhost` is always allowed for the Docker healthcheck.

## Subpath hosting
To serve at `example.com/paperless`, set `PAPERLESS_FORCE_SCRIPT_NAME=/paperless` (no trailing slash). Behind a reverse proxy such as Traefik or Nginx at a subpath you also need `PAPERLESS_FORCE_SCRIPT_NAME`. If you change `PAPERLESS_STATIC_URL`, include the trailing slash; the default is `/static/`.

## Two instances on one host
Give each a different `PAPERLESS_COOKIE_PREFIX` (default empty, which leaves cookie names unchanged), and log in again after changing it.

## Checked
Date: 2026-11-07
Pages read in full: configuration (docs/configuration.md), usage (docs/usage.md, covering password reset and the doc_url placeholder), setup (docs/setup.md).
Corrections: kept every setting and default after matching it to the configuration text; the password reset and doc_url statements were previously unsupported by the single listed source, so usage was added to sources; the example host was changed to the documented one.
Method: documentation only; no commands were run.
