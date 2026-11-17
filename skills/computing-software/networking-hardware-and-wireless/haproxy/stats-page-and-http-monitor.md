---
id: computing-software.networking-hardware-and-wireless.haproxy.stats-page-and-http-monitor
name: stats-page-and-http-monitor
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, stats-page, stats-uri, stats-auth, monitor-uri, stats-admin]
level: practitioner
status: docs-checked
description: "Publish the HAProxy statistics page with stats uri, auth, scope, refresh and admin, and a lightweight monitor-uri for upstream health checks."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# stats page and http monitor
A dedicated frontend or listen section (do not mix it with public ports) serves the dashboard:

```
frontend fe_stats
    bind 127.0.0.1:8404
    mode http
    stats enable
    stats uri /stats?
    stats refresh 10s
    stats show-legends
    stats show-node
    stats hide-version
    stats auth admin:ChangeMe!       # cleartext password, see below
    acl LOCALHOST src 127.0.0.1
    stats admin if LOCALHOST
    monitor-uri /haproxy_ping
    http-request use-service prometheus-exporter if { path /metrics }
```
- `stats enable` turns the page on with build-time defaults (URI `/haproxy?stats`, realm "HAProxy Statistics", no authentication, no scope restriction). The manual recommends setting the other `stats` options explicitly instead of relying on defaults.
- `stats uri <prefix>` is intercepted on relayed traffic, so make sure it never appears in the application. Including a question mark helps stop intermediate proxies caching the report and ensures no valid URI starts with the same words. Using `/` in a `listen` section of its own dedicates an address or port to statistics.
- `stats auth <user>:<passwd>` uses HTTP Basic authentication with cleartext passwords in the configuration; the password also travels in cleartext, so keep the page off public interfaces or protect the transport. It may be repeated for more users; failed attempts get a 401 so the browser prompts.
- `stats admin { if | unless } <cond>` allows enabling and disabling servers from the page (read-only by default). The manual warns that admin POST requests are prone to CSRF, only partly mitigated by an Origin/Referer check, so avoid exposing it on a public interface and restrict access; the POST is limited to the buffer size minus reserved space, so change few servers at a time.
- `stats scope { <name> | . }` restricts which listen, frontend or backend sections appear (and can be changed in admin mode); `.` means the current section. Names are compared as plain strings and never checked for existence.
- `stats refresh <delay>` suggests a browser refresh delay (seconds by default) and adds a "refresh/stop refresh" link. `stats hide-version` removes the HAProxy version from the report. `stats show-legends` adds cap, mode, SNMP id, IP and cookie information; `stats show-node [<name>]` reports a host name (the global node name if none is given).
- `monitor-uri <uri>` intercepts that exact URI in an HTTP-mode frontend and answers `HTTP/1.0 200 OK` (or 503 when a `monitor fail` condition is met) without forwarding or logging it. Method, version and headers are ignored; it is processed right after parsing, before `http-request` rules, with only `tcp-request` rules applied earlier. Only one URI is used (the last statement wins). `monitor fail { if | unless } <cond>` makes it return 503, typically with an ACL on `nbsrv(<backend>)`; it works only in HTTP mode.

Verify: request the stats URI from the allowed address and the monitor URI from a probe; the monitor URI returns 200, and 503 when its `monitor fail` condition holds.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `stats enable` defaults, `stats uri`, `stats auth`, `stats admin` (including the CSRF and buffer-size notes), `stats scope`, `stats refresh`, `stats hide-version`, `stats show-legends`, `stats show-node` (listed), `monitor-uri`, `monitor fail` and the `http-request use-service prometheus-exporter` example. Removed: `/stats;csv` and `;norefresh` (not in this manual), the claim about multiple `nbproc`-style workers having separate counters, and the `curl ... | head` verify command. Changed the stats URI to include a question mark per the manual's advice. Read as sections of the manual only.
Method: documentation only; no commands were run.
