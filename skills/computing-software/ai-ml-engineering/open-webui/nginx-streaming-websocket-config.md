---
id: computing-software.ai-ml-engineering.open-webui.nginx-streaming-websocket-config
name: nginx-streaming-websocket-config
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [https-nginx, nginx, websocket, sse, streaming, cors, caching, reverse-proxy]
level: advanced
status: docs-checked
description: "Configure Nginx in front of Open WebUI for streaming SSE, WebSocket upgrade, long timeouts, large uploads and safe caching that never touches auth paths."
sources:
  - https://docs.openwebui.com/reference/https
  - https://docs.openwebui.com/reference/https/nginx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a production Nginx config that streams chat responses correctly and keeps WebSockets alive.

## Non-negotiables
- `CORS_ALLOW_ORIGIN` must match your public URL (semicolon-separated list allowed), or WebSocket connections fail silently even with WebSocket support enabled in the proxy. Also set `WEBUI_URL` to the public HTTPS URL.
- Proxy buffering off. With `proxy_buffering on` (Nginx default) SSE is re-chunked and markdown tokens split: symptoms are visible `##`, `**`, missing words. In the location block: `proxy_buffering off; proxy_cache off;`.
- Even with HTTP/2 on the client side, proxy to the backend with HTTP/1.1 and pass upgrades:
```nginx
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```
- HTTPS is required for Voice Calls (microphone) except on localhost.

## Recommended structure
```nginx
upstream openwebui {
    server 127.0.0.1:3000;
    keepalive 128;
    keepalive_timeout 1800s;
    keepalive_requests 10000;
}
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    gzip on;
    gzip_types text/plain text/css application/javascript image/svg+xml;  # NOT application/json or text/event-stream

    location /api/ {
        proxy_pass http://openwebui;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        gzip off;
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_cache off;
        tcp_nodelay on;
        add_header X-Accel-Buffering "no" always;
        add_header Cache-Control "no-store" always;
        proxy_connect_timeout 1800;
        proxy_send_timeout 1800;
        proxy_read_timeout 1800;
    }
    location ~ ^/(ws/|socket\.io/) {
        proxy_pass http://openwebui;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        gzip off; proxy_buffering off; proxy_cache off;
        proxy_connect_timeout 86400; proxy_send_timeout 86400; proxy_read_timeout 86400;
    }
}
```
Size limits: `client_max_body_size 100M;` (uploads), `proxy_buffer_size 128k; proxy_buffers 4 256k; proxy_busy_buffers_size 256k; large_client_header_buffers 4 32k;` (large OAuth headers).

## Streaming mistakes
`gzip` on `application/json`, `proxy_buffering on`, `proxy_request_buffering on`, `chunked_transfer_encoding on`, `proxy_cache` on `/api/`, `X-Accel-Buffering "yes"`. The docs call `tcp_nodelay on` the most critical (avoids 200 ms delays). If streams end before the last chunk, try HTTP/1.1 instead of HTTP/2.

## Caching (optional)
Define zones in `http {}`, e.g. `proxy_cache_path /var/cache/nginx/openwebui levels=1:2 keys_zone=OPENWEBUI_CACHE:10m max_size=1g inactive=60m use_temp_path=off;` and an images zone (`OPENWEBUI_IMAGES`, 2g, 7d). Create the directories and chown them to the nginx user. Cache static assets 7-30 days, profile/model images (`^/api/v1/(users/[^/]+/profile/image|models/model/profile/image)$`) 1 day, HTML 5 min. Never cache `/api/v1/auths/`, `/oauth/`, general `/api/`, `/ws/`; use `proxy_no_cache 1; proxy_cache_bypass 1; add_header Cache-Control "no-store, no-cache, must-revalidate";`. Debug with `add_header X-Cache-Status $upstream_cache_status always;` (HIT/MISS/EXPIRED/BYPASS). Clear image cache with `rm -rf /var/cache/nginx/openwebui_images/*`.

## Checked
2026-11-04. Confirmed against the Open WebUI docs pages reference/https (index) and reference/https/nginx, with its NPM tab for the semicolon-separated CORS list (all read in full): the CORS_ALLOW_ORIGIN warning, WEBUI_URL and Voice Calls HTTPS notes, the buffering-off requirement and its symptoms, HTTP/1.1 upgrade directives behind HTTP/2, the upstream keepalive block, the /api/ and WebSocket locations with 1800 and 86400 second timeouts, gzip exclusion, size and header buffer limits, the streaming mistakes table including tcp_nodelay and X-Accel-Buffering, the cache zones, durations, never-cache list and required directives, X-Cache-Status debugging and the image cache clearing command. Nothing removed.
Method: documentation only; no commands were run.
