---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-fastcgi-transport
name: reverse-proxy-fastcgi-transport
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [fastcgi, php, transport, path-info, capture-stderr, httpoxy, reverse-proxy]
level: advanced
status: docs-checked
description: "Talk FastCGI from reverse_proxy with transport fastcgi: root, split for PATH_INFO, env, symlink resolution, timeouts and stderr capture."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: proxy to a FastCGI server such as php-fpm.

Block: `transport fastcgi { root <path>  split <at>  env <key> <value>  resolve_root_symlink  dial_timeout  read_timeout  write_timeout  capture_stderr }`.

- `root`: the site root; default `{http.vars.root}` or the working directory.
- `split`: where to split the path to produce PATH_INFO at the end of the URI.
- `env`: extra environment variable, repeatable. Standard CGI variables (including `SERVER_ADDR`) and request headers as `HTTP_*` are set by default. To mitigate httpoxy, the client's `Proxy` header is never passed as `HTTP_PROXY`.
- `resolve_root_symlink`: resolve the root through a symbolic link.
- `dial_timeout` default `3s`; `read_timeout` and `write_timeout` default none.
- `capture_stderr`: log messages the FastCGI server writes to stderr, at WARN, or ERROR when the response is 4xx/5xx. Ignored by default.

Request bodies without a `Content-Length` need `request_buffers`, because the transport requires a length (with `unlimited` the entire body is buffered and the header set).

For modern PHP applications the page points to `php_fastcgi`, a shortcut that adds the rewrites for `index.php` routing.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
