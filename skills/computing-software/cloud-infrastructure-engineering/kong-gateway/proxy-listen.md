---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.proxy-listen
name: proxy-listen
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, proxy-listen, reuseport, http2, listeners, kong-conf]
level: practitioner
status: docs-checked
description: "The kong.conf proxy_listen setting: default HTTP/HTTPS listeners on 8000 and 8443, listener flags such as ssl, http2, reuseport and backlog, and how to disable it."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proxy_listen

`proxy_listen` is the public entry point for client traffic. Default:

```
proxy_listen = 0.0.0.0:8000 reuseport backlog=16384, 0.0.0.0:8443 http2 ssl reuseport backlog=16384
```

It is a comma-separated list of `address:port` entries followed by Nginx listener flags such as `ssl`, `http2`, `reuseport` and `backlog=N`. Port 8000 serves plain HTTP; 8443 serves TLS with HTTP/2.

Set `proxy_listen` to `off` to disable the HTTP/HTTPS proxy port for the node. If `stream_listen` is also `off`, the node runs in control plane mode with all proxying disabled.

The TLS listener uses `ssl_cert` / `ssl_cert_key`. If unset, Kong auto-generates RSA and ECC default certificates at first start.

Environment form: `KONG_PROXY_LISTEN`.

The cipher set comes from `ssl_cipher_suite`; `ssl_protocols`, `ssl_ciphers` and `ssl_prefer_server_ciphers` are ignored unless `ssl_cipher_suite` is `custom`. The request body limit comes from `nginx_http_client_max_body_size`, where `0` disables checking.

## Checked

2026-11-04. Confirmed against kong.conf.default: the default value, flag meanings, `off` and control plane mode, auto-generated RSA and ECC certificates, the `ssl_*` interplay and the body size setting. Removed the example environment value and the hybrid sentence, which the page does not state.
Method: documentation only; no commands were run.
