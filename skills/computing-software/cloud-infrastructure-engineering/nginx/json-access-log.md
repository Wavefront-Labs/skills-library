---
id: computing-software.cloud-infrastructure-engineering.nginx.json-access-log
name: json-access-log
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, escape-json, log-format, escapejson, structured-logging, ndjson]
level: practitioner
status: docs-checked
description: "Producing JSON access logs in nginx with log_format escape=json, the default escaping, and numeric versus string fields."
sources: ["https://nginx.org/en/docs/http/ngx_http_log_module.html", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html", "https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`log_format name [escape=default|json|none] string ...;` (1.11.8 for `escape`; `none` since 1.13.10).

- Default escaping writes `"`, `\` and characters below 32 or above 126 as `\xXX`.
- `escape=json` escapes `"` and `\` as `\"` and `\\` and control characters as `\n`, `\r`, `\t`, `\b`, `\f` or `\u00XX`.
- `escape=json` only escapes the variable values; you write the surrounding quotes and braces in the format string.

```nginx
log_format json escape=json
  '{"ts":"$time_iso8601","remote":"$remote_addr","method":"$request_method",'
  '"uri":"$request_uri","status":$status,"bytes":$body_bytes_sent,'
  '"rt":$request_time,"urt":"$upstream_response_time","ua":"$http_user_agent",'
  '"req_id":"$request_id"}';
access_log /var/log/nginx/access.json json;
```

- `$status`, `$body_bytes_sent` and `$request_time` are single numeric values, so they can stay unquoted.
- `$upstream_response_time` holds a comma/colon separated list when several upstream connections were tried (and is not a plain number when unset), so the example quotes it.
- `$request_id` is a unique request identifier generated from 16 random bytes in hexadecimal (1.11.0). A variable whose value is not found is logged as a hyphen with default escaping.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_log_module` page (`log_format`, `escape`), `ngx_http_upstream_module` (`$upstream_response_time`) and `ngx_http_core_module` (`$request_id`, `$request_uri`, `$request_method`, `$body_bytes_sent`). Removed: pipe atomic-write size claim, the `X-Request-ID` forwarding advice, shipper names and the jq Verify step.
Method: documentation only; no commands were run.
