---
id: computing-software.ai-ml-engineering.open-webui.haproxy-reverse-proxy
name: haproxy-reverse-proxy
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [https-tunnels, haproxy, lets-encrypt, certbot, websocket, load-balancing]
level: advanced
status: docs-checked
description: "Front Open WebUI with HAProxy using subdomain or path routing, Let's Encrypt via certbot, long timeouts, and the HTTP/2 WebSocket workaround."
sources:
  - https://docs.openwebui.com/reference/https/haproxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: HTTPS and routing for Open WebUI in HAProxy, with working WebSockets.

## Install
Red Hat family: `sudo dnf install haproxy certbot openssl -y`. Debian family: `sudo apt install haproxy certbot openssl -y`. Config lives in `/etc/haproxy/haproxy.cfg`. Ports 80 and 443 must reach the HAProxy host (Let's Encrypt validation and HTTPS); at home forward them on the router and point DNS at it.

## Config essentials
`global`: `maxconn 4000`, `user haproxy`, `group haproxy`, `daemon`, `tune.ssl.default-dh-param 2048`, `chroot /var/lib/haproxy`.

`defaults` (long LLM responses need generous timeouts): `mode http`, `option httplog`, `option forwardfor`, `option http-server-close`, `option redispatch`, `retries 3`, `timeout http-request 300s`, `timeout queue 2m`, `timeout connect 120s`, `timeout client 10m`, `timeout server 10m`, `timeout http-keep-alive 120s`, `timeout check 10s`, `maxconn 3000`.

Frontend and backends:
```
frontend web
    bind 0.0.0.0:80
    bind 0.0.0.0:443 ssl crt /path/to/ssl/folder/
    acl letsencrypt-acl path_beg /.well-known/acme-challenge/
    use_backend letsencrypt-backend if letsencrypt-acl
    # subdomain method
    acl chat-acl hdr(host) -i subdomain.domain.tld
    # or path method
    # acl chat-acl path_beg /owui/
    use_backend owui_chat if chat-acl

backend letsencrypt-backend
    server letsencrypt 127.0.0.1:8688

backend owui_chat
    option forwardfor
    http-request add-header X-CLIENT-IP %[src]
    http-request set-header X-Forwarded-Proto https if { ssl_fc }
    server chat <ip>:3000
```
WebSockets need TLS configured; Let's Encrypt is the easy path.

## HTTP/2 and WebSockets
HAProxy 3.x may enable HTTP/2 by default and WebSockets over an H2 tunnel (RFC 8441) can freeze the UI. Add `option h2-workaround-bogus-websocket-clients` to `defaults` or `frontend` so clients fall back to HTTP/1.1 Upgrade; keep the backend on HTTP/1.1 (default in `mode http`).

## Certificates
1. Placeholder cert so HAProxy can start: `openssl req -x509 -newkey rsa:2048 -keyout /tmp/haproxy.key -out /tmp/haproxy.crt -days 3650 -nodes -subj "/CN=localhost"` then `cat /tmp/haproxy.crt /tmp/haproxy.key > /etc/haproxy/certs/haproxy.pem`.
2. Validate and start: `haproxy -c -f /etc/haproxy/haproxy.cfg`, `systemctl start haproxy`, `systemctl enable haproxy`.
3. `certbot register --agree-tos --email your@email.com --non-interactive`, then `certbot certonly -n --standalone --preferred-challenges http --http-01-port 8688 -d yourdomain.com` (port 8688 matches the letsencrypt backend).
4. Merge for HAProxy: `cat /etc/letsencrypt/live/{domain}/fullchain.pem /etc/letsencrypt/live/{domain}/privkey.pem > /etc/haproxy/certs/{domain}.pem`, `chmod 600`, `chown haproxy:haproxy`, then `systemctl restart haproxy`.

## Gotchas
- Optional helper: the third-party haproxy-manager container (github.com/shadowdao/haproxy-manager) automates config and cert lifecycle; never expose its port 8000 publicly.
- The page's certbot line is printed as `--http-01-port-8688` (a typo); the working flag form is `--http-01-port 8688`, as written above.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page reference/https/haproxy (read in full): dnf and apt install commands, the config path, the global, defaults and frontend/backend directives and timeouts, subdomain versus path ACLs, the HTTP/2 WebSocket workaround option, the port 80 and 443 note, the placeholder certificate, validate and start commands, certbot register and certonly with port 8688, the merged PEM steps and the haproxy-manager warning about port 8000. Removed the WEBUI_URL and CORS_ALLOW_ORIGIN gotcha, which this page does not state. The page prints the certbot flag with a hyphen before 8688; the skill keeps the standard space-separated form and flags the typo.
Method: documentation only; no commands were run.
