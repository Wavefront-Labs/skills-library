---
id: computing-software.networking-hardware-and-wireless.haproxy.stick-tables-concepts
name: stick-tables-concepts
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, stick-table, track-sc, stick-table-types, sc-http-req-rate, table-expire]
level: practitioner
status: docs-checked
description: "Define HAProxy stick tables (type, size, expire, store) and track clients with track-sc to count rates, connections and errors."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# stick tables concepts
A stick table stores entries keyed by a client attribute, each with optional data counters. There is only one stick-table per proxy; to use more, create a dummy backend holding a table and reference it with `table`.

```
backend st_abuse
    stick-table type ip size 1m expire 10m store gpc0,http_req_rate(10s),conn_cur,http_err_rate(1m)
frontend fe_web
    http-request track-sc0 src table st_abuse
    http-request deny deny_status 429 if { sc_http_req_rate(0,st_abuse) gt 100 }
```
Types: `ip` (IPv4 only, about 50 bytes per entry), `ipv6` (about 60 bytes), `integer` (32-bit), `string [len N]` and `binary [len N]` (default 32; longer keys are truncated, shorter binary keys are zero-padded). `size` is the maximum entry count (suffixes k, m, g), about 50 bytes per entry plus string length, and the full set of data types needs 116 bytes per entry. When full, the oldest entries are purged unless `nopurge` is set (then set `expire`).

`store` lists data types; a data type that is not stored makes ACLs on it simply not match. Examples: `conn_cur`, `conn_cnt`, `conn_rate(<period>)`, `sess_rate(<period>)`, `http_req_cnt`, `http_req_rate(<period>)`, `http_err_cnt`, `http_err_rate(<period>)`, `http_fail_rate(<period>)`, `bytes_in_rate(<period>)`, `bytes_out_rate(<period>)`, `gpc0`/`gpc1` (counters), `gpc(<n>)` arrays (up to 100), `gpt0` or `gpt(<n>)` (tags) and `server_id` (enabled automatically when referenced). Rates take a period in milliseconds or with a unit suffix. `http_req_rate` counts every started request, valid or not; `http_err_cnt` counts invalid, truncated, denied and tarpitted requests, failed authentications and server 4xx responses.

`track-sc0|1|2 <key> [table <table>]` starts tracking; it does not stop rule evaluation. The first `track-sc0` executed selects the first counter set, and so on. By default three counter sets exist (`tune.stick-counters`; raising it costs 16 bytes per connection and per request each). Convention: sc0 in `tcp-request connection`, sc1 for frontend `tcp-request content`, sc2 for backend content rules. `sc_http_req_rate(<ctr>[,<table>])` and `sc_conn_cur(<ctr>[,<table>])` read the tracked counters.

`expire` is the maximum age since the entry was created, refreshed by `track-sc`, or matched by `stick match`/`stick on`. Unset means entries never expire but old ones are removed when the table is full; the maximum is a little over 24 days. Learned associations are lost on restart unless `peers` replicate the table.

Verify: the runtime API `show table <name>` lists entries (optionally filtered by `key` or `data.<type> <operator> <value>`), and `clear table <name> key <key>` removes one.

## Checked
2026-11-03. Confirmed against configuration.html (`stick-table` arguments and data types, `track-sc*`, `tune.stick-counters`, `sc_http_req_rate`, `sc_conn_cur`, `deny`) and management.html (`show table`, `clear table`). Fixed: `expire` is not "reset on every access" but is refreshed only by track-sc and stick match/on; `gpc0` is a legacy counter beside `gpc(<n>)`; the counter-set number is bounded by `tune.stick-counters` (default 3). Removed: "50-100 bytes per entry" (replaced with documented figures), "2.7+" version claim and the `socat` command in the verify line.
Method: documentation only; no commands were run.
