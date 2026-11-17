---
id: computing-software.networking-hardware-and-wireless.haproxy.http-connection-reuse-and-keepalive
name: http-connection-reuse-and-keepalive
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, http-reuse, keep-alive, pool-max-conn, http-keep-alive, idle-connections]
level: practitioner
status: docs-checked
description: "Tune HAProxy server connection reuse (http-reuse), keep-alive and idle connections to cut backend connection churn."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http connection reuse and keepalive
HAProxy operates in keep-alive mode by default for HTTP/1.x connections, and `http-reuse` governs how idle server connections are shared between requests.

```
backend be_app
    http-reuse safe
    default-server pool-max-conn 200 pool-purge-delay 5s pool-low-conn 20
    option http-keep-alive
    timeout http-keep-alive 5s
    server a 10.0.0.11:8080 check
```
- Idle connections are kept per server in a pool and grouped by common properties: source and destination addresses, proxy protocol, TOS and mark socket options, and the connection name (the `pool-conn-name` expression, otherwise the `sni` expression).
- `http-reuse never`: idle connections are never shared between sessions (useful to cancel an inherited strategy or to troubleshoot a bogus application).
- `http-reuse safe` is the default and recommended strategy: the first request of a session always uses its own connection, only later requests may use other existing connections, so a browser can silently retry if the server closes a connection while the request is sent.
- `http-reuse aggressive`: first requests may use existing connections that have already been reused at least once; use only when clients can retry a failed request and the benefit outweighs rare connection failures.
- `http-reuse always`: first requests may use any existing connection; only for paths known never to break connections quickly after release (the manual suggests cache farms), and the manual recommends keeping the `http-keep-alive` timeout low in this mode.
- Connections with authentication schemes that rely on the connection, such as NTLM, are marked private and never shared (unless a multiplexing protocol is used with a level above `safe`).
- Server keywords: `pool-max-conn <max>` caps idle connections per server (default -1 unlimited, 0 none); `pool-purge-delay <delay>` closes half the idle connections each interval (default 5s, 0 keeps none); `pool-low-conn <max>` sets a threshold below which a thread does not steal idle connections from another thread (default 0, recommended for normal use).
- `tune.idle-pool.shared { on | off }` shares idle pools between threads (default on); the manual strongly advises against disabling it without a conservative `pool-low-conn`.
- `option http-keep-alive` turns on keep-alive on both sides, giving the lowest client latency and fastest server-side reuse at the cost of idle server connections, and disables any earlier `option httpclose` or `option http-server-close`. `timeout http-keep-alive` is how long to wait for a new request to start after a response; if it expires the connection closes without an error.
- The idle keep-or-close decisions are also governed by `tune.pool-low-fd-ratio` (default 20%) and `tune.pool-high-fd-ratio` (default 25%) of total file descriptors.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual: `http-reuse` levels and text, pool key properties, NTLM handling, `pool-max-conn`, `pool-purge-delay`, `pool-low-conn`, `tune.idle-pool.shared`, `option http-keep-alive`, `timeout http-keep-alive`, the pool fd-ratio defaults. Removed: the claim that reuse is blocked by `option http-server-close`/`httpclose` and by `private` cookie persistence, the `502`/`SH--` retry explanation, the advice to set the server keepalive higher than the pool timers, the `show pools`/`show stat` column numbers and `ss` verify commands, and the example's implication that `reuse` stats columns exist. Read as sections of the manual only.
Method: documentation only; no commands were run.
