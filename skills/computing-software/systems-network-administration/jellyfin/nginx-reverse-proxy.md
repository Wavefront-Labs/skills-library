---
id: computing-software.systems-network-administration.jellyfin.nginx-reverse-proxy
name: nginx-reverse-proxy
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, nginx, reverse-proxy, websocket, proxy-buffering, log-format]
level: advanced
status: draft
description: "Proxy Jellyfin with Nginx using the documented server block, a separate /socket location and log filtering for api_key."
sources: ["https://jellyfin.org/docs/general/post-install/networking/8_reverse-proxy/nginx/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Nginx reverse proxy for Jellyfin

Create `/etc/nginx/sites-available/jellyfin`, symlink it into `sites-enabled` and reload nginx. A listener on port 80 is required for Certbot renewal.

Key elements of the documented HTTPS server block:
- `listen 443 ssl;` plus `http2 on;` for nginx 1.25 or later (older versions use `listen 443 ssl http2;`).
- `client_max_body_size 20M;` because the default of 1M may be too small for posters.
- `ssl_protocols TLSv1.3 TLSv1.2;` with certificate paths under `/etc/letsencrypt/live/`.
- `set $jellyfin 127.0.0.1;` to hold the upstream in a variable.
- Security headers, including `X-Content-Type-Options "nosniff"`, a `Permissions-Policy` that may cause issues with some clients, and a Content-Security-Policy that must whitelist external scripts such as `cast_sender.js` for Chromecast.
- `location /` with `proxy_pass http://$jellyfin:8096;`, `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Host` headers and `proxy_buffering off;`.
- `location /socket` with `proxy_http_version 1.1;`, `Upgrade $http_upgrade` and `Connection "upgrade"` for WebSockets.
- A port 80 server that returns 301 to HTTPS.

**Hide secrets in logs.** Define a `log_format` that uses a `map $request $secretfilter` replacing the value of `api_key=` or `ApiKey=` with `***`, and point `access_log` in every server block at it.

Also add the proxy's address to Known Proxies in Jellyfin.
