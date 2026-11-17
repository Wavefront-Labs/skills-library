---
id: computing-software.networking-hardware-and-wireless.haproxy.termination-state-flags-troubleshooting
name: termination-state-flags-troubleshooting
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, termination-state, haproxy-503, haproxy-504, sc-flags, log-troubleshooting]
level: practitioner
status: docs-checked
description: "Diagnose HAProxy 502, 503, 504 and 400 responses with termination state codes (cD, sH, SC, PR, sQ) and fix the root cause."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# termination state flags troubleshooting
The `termination_state` log field is 2 characters in TCP mode and 4 in HTTP mode: `<event><state><cookie-in><cookie-out>`.

- First character, the first event that ended the stream: `C` client aborted, `S` server aborted or refused, `P` proxy aborted (connection limit, a deny filter, or a security check on the response), `L` handled locally by HAProxy, `R` proxy resource exhausted, `I` internal error, `D` server detected down and configured to kill connections, `U` backup killed because an active server came up, `K` killed by an admin, lowercase `c` client-side timeout, lowercase `s` server-side timeout, `-` normal completion.
- Second character, the stream state when it closed: `R` waiting for a complete request, `Q` queued waiting for a connection slot (needs server `maxconn`), `C` waiting for the server connection, `H` waiting for response headers, `D` data phase, `L` last data to the client, `T` tarpitted, `-` normal.
- Third character: persistence cookie from the client (`N` none, `I` invalid, `D` server down, `V` valid, `E` expired by `maxidle`, `O` too old by `maxlife`, `U` not used, `-` n/a). Fourth: what happened to the server's cookie (`N` none, `I` inserted, `U` updated, `P` passed as is, `R` rewritten, `D` deleted, `-` n/a).

Common pairs from the manual:
- `SC` server or a device in between refused the TCP connection (RST or ICMP, or no route); status likely 502 or 503.
- `sC` `timeout connect` struck before connecting; likely 503 or 504.
- `sH` `timeout server` struck before response headers; the most common anomaly, pointing at slow transactions or saturated servers. Raising `timeout server` is a workaround; the long-term fix is the application.
- `SH` server aborted before sending complete headers, or crashed; inspect the server's logs.
- `sD` server idle past `timeout server` during data, often a short timeout on L4 equipment or an expired keep-alive.
- `cD` client idle past `timeout client` during data; `CD` client aborted during data.
- `sQ` expired in the queue (see `timeout queue`); `CQ` client aborted while queued.
- `PR` proxy blocked the client request: invalid HTTP (400), a deny filter (403), or a request header rewrite failure (500).
- `PH` proxy blocked the server response as invalid, incomplete or dangerous (502).
- `PC` proxy refused to connect because the process socket limit was reached; consider the global `maxconn`.
- `PT` request tarpitted; `CT` client aborted while tarpitted.
- `LR` handled locally (redirect, `return`, or an applet such as stats, cache, Prometheus exporter or a Lua applet).

Gotcha: an HTTP request larger than `tune.bufsize` minus `tune.maxrewrite` is answered with 400 (a response larger than `tune.bufsize` gives 502). The default `tune.bufsize` is 16384, the docs strongly advise against changing it, and HTTP/2 requires 16384 or more. Large cookies or URLs are the usual cause.

Verify: reproduce the failure, read the log line, change one setting and confirm the flags change accordingly.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: the termination state description (all four characters), the table of common combinations (`CD`, `cD`, `CQ`, `sC`, `SC`, `sD`, `SH`, `sH`, `sQ`, `PC`, `PH`, `PR`, `PT`, `CT`, `LR`) and `tune.bufsize`/`tune.maxrewrite` behaviour. Fixed: the fourth character is cookie handling, not redispatch; `PC` is the socket limit, not "no server available"; `tune.bufsize` rule corrected (request limit is bufsize minus maxrewrite). Removed: `option log-health-checks`, `tcpdump` advice, the `NOSRV` claim and the `show errors`/`show sess` debugging line. Read as sections of the configuration manual only.
Method: documentation only; no commands were run.
