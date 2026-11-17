---
id: computing-software.devops-ci-cd.forgejo.reverse-proxy-subpath-and-sockets
name: reverse-proxy-subpath-and-sockets
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [subpath, unix-socket, fastcgi, fcgi-unix]
level: advanced
status: docs-checked
description: "Serve Forgejo on a URL subpath or over a Unix socket and FastCGI, and understand the subpath security caveat."
sources:
  - https://forgejo.org/docs/latest/admin/setup/reverse-proxy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Subpath: to serve on something like `http://example.com/code`, use `location /code/ { proxy_pass http://127.0.0.1:3000/; ... }` with the same proxy headers as the basic setup, and set Forgejo's `ROOT_URL` to the URL including the subpath, otherwise links are broken. Security warning: browsers treat the same origin as safe, so a subpath is unsafe if that origin hosts user-entered content under other subpaths; malicious content could host CSRF attacks against Forgejo, and Forgejo offers no protection against this.

Unix socket over HTTP: set `PROTOCOL = http+unix` in `[server]` and `HTTP_ADDR` to the socket file, for example `/run/forgejo.sock`. The page then says to adapt nginx to something like `proxy_pass http://unix:/run/forgejo.socket:/;`. Its own examples spell the socket `/run/forgejo.sock` for `HTTP_ADDR` and `/run/forgejo.socket` in `proxy_pass`, so use one path in both places.

FastCGI: set `PROTOCOL = fcgi+unix` and `HTTP_ADDR` to the socket path. The docs say FastCGI improves security because it is immune to desync attacks (request smuggling) and untrusted-header confusion issues. The nginx server block then uses `include fastcgi_params;` and `fastcgi_pass unix:/run/forgejo.sock;` inside `location /`.

## Checked

2026-11-04. Confirmed against the Forgejo Reverse proxy page (Security of subpath, HTTP with a subpath, HTTP with Unix socket, FastCGI with Unix socket): the subpath configuration, ROOT_URL, the CSRF warning, PROTOCOL values and the FastCGI claim. Recorded the page's inconsistent socket spelling, and replaced the generic FastCGI sentence with the page's nginx lines.

Method: documentation only; no commands were run.
