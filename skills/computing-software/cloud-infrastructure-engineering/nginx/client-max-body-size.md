---
id: computing-software.cloud-infrastructure-engineering.nginx.client-max-body-size
name: client-max-body-size
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, client-max-body-size, 413, uploads, client-body-buffer-size, request-body]
level: intro
status: docs-checked
description: "Handling request bodies in nginx: client_max_body_size default 1m and 413 errors, client_body_buffer_size, temp files and proxy_request_buffering."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`client_max_body_size` (default `1m`; contexts `http`, `server`, `location`) sets the largest allowed request body. A larger body gets `413 (Request Entity Too Large)`; browsers cannot correctly display this error. `0` disables the check.

```nginx
http {
    client_max_body_size 1m;
}
location /upload/ {
    client_max_body_size 200m;
    client_body_buffer_size 128k;
    client_body_temp_path /var/cache/nginx/body 1 2;
    client_body_timeout 30s;
    proxy_request_buffering off;
    proxy_pass http://app;
}
```

- `client_body_buffer_size` (default `8k|16k`, two memory pages) is the read buffer; a larger body is written wholly or partly to a temporary file.
- `client_body_temp_path path [level1 [level2 [level3]]]` sets the temp directory with up to three subdirectory levels.
- `client_body_timeout` (default `60s`) applies between two successive reads, not to the whole body; if the client sends nothing in that time the request ends with `408 (Request Time-out)`.
- `proxy_request_buffering` (default `on`): the whole body is read from the client before the request goes to the proxied server. With `off` the body is sent as it arrives and the request cannot be passed to the next server once sending has started. A chunked request body is buffered regardless unless HTTP/1.1 or HTTP/2 is enabled for proxying.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_core_module` page (client_max_body_size, client_body_* directives and defaults) and `ngx_http_proxy_module` (`proxy_request_buffering`). Removed: PHP and Express limit claims, the error log message text, claims about enforcement of chunked uploads, and the dd/curl Verify step.
Method: documentation only; no commands were run.
