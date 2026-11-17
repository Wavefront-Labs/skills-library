---
id: computing-software.systems-network-administration.varnish-cache.vmod-std-functions
name: vmod-std-functions
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vmod-std, std-log, type-conversion, std-healthy]
level: practitioner
status: docs-checked
description: "Use vmod_std: logging and syslog, type conversion, healthy and port, querysort, case and string helpers, file access, cache_req_body, ban, rollback and timed_call."
sources:
  - https://www.varnish.org/docs/reference/vmod_std/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# vmod std functions

`import std;`

- Logging: `std.log(STRING)` writes to the shared memory log with VSL tag `SLT_VCL_Log`; `std.syslog(INT priority, STRING)` sends to syslog (priority is facility ORed with level; `std.syslog(9, ...)` is `LOG_USER | LOG_ALERT`) and, unlike other std functions, has no effect rather than failing VCL on workspace overflow; `std.timestamp(STRING)` adds a labelled timestamp to the log.
- Conversion, all of the form `TYPE type([arguments], [fallback])` with exactly one source argument: `std.duration()`, `std.bytes()`, `std.integer()`, `std.real()`, `std.time()`, `std.ip()`. If conversion fails, `fallback` is returned, or the VCL fails if none was given. `std.strftime(TIME, format)` formats in UTC and returns an empty string on failure.
  - `std.duration("1w", 3600s)`: string needs a unit (`ms`, `s`, `m`, `h`, `d`, `w`, `y`); `real=` and `integer=` arguments are seconds.
  - `std.bytes()`: string multipliers `k`, `m`, `g`, `t`, `p`; `real=` and `integer=` are bytes.
  - `std.ip(s, fallback, resolve=1, p)` uses `getaddrinfo(3)`; the port defaults to 80 (see `std.port()`); `resolve=false` avoids network lookups.
- Strings: `std.tolower()`, `std.toupper()`, `std.strstr(s1, s2)` (case-sensitive; empty string if not found), `std.fnmatch(pattern, subject, pathname=1, noescape=0, period=0)` (shell-style matching; VCL failure if an argument is NULL such as an unset header), `std.querysort(STRING)` sorts a query string for cache normalization, `std.collect(header, sep)` joins repeated headers (collapsing `Set-Cookie` gives unexpected results in browsers; using `obj.http` headers fails VCL).
- Backends: `std.healthy(be)` is true if the backend is healthy; `std.port(ip)` returns the port and always 0 for a Unix domain socket address.
- Files and environment: `std.fileread()` (text) and `std.blobread()` (any file) cache the whole file on first call and never re-read it; `std.file_exists(path)`; `std.getenv(name)` returns the empty string if unset. Newlines in `fileread` output can make invalid headers.
- Requests: `std.cache_req_body(BYTES)` (vcl_recv only) caches the request body if it is smaller than the size and returns true if cached, which makes retrying backend requests with a body possible (POST, PUT); `std.late_100_continue(BOOL)` (vcl_recv only); `std.rollback(HTTP)` restores headers to their original state; `std.set_ip_tos(INT)` sets DSCP/TOS for the whole TCP connection (client context only).
- Invalidation: `std.ban(STRING)` returns true on success; on failure `std.ban_error()` gives the text. Expressions are `<field> <operator> <arg> [&& ...]`; chain with `&&` only, use several bans for OR. Unset headers are not equal to any string. `obj.last_hit` bans depend on the storage engine and `lru_interval`.
- Misc: `std.random(lo, hi)` (not cryptographic), `std.round()` (halfway away from zero), `std.now()` (a new value on every call, unlike the `now` variable), `std.syntax(REAL)` (true if VCL version is at least that), `std.timed_call(SUB)` returns a DURATION.

## Checked
2026-11-08. Read in full: the vmod_std reference page. Confirmed: function list, signatures, defaults, restrictions and the notes above. Removed: the `VCL_Log:tagA` query variant (not on the page) and the claim that cache_req_body stores the body "for hashing" (the page says it enables retrying backend requests with a body).
Method: documentation only; no commands were run.
