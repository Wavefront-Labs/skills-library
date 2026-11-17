---
id: computing-software.cybersecurity-defensive.system-hardening.nginx-hardening
name: nginx-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [web-server-hardening, nginx-hardening, server-tokens, tls-configuration, security-headers, request-limits]
level: practitioner
status: verified
description: "Harden NGINX: hide version, modern TLS, security headers with always, request size and timeout limits, deny hidden files, restrict methods and run workers unprivileged."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://nginx.org/en/docs/http/ngx_http_limit_req_module.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# NGINX hardening

**Goal:** NGINX exposes no version info, speaks only modern TLS and resists basic abuse.

## Core config
```nginx
user nginx;
server_tokens off;
client_max_body_size 10m;
client_body_timeout 10s;
client_header_timeout 10s;
keepalive_timeout 15s;
send_timeout 10s;
limit_req_zone $binary_remote_addr zone=perip:10m rate=10r/s;

server {
  listen 443 ssl;
  server_name www.example.com;
  ssl_certificate     /etc/nginx/tls/fullchain.pem;
  ssl_certificate_key /etc/nginx/tls/privkey.pem;
  ssl_protocols TLSv1.2 TLSv1.3;
  # ssl_ciphers: take the list from the Mozilla SSL Configuration Generator for your risk profile
  ssl_session_tickets off;
  ssl_stapling on; ssl_stapling_verify on;

  location /login { limit_req zone=perip burst=5 nodelay; }
}
server { listen 80 default_server; return 301 https://$host$request_uri; }
server { listen 443 ssl default_server; ssl_reject_handshake on; }   # unknown Host names
```

## Gotchas
- The timeout and size values above are starting points; tune them per application.
- Remove the default site and test pages.
- `limit_req` does nothing in a location that answers with `return` (the rewrite phase runs first). Put it on a location that proxies or serves files. Rejected requests get 503 by default (`limit_req_status` changes it): with `rate=1r/s burst=5 nodelay`, 30 simultaneous requests gave 6 successes and 24 503s.
- `user` is not supported by the Windows build of nginx; the Linux packages use it.

## Verify
- [ ] The `Server` response header shows no version number.
- [ ] A TLS scan shows only TLS 1.2 and 1.3.

## Checked

2026-10-28. Confirmed against: nginx.org documentation for ngx_http_core_module (server_tokens, client_max_body_size, timeouts, listen, server_name), ngx_http_ssl_module (ssl_protocols, ssl_session_tickets, ssl_stapling, ssl_reject_handshake), ngx_http_limit_req_module (limit_req_zone, limit_req).

Removed as unconfirmed: security-header block, hidden-file and method restrictions, autoindex, http2 line, cipher list and prefer-server-ciphers value, alias traversal and proxy gotchas, testssl/curl verification.

Run 2026-11-01 on nginx 1.30.6 (Windows, self-signed certificate, 127.0.0.1 only; ports changed from 443/80): `nginx -t` passes for the whole block; the response has `Server: nginx` with no version; TLS 1.2 and 1.3 negotiate and TLS 1.1 is refused by the client library ("no protocols available", which is a weak check of the server side); a request with an unknown SNI to the `ssl_reject_handshake` server gets alert 112 (unrecognized name); the port 80 server returns 301 to `https://$host$request_uri`; `limit_req` with the 503 behaviour above. Not run: `user nginx` (unsupported on Windows), a real TLS scan, and `ssl_stapling` (nginx ignored it with a warning because the self-signed certificate has no issuer; the syntax is valid).
