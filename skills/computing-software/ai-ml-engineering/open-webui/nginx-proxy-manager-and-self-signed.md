---
id: computing-software.ai-ml-engineering.open-webui.nginx-proxy-manager-and-self-signed
name: nginx-proxy-manager-and-self-signed
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [https-nginx, nginx-proxy-manager, self-signed, windows, lan, microphone]
level: practitioner
status: docs-checked
description: "Give a home or LAN Open WebUI HTTPS using Nginx Proxy Manager with DuckDNS, or a self-signed certificate on dockerised or Windows Nginx."
sources:
  - https://docs.openwebui.com/reference/https/nginx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: HTTPS on a home or internal server so browsers allow microphone input (most refuse it on non-localhost http).

## Option A: Nginx Proxy Manager (NPM)
1. Compose service `jc21/nginx-proxy-manager:latest` with ports `80:80`, `81:81`, `443:443` and volumes `./data:/data`, `./letsencrypt:/etc/letsencrypt`; `docker compose up -d`.
2. Create a domain (for example on DuckDNS) pointing at the proxy host's local IP; get the DuckDNS API token.
3. Open `http://server_ip:81`, log in with `admin@example.com` / `changeme` and change them. SSL Certificates > Add > Let's Encrypt: enter the email and both the wildcard and bare name (for example `*.hello.duckdns.org` and `hello.duckdns.org`), choose "Use a DNS challenge", DuckDNS, paste `dns_duckdns_token=<token>`; raise propagation time (for example 120 s) if needed.
4. Proxy Hosts > Add: domain `openwebui.hello.duckdns.org`, scheme HTTP, host IP of the Open WebUI machine, enable "Websockets support", select the certificate, Force SSL, HTTP/2.
5. Advanced tab > Custom Nginx Configuration:
```nginx
proxy_buffering off;
proxy_cache off;
proxy_read_timeout 1800;
proxy_send_timeout 1800;
proxy_connect_timeout 1800;
```
(The default 60 s timeout cuts long completions.)
6. Set `CORS_ALLOW_ORIGIN="https://openwebui.hello.duckdns.org"` on Open WebUI (critical; semicolon-separated list allowed). Also enter your URL in Settings > Admin > General (the docs call it the Webhook URL field) to avoid an HTTPS error.
If you add custom caching rules, exclude `/api/`, `/auth/`, `/signup/`, `/signin/`, `/sso/`, `/admin/`, `/signout/`, `/oauth/`, `/login/`, `/logout/`. Local firewall software such as Portmaster can block Docker network traffic.

## Option B: self-signed on dockerised Nginx
```bash
mkdir -p conf.d ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/nginx.key -out ssl/nginx.crt -subj "/CN=your_domain_or_IP"
```
`conf.d/open-webui.conf`: `listen 443 ssl; ssl_certificate /etc/nginx/ssl/nginx.crt; ssl_certificate_key /etc/nginx/ssl/nginx.key; ssl_protocols TLSv1.2 TLSv1.3;` with the same location blocks as the Let's Encrypt skill, proxying to `http://host.docker.internal:3000`. Compose: `nginx:alpine`, port `443:443`, volumes `./conf.d` mounted at `/etc/nginx/conf.d` and `./ssl:/etc/nginx/ssl`, `depends_on: open-webui`. Run `docker compose up -d nginx` and open `https://your_domain_or_IP` (browser will warn).

## Option C: Windows without Docker (pip install, `open-webui serve`)
Install OpenSSL (SLP binaries or `choco install openssl -y`; check `openssl version`) and unzip Nginx from nginx.org. Generate `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx.key -out nginx.crt`. In `nginx.conf` use a `map $http_upgrade $connection_upgrade { default upgrade; '' close; }`, redirect port 80 to HTTPS, listen 443 ssl on your LAN IP (from `ipconfig`), and `proxy_pass http://localhost:8080` with `Connection $connection_upgrade`, buffering and cache off, read timeout 1800. Validate with `nginx -t`, start with `nginx`, reload with `nginx -s reload`; allow Windows Firewall access.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page reference/https/nginx and its three tab sources reference/tab-nginx/NginxProxyManager, SelfSigned and Windows (all read in full): the NPM Compose service and ports, DuckDNS setup, default login, wildcard plus bare certificate with DNS challenge and token format, propagation time, proxy host settings, the buffering and 1800 second timeout directives, the CORS_ALLOW_ORIGIN warning with a semicolon-separated list, the Webhook URL step, the caching exclusion paths and the Portmaster note; the self-signed docker steps with openssl command, location blocks and Compose service; and the Windows pip-install flow with openssl, nginx.conf map and redirect, nginx -t, nginx -s reload and firewall note. Nothing removed.
Method: documentation only; no commands were run.
