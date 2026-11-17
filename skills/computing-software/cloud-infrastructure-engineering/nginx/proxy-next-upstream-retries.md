---
id: computing-software.cloud-infrastructure-engineering.nginx.proxy-next-upstream-retries
name: proxy-next-upstream-retries
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, proxy-next-upstream, retries, failover, idempotent]
level: advanced
status: docs-checked
description: "Controlling when nginx retries another upstream server, including non-idempotent request limits and tries/time caps."
sources: ["https://nginx.org/en/docs/http/ngx_http_proxy_module.html", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`proxy_next_upstream` lists the conditions that pass a request to the next server. Default: `error timeout`.

```nginx
proxy_next_upstream error timeout http_502 http_503;
proxy_next_upstream_tries   3;     # limit on the number of tries
proxy_next_upstream_timeout 10s;   # limit on the time spent passing to next servers
```

- `proxy_next_upstream_tries` and `proxy_next_upstream_timeout` both default to `0`, which turns the limit off.
- Valid conditions: `error`, `timeout`, `invalid_header`, `http_500`, `http_502`, `http_503`, `http_504`, `http_403`, `http_404`, `http_429`, `non_idempotent`, `off` (`denied` is commercial subscription only).
- Requests with a non-idempotent method (POST, LOCK, PATCH) are not passed to the next server once the request has been sent to an upstream, unless `non_idempotent` is set. Setting it allows retrying such requests, so only use it where a duplicate is harmless.
- A request can only be passed on if nothing has been sent to the client yet; an error mid-response cannot be retried.
- `error`, `timeout` and `invalid_header` always count as unsuccessful attempts; `http_500`, `http_502`, `http_503`, `http_504` and `http_429` count only if listed; `http_403` and `http_404` never count.
- Unsuccessful attempts feed `max_fails`/`fail_timeout` on the `upstream` `server` line, which decides when a server is skipped.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_proxy_module page: the directive syntax, defaults, every condition, non_idempotent wording, the nothing-sent-to-client rule, what counts as unsuccessful. Confirmed in ngx_http_upstream_module: max_fails/fail_timeout defined by the next_upstream directives.
Removed as unconfirmed: the advice that http_500 multiplies load, the dead-backend curl verify step.
Method: documentation only; no commands were run.
