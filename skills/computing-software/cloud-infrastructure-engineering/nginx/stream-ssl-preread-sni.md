---
id: computing-software.cloud-infrastructure-engineering.nginx.stream-ssl-preread-sni
name: stream-ssl-preread-sni
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, ssl-preread, sni-routing, stream, passthrough]
level: practitioner
status: docs-checked
description: "Routing TLS by SNI without terminating it using ngx_stream_ssl_preread_module, a map on $ssl_preread_server_name, and PROXY protocol."
sources: ["https://nginx.org/en/docs/stream/ngx_stream_ssl_preread_module.html", "https://nginx.org/en/docs/stream/ngx_stream_core_module.html", "https://nginx.org/en/docs/stream/ngx_stream_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`ngx_stream_ssl_preread_module` (1.11.5; not built by default, needs `--with-stream_ssl_preread_module`) extracts information from the ClientHello without terminating SSL/TLS. `ssl_preread` is `off` by default (contexts `stream`, `server`).

```nginx
stream {
    map $ssl_preread_server_name $upstream {
        api.example.com   api_pool;
        db.example.com    db_pool;
        default           web_pool;
    }
    upstream api_pool { server 10.0.0.10:443; }
    upstream db_pool  { server 10.0.0.20:443; }
    upstream web_pool { server 10.0.0.30:443; }

    server {
        listen 443;
        ssl_preread on;
        preread_timeout 10s;
        proxy_pass $upstream;
        proxy_protocol on;           # PROXY protocol v1 to the backend
    }
}
```

- Variables: `$ssl_preread_server_name` (SNI name), `$ssl_preread_alpn_protocols` (ALPN list, comma separated), `$ssl_preread_protocol` (highest SSL protocol version the client supports, 1.15.2). The module page also shows routing on ALPN and on protocol version (an empty `$ssl_preread_protocol` for SSH on the same port).
- `preread_timeout` (default `30s`) is the timeout of the preread phase; `preread_buffer_size` defaults to `16k`.
- `proxy_protocol on` enables version 1 of the PROXY protocol (text) for connections to the proxied server. `v2` is documented from 1.31.4.
- To receive the PROXY protocol on a `listen`, add the `proxy_protocol` parameter there; `proxy_protocol_timeout` defaults to 30s.

## Checked
Date: 2026-11-03.
Confirmed in the ssl_preread, stream core and stream proxy module pages: all of the above.
Removed as unconfirmed: the encrypted ClientHello adoption remark, claims about clients without SNI, the "breaks every connection" warning, the mTLS/HTTP-rules remark, and the stand-alone verify step.
Method: documentation only; no commands were run.
