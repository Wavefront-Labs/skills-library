---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.nginx-custom-template
name: nginx-custom-template
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, nginx-conf, nginx-http-include, custom-template, penlight]
level: advanced
status: docs-checked
description: "Add a custom Nginx server block via nginx_http_include, or replace Kong's Nginx template with --nginx-conf, keeping placeholders like ${{LOG_LEVEL}}."
sources:
  - https://developer.konghq.com/gateway/nginx-directives/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Nginx include and template

## Include a file

Write a custom `server` block to a file such as `my-server.kong.conf`, then point Kong at it:

```
nginx_http_include = ./my-server.kong.conf
```

or set `KONG_NGINX_HTTP_INCLUDE`. Relative paths resolve against `prefix` or the `-p` flag of `kong start`. The docs example listens on port 2112 and returns 200.

## Replace the template

Pass `--nginx-conf` to `kong start`, `reload` or `restart`:

```
kong start -c kong.conf --nginx-conf custom_nginx.template
```

Templates use the Penlight templating engine, which supports `pairs`, `ipairs`, `tostring` and `os.getenv`.

Kong's default template is split into `nginx.lua`, which includes `nginx_kong.lua`. At startup these are copied into the prefix as `nginx.conf` and `nginx-kong.conf`.

To change something `kong.conf` does not expose, inline the contents of `nginx_kong.lua` into your own file and keep the placeholders, for example `${{NGINX_WORKER_PROCESSES}}`, `${{LOG_LEVEL}}` and `${{DNS_RESOLVER}}`.

Use a custom template for values that are not adjustable in `kong.conf`, or to embed Kong in an already running OpenResty instance.

## Checked

2026-11-04. Confirmed against the Nginx directives page: `nginx_http_include` and `KONG_NGINX_HTTP_INCLUDE`, relative-path rule, the port 2112 example, `--nginx-conf` on start, reload and restart, Penlight and its four functions, the `nginx.lua` and `nginx_kong.lua` split copied to `nginx.conf` and `nginx-kong.conf`, and the placeholders. Replaced an access-log sentence copied from a different page with the page's two use cases.
Method: documentation only; no commands were run.
