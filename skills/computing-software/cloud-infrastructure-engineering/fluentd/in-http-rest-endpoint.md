---
id: computing-software.cloud-infrastructure-engineering.fluentd.in-http-rest-endpoint
name: in-http-rest-endpoint
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, in-http, http, rest, content-type, cors, curl]
level: practitioner
status: docs-checked
description: "Accept events over HTTP with in_http: tag from the URL path, json/ndjson/msgpack bodies by Content-Type, time override, header and query capture, CORS and size limits."
sources:
  - https://docs.fluentd.org/input/http
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in_http
```
<source>
  @type http
  port 9880
  bind 0.0.0.0
  body_size_limit 32m
  keepalive_timeout 10s
</source>
```
The URL path is the tag. Default Content-Type is `application/x-www-form-urlencoded`, which needs a prefix:
```
curl -X POST -d 'json={"foo":"bar"}' http://localhost:9880/app.log
curl -X POST -d '{"foo":"bar"}' -H 'Content-Type: application/json' http://localhost:9880/app.log
```
Formats: `json`, `ndjson`, `msgpack` (the `ndjson=` and `msgpack=` prefixes work the same way). Timestamps are assigned on arrival; override with `?time=1518756037.3137116`.

Parameters:
- `port` (9880), `bind`, `backlog`, `body_size_limit` (32MB), `keepalive_timeout` (10s).
- `decompression_size_limit` (1.19.3, 256MB): for `Content-Encoding` gzip or deflate; exceeding it returns `400 Bad Request`.
- `add_http_headers` (`HTTP_` prefix), `add_query_params` (1.12.0, `QUERY_` prefix, upper case), `add_remote_addr` (`REMOTE_ADDR`; the first `X-Forwarded-For` host).
- `add_tag_prefix` (1.18.0): `backend` makes `/app.log` tag `backend.app.log`.
- `cors_allow_origins` (`["*"]` allowed since 1.2.6), `cors_allow_credentials` (1.14.0). Since 1.19.0 empty `Origin` requests are allowed.
- `respond_with_empty_img`, `use_204_response` (1.8.0), `dump_error_log` (1.11.1) false to silence 400/500 logs.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/input/http and confirmed: port, bind, size limits, header and query capture, tag prefix, CORS, response options. Removed or reworded: nothing.

Method: documentation only; no commands were run.
