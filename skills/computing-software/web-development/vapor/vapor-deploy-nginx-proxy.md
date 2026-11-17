---
id: computing-software.web-development.vapor.vapor-deploy-nginx-proxy
name: vapor-deploy-nginx-proxy
category: computing-software
field: web-development
product: vapor
tags: [vapor, vapor-nginx, nginx, reverse-proxy, tls, static-files, deployment]
level: practitioner
status: docs-checked
description: "Put Nginx in front of a Vapor server as a reverse proxy: install, site config with proxy_pass, serving Public files directly, and TLS settings."
sources:
  - https://docs.vapor.codes/deploy/nginx/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: bind Vapor to an internal port and let Nginx face the internet. The docs recommend proxying Vapor behind Nginx for performance, security and ease of use; the proxy can force TLS, rate limit, or serve public files.

## Model
Bind Vapor to a port such as 8080 (ports above 1024 need no sudo); it is then unreachable from outside. Nginx listens on 80 (443 for HTTPS) and forwards to it.

## Install
- Ubuntu: `sudo apt-get update` then `sudo apt-get install nginx`
- CentOS / Amazon Linux: `sudo yum install nginx`
- Fedora: `sudo dnf install nginx`

Check by visiting the server IP in a browser. Control: `sudo service nginx stop|start|restart`. You also need a way to start and stop Vapor itself; the page points to Supervisor.

## Proxy config
Site configs are in `/etc/nginx/sites-enabled/` (copy a template from `/etc/nginx/sites-available/`). Example for project `Hello` binding to 8080 in production mode:

```sh
server {
    server_name hello.com;
    listen 80;

    root /path/to/vapor-home/Hello/Public/;

    location @proxy {
        proxy_pass http://127.0.0.1:8080;
        proxy_pass_header Server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 3s;
        proxy_read_timeout 10s;
    }
}
```

## Serve static files from Nginx
Frees Vapor under heavy load:

```sh
location / {
    try_files $uri @proxy;
}
```

## TLS
Generate free certificates with Let's Encrypt, then add to the server block:

```sh
listen 443 ssl;
ssl_certificate /etc/letsencrypt/live/hello.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/hello.com/privkey.pem;
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_dhparam /etc/ssl/certs/dhparam.pem;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_stapling on;
ssl_stapling_verify on;
add_header Strict-Transport-Security max-age=15768000;
```

The page also sets a long `ssl_ciphers` list (see the source page for the exact string). It calls these relatively strict settings; some are not required but enhance security.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) deploy/nginx, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
