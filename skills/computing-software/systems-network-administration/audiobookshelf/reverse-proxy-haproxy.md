---
id: computing-software.systems-network-administration.audiobookshelf.reverse-proxy-haproxy
name: reverse-proxy-haproxy
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [reverse-proxy, haproxy, acl, backend, http2, alpn]
level: advanced
status: docs-checked
description: "Route Audiobookshelf through HAProxy with a host ACL, a dedicated backend and TLS with ALPN for http2."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/reverse-proxy/8.ha-proxy-setup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generic config on the docs page using `audiobookshelf.YOUR_DOMAIN.COM`:

```haproxy
frontend my_frontend
    bind :443 name :443 ssl crt-list /path/to/cert.crt_list alpn h2,http/1.1
    mode http
    acl is_audiobookshelf hdr_beg(host) -i audiobookshelf
    use_backend audiobookshelf_backend if is_audiobookshelf
    default_backend default_backend

backend audiobookshelf_backend
    mode http
    server audiobookshelf_server 127.0.0.99:13378

backend default_backend
    mode http
    server default_server 127.0.0.123:8081
```

Keep your own `global` and `defaults` sections (the page shows them as placeholders; `defaults` has `mode http`). To use `http2`, `ssl` is needed, which is why the `bind` line carries `ssl` and `alpn h2,http/1.1`.

The docs also link a separate pfSense and HAProxy page for additional security.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: HAProxy page.

Method: documentation only; no commands were run.
