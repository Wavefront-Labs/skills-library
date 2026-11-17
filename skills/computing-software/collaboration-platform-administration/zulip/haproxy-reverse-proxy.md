---
id: computing-software.collaboration-platform-administration.zulip.haproxy-reverse-proxy
name: haproxy-reverse-proxy
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [haproxy, tls-termination, forwarded-proto]
level: advanced
status: docs-checked
description: "Configure HAProxy as a TLS-terminating front end for Zulip with X-Forwarded-Proto headers, a 20 minute server timeout and a health-checked HTTPS backend."
sources: ["https://zulip.readthedocs.io/en/latest/production/reverse-proxies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HAProxy in front of Zulip

After configuring Zulip to trust the proxy's address, use a minimal frontend and backend.

Frontend `zulip`, in `mode http`:

- `bind *:80` and `bind *:443 ssl crt /etc/ssl/private/zulip-combined.crt`.- `http-request redirect scheme https code 301 unless { ssl_fc }` sends plain HTTP to HTTPS.
- `http-request set-header X-Forwarded-Proto http unless { ssl_fc }` and `http-request set-header X-Forwarded-Proto https if { ssl_fc }`. Setting the header, rather than appending to it, is what Zulip's CSRF checks rely on.
- `default_backend zulip`.

Backend `zulip`, in `mode http`:

- `timeout server 20m`, so real-time long-polling is not cut off.
- `server zulip 10.10.10.10:443 check ssl ca-file /etc/ssl/certs/ca-certificates.crt`, which health-checks the Zulip server and verifies its certificate.

Change the `bind ... crt` path and the backend `server` address for your deployment.
Remember to put the proxy IP in the `[loadbalancer]` `ips` setting in `/etc/zulip/zulip.conf`; otherwise logs show the proxy address for every client.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/reverse-proxies.html (zulip.readthedocs.io, latest). Removed: the combined-file explanation and the HTTP-only server-line advice.

Method: documentation only; no commands were run.
