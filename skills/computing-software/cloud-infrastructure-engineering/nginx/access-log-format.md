---
id: computing-software.cloud-infrastructure-engineering.nginx.access-log-format
name: access-log-format
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, log-format, access-log, combined, observability]
level: intro
status: docs-checked
description: "Defining a custom nginx log_format with upstream timing variables, the predefined combined format, and where access_log and log_format can appear."
sources: ["https://nginx.org/en/docs/http/ngx_http_log_module.html", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`access_log` defaults to `logs/access.log combined` and is valid in `http`, `server`, `location`, `if in location` and `limit_except`. `log_format` is valid only in `http`. The predefined `combined` format always exists.

```nginx
log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" "$http_user_agent" '
                'rt=$request_time uct=$upstream_connect_time urt=$upstream_response_time '
                'ua=$upstream_addr us=$upstream_status cs=$upstream_cache_status';
access_log /var/log/nginx/access.log main;
```

- `$request_time` is the time from the first bytes read from the client to the log write after the last bytes were sent to the client.
- `$upstream_response_time`, `$upstream_connect_time`, `$upstream_addr` and `$upstream_status` hold one value per upstream connection when several were tried, separated by commas and colons.
- A variable whose value is not found is logged as a hyphen.
- Several `access_log` directives may sit on one level; `access_log off;` cancels all `access_log` directives on the current level.
- `syslog:` as the first parameter sends the log to syslog.
- A log path that contains variables makes nginx open and close the file for each write and disables buffering; `open_log_file_cache max=1000 inactive=20s valid=1m min_uses=2;` caches the descriptors (`inactive` defaults to 10 seconds, `valid` to 60 seconds, `min_uses` to 1).
- Header lines sent to the client are available as `$sent_http_<name>`, for example `$sent_http_content_range`.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_log_module` page (access_log, log_format, open_log_file_cache, variables) and the `ngx_http_upstream_module` page (`$upstream_*` variables and comma-separated multiple values). Removed: advice about secrets in `$request`, the claim that a nested `access_log` replaces the parent's, and the invented Verify step.
Method: documentation only; no commands were run.
