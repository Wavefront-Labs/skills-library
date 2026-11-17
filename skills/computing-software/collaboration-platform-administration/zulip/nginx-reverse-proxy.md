---
id: computing-software.collaboration-platform-administration.zulip.nginx-reverse-proxy
name: nginx-reverse-proxy
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [nginx-proxy, proxy-read-timeout, proxy-buffering]
level: advanced
status: docs-checked
description: "Put your own nginx in front of Zulip with a working server block, forwarded headers, long proxy_read_timeout, no buffering and client_max_body_size for uploads."
sources: ["https://zulip.readthedocs.io/en/latest/production/reverse-proxies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nginx in front of Zulip

First complete the proxy-trust setup on the Zulip server. For the proxy's root `nginx.conf`, copy `/etc/nginx/nginx.conf` from a Zulip server: it carries recommended settings, and without `client_max_body_size` large uploads fail.

A site file in `/etc/nginx/sites-available` needs two server blocks. The first listens on 80 (and IPv6) and returns a 301 redirect to `https://$host$request_uri`. The second listens on 443 with `ssl http2`, sets `server_name`, and points `ssl_certificate` and `ssl_certificate_key` at your Let's Encrypt `fullchain.pem` and `privkey.pem`. Its `location /` block contains:

- `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`
- `proxy_set_header X-Forwarded-Proto $scheme;`
- `proxy_set_header Host $host;`
- `proxy_http_version 1.1;`
- `proxy_buffering off;`
- `proxy_read_timeout 20m;`
- `proxy_pass https://10.10.10.10:443;` (use your Zulip address)

Update `server_name`, certificate paths and `proxy_pass` for your deployment.
The timeout and buffering lines matter: long-polling for real-time events breaks if the timeout is near 60 seconds, and buffering causes occasional 502 errors on the events API.

Avoid proxy upstream names that resolve to both IPv4 and IPv6, since nginx may load-balance between them and produce hard-to-debug errors.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/reverse-proxies.html (zulip.readthedocs.io, latest). Removed: the http:// proxy_pass instruction for HTTP-only mode.

Method: documentation only; no commands were run.
