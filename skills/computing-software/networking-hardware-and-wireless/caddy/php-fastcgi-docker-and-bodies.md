---
id: computing-software.networking-hardware-and-wireless.caddy.php-fastcgi-docker-and-bodies
name: php-fastcgi-docker-and-bodies
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [php-fastcgi, docker, multiple-sites, request-buffers, 411-length-required, root, caddyfile]
level: advanced
status: docs-checked
description: "Run several PHP apps or Docker php-fpm with php_fastcgi: separate roots per site, the root subdirective, and the 411 Length Required body-buffering rule."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/php_fastcgi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid two common php_fastcgi pitfalls.

Different roots: when Caddy serves several PHP apps, each app needs a distinct webroot in Caddy so it can read static files separately and detect whether PHP files exist. Under Docker the php-fpm containers often mount the files at the same path, so mount them into the Caddy container in different directories and set `root` inside `php_fastcgi` to the path php-fpm sees. The page's pattern: `app1.example.com { root /srv/app1/public  php_fastcgi app1:9000 { root /var/www/html/public }  file_server }` and the same for `app2` with `/srv/app2/public`. The outer `root` is Caddy's view of the files; the inner one is php-fpm's view.

Request body length: FastCGI needs the body length up front. A request with a body but no `Content-Length` (chunked, or HTTP/2 and HTTP/3 without the header) gets `411 Length Required` unless the whole body fits in the `request_buffers` buffer. The buffer must be larger than the body; a body exactly the buffer size is still rejected. `request_buffers unlimited` buffers any size, but the page advises limiting sizes with `request_body { max_size ... }`.

Since `php_fastcgi` accepts all `reverse_proxy` subdirectives, set `request_buffers` inside the same block.

## Checked

2026-11-03: read caddyfile/directives/php_fastcgi against this skill. Confirmed: per-app webroot pattern with an inner root, 411 Length Required for bodies without Content-Length, request_buffers advice.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
