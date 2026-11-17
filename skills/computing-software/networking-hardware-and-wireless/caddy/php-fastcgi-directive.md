---
id: computing-software.networking-hardware-and-wireless.caddy.php-fastcgi-directive
name: php-fastcgi-directive
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [php-fastcgi, php-fpm, try-files, index-php, expanded-form, caddyfile, laravel]
level: practitioner
status: docs-checked
description: "Serve PHP apps with php_fastcgi: syntax, defaults for split, index and try_files, the expanded route it replaces, and the root plus file_server pairing."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/php_fastcgi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run PHP behind php-fpm with sensible routing.

`php_fastcgi [<matcher>] <php-fpm_gateways...> { root  split  index  try_files  env  resolve_root_symlink  capture_stderr  dial_timeout  read_timeout  write_timeout  <any reverse_proxy subdirectives> }`. Gateways are TCP or unix socket addresses. It assumes `index.php` at the root acts as a router; most modern apps need no subdirectives.

Defaults: `split .php` (first match splits PATH_INFO from the script name), `index index.php` (`off` disables the index.php fallback), `try_files {path} {path}/index.php index.php`, `dial_timeout 3s`, read and write timeouts none. `resolve_root_symlink` supports deployments that swap a symlink (off by default to avoid repeated system calls). `env` adds variables; the client `Proxy` header is never exposed as `HTTP_PROXY` (httpoxy).

Expanded form, in one `route`: (1) a 308 redirect that adds a trailing slash when `{path}/index.php` exists and the path lacks one; (2) a `file` matcher with `try_files {path} {path}/index.php index.php`, policy `first_exist_fallback`, `split_path .php`, then `rewrite`; (3) `reverse_proxy` for `path *.php` with `transport fastcgi { split .php }`. Non-PHP files fall through, so it should almost always be paired with `root` (often `/var/www/html/public`) and `file_server`.

Examples: `php_fastcgi 127.0.0.1:9000`; `php_fastcgi /blog/* localhost:9000`; `php_fastcgi unix//run/php/php8.2-fpm.sock`. For apps without an index.php entrypoint use `try_files {path} {path}/index.php =404` plus `handle_errors`.

## Checked

2026-11-03: read caddyfile/directives/php_fastcgi against this skill. Confirmed: syntax and subdirectives, defaults (split .php, index index.php or off, dial_timeout 3s), resolve_root_symlink, capture_stderr, env and httpoxy note, expanded form with 308 redirect, examples including the php8.2 socket.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
