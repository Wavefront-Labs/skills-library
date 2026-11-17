---
id: computing-software.cloud-infrastructure-engineering.nginx.ssl-early-data
name: ssl-early-data
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, ssl-early-data, early-data, 0-rtt, replay, tls13]
level: practitioner
status: docs-checked
description: "TLS 1.3 early data in nginx: enabling ssl_early_data, passing $ssl_early_data to upstreams as Early-Data, and the replay-attack caveat."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://nginx.org/en/docs/http/server_names.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`ssl_early_data` (contexts `http`, `server`; default `off`; since 1.15.3) enables TLS 1.3 early data. It works with OpenSSL 1.1.1 or higher (1.15.4) and BoringSSL.

```nginx
ssl_protocols TLSv1.3;
ssl_early_data on;
location / {
    proxy_set_header Early-Data $ssl_early_data;
    proxy_pass http://app;
}
```

- Requests sent in early data are subject to replay attacks. The docs say to protect against them at the application layer with the `$ssl_early_data` variable, as above.
- `$ssl_early_data` is `1` if early data is used and the handshake is not complete, otherwise empty.
- OpenSSL's built-in replay protection is disabled because it interferes with session resumption. It can be turned back on with `ssl_conf_command Options AntiReplay;`.
- Specified at `server` level, the value comes from the default server (session resumption always starts from the default server context), so set `ssl_early_data`, `ssl_session_cache`, `ssl_session_tickets` and `ssl_session_timeout` on the default server.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_ssl_module page: ssl_early_data default, versions, replay wording, `$ssl_early_data`, AntiReplay option. Confirmed in the server_names page: default-server rule for session-related directives.
Removed as unconfirmed: the `425 Too Early` / RFC 8470 advice, "nginx does not reject early-data POSTs", shared ticket key and replay-window claims, and the openssl s_client verify step.
Method: documentation only; no commands were run.
