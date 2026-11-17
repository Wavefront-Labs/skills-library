---
id: computing-software.devops-ci-cd.gitea.reverse-proxy
name: reverse-proxy
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-reverse-proxy-nginx, gitea, nginx, apache-httpd, caddy, haproxy, iis-arr, root-url, websocket-upgrade, x-real-ip, sub-path]
level: practitioner
status: docs-checked
description: "Put Gitea behind nginx, Apache, Caddy, HAProxy or IIS: ROOT_URL, undecoded URIs, forwarded headers, /-/ws WebSocket, sub-path and /v2 registry rules."
sources: ["https://docs.gitea.com/administration/reverse-proxies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea behind a reverse proxy

## Rules for every proxy
1. `[server] ROOT_URL = https://git.example.com/`.
2. Pass `https://git.example.com/foo` to `http://gitea:3000/foo`.
3. Do **not** decode the URI: `/a%2Fb` must reach Gitea as `/a%2Fb`.
4. Pass `Host` and `X-Forwarded-Proto` so Gitea sees the real URL.
5. Serve a certificate that includes all intermediate and root CA certificates, or `git clone`/`pull` fail.
6. WebSocket at `/-/ws` (live notification counter): use HTTP/1.1 and forward `Upgrade` and `Connection`; without it Gitea falls back to polling.

## nginx
```nginx
location / {
    client_max_body_size 512M;      # too small gives 413 on large pushes/uploads
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Connection $http_connection;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
Sub-path: `location ~ ^/(gitea|v2)($|/)` with `rewrite ^ $request_uri;` then `rewrite ^/(gitea($|/))?(.*) /$3 break;` and `proxy_pass http://127.0.0.1:3000$uri;` (keeps `%2F`, strips `/gitea`, passes `/v2` as is). `ROOT_URL` must then end in `/gitea/`. The container registry needs a fixed `/v2` at the host root, so a sub-path setup must still route `/v2` to Gitea.
Static assets: run `make frontend` in a source snapshot and serve `public/`. Single domain: `STATIC_URL_PREFIX = /_/static` with `location /_/static/assets/ { alias /path/to/gitea/public/; }`. CDN: `STATIC_URL_PREFIX = http://cdn.example.com/gitea`.
Nginx Proxy Manager already adds proxy directives: only add `client_max_body_size 512M;` to the custom `/` location (duplicate `proxy_set_header Host $host` gives 400) and tick Websockets Support; adding `proxy_http_version` makes Nginx refuse to start.

## Apache HTTPD
Enable `proxy` and `proxy_http`:
```apacheconf
ProxyPreserveHost On
ProxyRequests off
AllowEncodedSlashes NoDecode
ProxyPass / http://localhost:3000/ nocanon upgrade=websocket
RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
```
`upgrade=websocket` needs Apache 2.4.48+; remove it on older versions or Apache will not start. For Let's Encrypt webroot add `ProxyPass /.well-known !` first. Sub-path: `ProxyPass /git http://localhost:3000 nocanon upgrade=websocket` (no trailing slashes) and `ROOT_URL .../git/`.

## Caddy
`git.example.com { reverse_proxy localhost:3000 }`. Sub-path: `route /git/* { uri strip_prefix /git; reverse_proxy localhost:3000 }` plus matching `ROOT_URL`.

## HAProxy
Frontend `acl acl_gitea hdr(host) -i gitea.example.com` and `use_backend gitea if acl_gitea`; backend `server localhost:3000 check`. TLS ends at HAProxy, so Gitea stays on HTTP. Sub-path ACL: `path_beg /gitea`.

## IIS
Needs ARR plus URL Rewrite and the `WebSocket Protocol` Windows feature. Inbound rule rewrites to `http://127.0.0.1:3000{UNENCODED_URL}` with `useOriginalURLEncoding="false"` and `requestPathInvalidCharacters=""`; add an outbound rule rewriting `http://127.0.0.1:3000/` links to the public host, and turn **Reverse rewrite host in response headers** off in ARR Server Proxy Settings or redirects after sign-in send browsers to `127.0.0.1:3000`.

## Checked

2026-11-03: read https://docs.gitea.com/administration/reverse-proxies/ line by line; the commands, options, defaults and values stated above match those pages.
Changed: Removed the unconfirmed X-Real-IP rule; certificate rule now says intermediate and root CA certificates.
Method: documentation only; no commands were run.
