---
id: computing-software.cloud-infrastructure-engineering.docker.serving-spa-builds-with-unprivileged-nginx
name: serving-spa-builds-with-unprivileged-nginx
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, language-images, nginx-spa, nginx-unprivileged, react, vite, static-site, non-root]
level: practitioner
status: gated
description: "Ship a React/Vite/Angular build as a small non-root nginx image: multi-stage build, try_files SPA fallback, cache headers, runtime config injection and read-only rootfs."
sources: ["https://hub.docker.com/r/nginxinc/nginx-unprivileged", "https://hub.docker.com/_/nginx", "https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serving SPA builds with unprivileged nginx

## Dockerfile
```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-bookworm-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build                       # Vite: dist/, CRA: build/, Angular: dist/<app>/browser

FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
```
`nginx-unprivileged` runs as UID 101, listens on 8080 and keeps pid/cache paths writable
for that user. The official `nginx` image starts as root and binds 80.

## nginx.conf
```nginx
server {
  listen 8080;
  root /usr/share/nginx/html;

  location / {
    try_files $uri $uri/ /index.html;          # client-side routing fallback
  }
  location = /index.html {
    add_header Cache-Control "no-cache";       # always revalidate the entry point
  }
  location /assets/ {
    add_header Cache-Control "public, max-age=31536000, immutable";   # hashed filenames
  }
  location = /healthz { access_log off; return 200 "ok\n"; }

  gzip on;
  gzip_types text/css application/javascript application/json image/svg+xml;
}
```

## Runtime configuration (one image, many environments)
Build-time `VITE_*`/`REACT_APP_*` values are baked into the JS. To configure at runtime,
serve a small `config.js` generated at container start:
```sh
# /docker-entrypoint.d/30-config.sh (executed by the nginx image entrypoint)
cat > /usr/share/nginx/html/config.js <<EOF
window.__CONFIG__ = { apiUrl: "${API_URL}" };
EOF
```
The html dir must be writable by UID 101 for this (or write to a tmpfs and `alias` it).

## Hardening
```bash
docker run -d -p 8080:8080 --read-only \
  --tmpfs /tmp --tmpfs /var/cache/nginx --tmpfs /var/run \
  --cap-drop ALL myspa
```

## Gotchas
- Without `try_files` deep links return 404 on refresh.
- `index.html` cached by a CDN for a day means users load old asset hashes that no longer
  exist; keep it `no-cache`.
- Angular 17+ outputs to `dist/<app>/browser`; copy the right directory.

## Verify
```bash
curl -sI localhost:8080/some/deep/link | head -1     # 200
curl -sI localhost:8080/assets/index-abc123.js | grep -i cache-control
docker exec <c> id                                    # uid=101(nginx)
```

## Checked

- Date: 2026-11-02.
- Confirmed against: try_files fallback to index.html (nginx core module docs); nginx image config locations (Docker Hub nginx page).
- Not confirmed: unprivileged image port and entrypoint.d behaviour, cache-header values and gzip_types (Docker Hub nginx-unprivileged page returned a stub) (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
