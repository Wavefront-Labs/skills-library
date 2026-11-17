---
id: computing-software.cloud-infrastructure-engineering.nginx.conditional-logging-buffering
name: conditional-logging-buffering
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, access-log-buffer, access-log, buffer, flush, conditional-logging]
level: practitioner
status: docs-checked
description: "Reducing log I/O and noise in nginx with the access_log buffer, gzip and flush parameters and if= conditions."
sources: ["https://nginx.org/en/docs/http/ngx_http_log_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`access_log path [format [buffer=size] [gzip[=level]] [flush=time] [if=condition]];`

```nginx
map $status $loggable {
    ~^[23]  0;
    default 1;
}

access_log /var/log/nginx/access.log main buffer=64k flush=5s;
access_log /var/log/nginx/errors.log main if=$loggable;

location = /healthz { access_log off; return 200; }
```

- Using `buffer` or `gzip` buffers log writes. The buffer must not exceed the size of an atomic write to a disk file.
- Buffered data is written when the next line does not fit, when it is older than `flush`, and when a worker re-opens log files or shuts down.
- `gzip[=level]` compresses the buffered data in atomic blocks (level 1 to 9, default 1; buffer size defaults to 64K), so the file can be read with `zcat` at any time. nginx must be built with zlib.
- `if=condition` skips the line when the condition evaluates to `0` or an empty string. The documented example logs only responses that are not 2xx or 3xx, using a `map` on `$status`.
- Buffered writes do not work when the log path contains variables.
- `access_log off;` cancels all `access_log` directives on the current level.

## Checked

2026-11-03. Confirmed against the nginx `ngx_http_log_module` page (access_log parameters, buffering rules, gzip, `if=` and its map example). Removed: `split_clients` sampling, claims about crash loss and partial gzip blocks, the unused `$not_health` map, and the curl Verify step.
Method: documentation only; no commands were run.
