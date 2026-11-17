---
id: computing-software.devops-ci-cd.forgejo.reverse-proxy-nginx-basic
name: reverse-proxy-nginx-basic
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [nginx, reverse-proxy, merge-slashes, client-max-body-size]
level: practitioner
status: docs-checked
description: "Put nginx in front of Forgejo with the documented headers, merge_slashes off and a large body limit."
sources:
  - https://forgejo.org/docs/latest/admin/setup/reverse-proxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo runs standalone or behind a reverse proxy, which helps with subpath mapping, sharing port 80/443 with another server, proxy authentication, rate limiting, advanced security headers and caching. Forgejo does not need a proxy for HTTPS: set `PROTOCOL=https` in the `[server]` section with `CERT_FILE` and `KEY_FILE`, or let it manage certificates with `ENABLE_ACME=true`.

A basic nginx file such as `/etc/nginx/conf.d/forgejo.conf` listens on port 80 (IPv4 and IPv6), sets `server_name`, and contains `merge_slashes off;` which is required to handle URL-encoded slashes. The `location /` block proxies to `http://127.0.0.1:3000` (the default Forgejo port) and sets `Connection $http_connection`, `Upgrade $http_upgrade`, `Host $host`, `X-Real-IP $remote_addr`, `X-Forwarded-For $proxy_add_x_forwarded_for` and `X-Forwarded-Proto $scheme`, plus `client_max_body_size 512M`.

Make sure to reload or restart nginx after changing the configuration.

## Checked

2026-11-04. Confirmed against the Forgejo Reverse proxy page (intro and NGINX Basic HTTP sections): the proxy use cases, native HTTPS settings, the forgejo.conf location, merge_slashes, port 3000, every proxy_set_header line and client_max_body_size 512M. Removed: the ROOT_URL sentence (the page states it only for subpaths), the remark about large pushes and the note on Upgrade and Connection headers, none of which the page explains.

Method: documentation only; no commands were run.
