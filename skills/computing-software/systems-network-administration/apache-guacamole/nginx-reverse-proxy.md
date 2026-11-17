---
id: computing-software.systems-network-administration.apache-guacamole.nginx-reverse-proxy
name: nginx-reverse-proxy
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, nginx, reverse-proxy, ssl-termination, websocket, proxy-buffering, client-max-body-size, x-forwarded-for]
level: practitioner
status: docs-checked
description: "Proxy Guacamole behind Nginx: WebSocket upgrade headers, proxy_buffering off, X-Forwarded-For and a raised client_max_body_size."
sources:
  - https://guacamole.apache.org/doc/gug/reverse-proxy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nginx reverse proxy

```nginx
location /guacamole/ {
    proxy_pass http://HOSTNAME:8080;
    proxy_buffering off;
    proxy_http_version 1.1;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $http_connection;
    client_max_body_size 1g;
    access_log off;
}
```
Why each line:
- `proxy_buffering off`: do not forget it; Nginx buffers by default and excessive buffering blocks the HTTP tunnel, so Guacamole may not work.
- `Upgrade` / `Connection` headers: must be set explicitly for WebSocket through Nginx.
- `X-Forwarded-For`: passes the client IP to the web application server (Tomcat needs the RemoteIpValve to use it; see apache-guacamole.tomcat-remoteipvalve). Guacamole uses the remote IP for auditing logins and connections.
- `client_max_body_size`: Nginx limits uploads to 1 MB by default; the resulting errors can be non-intuitive (for example "permission denied"). The manual's example sets `1g`.
- `access_log off` is part of the manual's example location block.

Terminate TLS in this server block (see apache-guacamole.security-hardening-overview). Port 8080 is the servlet container's default, and the manual recommends a proxy so Tomcat can run unprivileged.

Verify: a session shows the desktop and a file upload larger than 1 MB succeeds.

## Checked

2026-11-08. Read the whole of the reverse proxy page (reverse-proxy.html) and confirmed the Nginx location block, proxy_buffering, Upgrade and Connection headers, X-Forwarded-For, the 1 MB upload default with client_max_body_size, and the reasons for proxying. Removed the claims that the missing buffering setting shows a blank display, that X-Forwarded-For is needed for auth-ban and host restrictions specifically, and the stated purpose of access_log off (none on the page).
Method: documentation only; no commands were run.
