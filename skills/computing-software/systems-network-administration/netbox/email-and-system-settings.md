---
id: computing-software.systems-network-administration.netbox.email-and-system-settings
name: email-and-system-settings
category: computing-software
field: systems-network-administration
product: netbox
tags: [email-configuration, base-path, http-client-ip-headers]
level: practitioner
status: docs-checked
description: "Set EMAIL, BASE_PATH, HTTP_CLIENT_IP_HEADERS and bulk update chunking in configuration.py."
sources: ["https://netboxlabs.com/docs/netbox/configuration/system/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# System settings

Goal: configure the common system parameters.

**EMAIL** (dictionary): `SERVER` (required), `PORT` (default 25), `USERNAME`, `PASSWORD`, `USE_SSL` and `USE_TLS` (default False, mutually exclusive), `SSL_CERTFILE`, `SSL_KEYFILE`, `TIMEOUT` (default 10 seconds), `FROM_EMAIL`. Without `SERVER`, an `InvalidMailer` exception is raised at send time, not at startup. Email is sent only for critical events or if configured for logging. Test from the shell:
```
python3 ./manage.py nbshell
>>> from django.core.mail import send_mail
>>> send_mail('Subject', 'Body', 'noreply-netbox@example.com', ['users@example.com'])
```

**BASE_PATH**: for an install at `https://example.com/netbox/`, set `BASE_PATH = 'netbox/'` (no scheme or domain).

**HTTP_CLIENT_IP_HEADERS**: default order `HTTP_X_REAL_IP`, `HTTP_X_FORWARDED_FOR`, `REMOTE_ADDR`; the first present header wins. The client IP is used for API token source restrictions and failed-login logging. Trust the forwarded headers only behind a reverse proxy that overwrites them.

**Others**

- `BULK_UPDATE_CHUNK_SIZE`: default 5000 rows per UPDATE; `None` disables chunking.
- `DEFAULT_LANGUAGE`: default `en-us`.
- `HOSTNAME`: defaults to the system hostname.
- `HTTP_PROXIES`: proxies for outbound requests such as webhooks.
- `DATABASE_ROUTERS` default is an empty list.

**Checklist**

1. EMAIL tested from nbshell.
2. Proxy header trust reviewed.
3. BASE_PATH has no domain.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: System configuration page: EMAIL keys including TIMEOUT default 10 seconds, USE_SSL/USE_TLS defaults, BULK_UPDATE_CHUNK_SIZE default 5000 with None disabling chunking, HTTP_CLIENT_IP_HEADERS, BASE_PATH, DEFAULT_LANGUAGE. Removed: Nothing.

Method: documentation only; no commands were run.
