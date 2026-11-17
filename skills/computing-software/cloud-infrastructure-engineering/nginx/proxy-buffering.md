---
id: computing-software.cloud-infrastructure-engineering.nginx.proxy-buffering
name: proxy-buffering
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, proxy-buffering, proxy-buffers, proxy-buffer-size, streaming]
level: practitioner
status: docs-checked
description: "How nginx proxy_buffering, proxy_buffer_size, proxy_buffers and temp-file limits work, and when X-Accel-Buffering turns buffering off."
sources: ["https://nginx.org/en/docs/http/ngx_http_proxy_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Defaults and meanings from the `ngx_http_proxy_module` page (contexts `http`, `server`, `location`):

- `proxy_buffering on | off;` default `on`. When on, nginx receives the response as soon as possible into the buffers set by `proxy_buffer_size` and `proxy_buffers`; if the whole response does not fit in memory, part can go to a temporary file. When off, the response is passed to the client synchronously as received, and the most nginx reads at a time is `proxy_buffer_size`.
- A proxied server can switch buffering per response with the `X-Accel-Buffering` header (`yes` or `no`); `proxy_ignore_headers` can disable that.
- `proxy_buffer_size` default `4k|8k` (one memory page): the buffer for the first part of the response, usually the header. If the header exceeds it, the response is considered invalid.
- `proxy_buffers number size` default `8 4k|8k`: buffers per connection.
- `proxy_busy_buffers_size` default `8k|16k`: limits the buffers that can be busy sending to the client while the response is not fully read.
- `proxy_max_temp_file_size` default `1024m`: maximum temporary file size; `0` disables buffering of responses to temporary files. It does not apply to cached or stored responses. `proxy_temp_file_write_size` limits data written per write.
- `proxy_temp_path path [level1 [level2 [level3]]]` sets the temp directory (default `proxy_temp`).
- `proxy_limit_rate` works only with buffering enabled.

```nginx
location /events {
    proxy_buffering off;
    proxy_pass http://app;
}
```

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_proxy_module` page. Removed: the 502 and "upstream sent too big header" error text, the temp-file log message, the slow-client note, the SSE and token streaming claims, the invented buffer sizes, and the curl Verify step.
Method: documentation only; no commands were run.
