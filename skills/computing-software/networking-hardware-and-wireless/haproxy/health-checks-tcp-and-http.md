---
id: computing-software.networking-hardware-and-wireless.haproxy.health-checks-tcp-and-http
name: health-checks-tcp-and-http
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, health-check, option-httpchk, http-check-send, check-port, tcp-check]
level: practitioner
status: docs-checked
description: "Define layer 4 and layer 7 health checks for HAProxy servers using check, option httpchk, http-check send/expect and tcp-check."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# health checks tcp and http
The server keyword `check` enables health checks. With no other check method configured, a server is considered available when a connection can be established (TCP by default, or SSL/TLS when `ssl` or `check-ssl` is set). Without `check` the server is always considered available.

```
backend be_app
    option httpchk
    http-check connect
    http-check send meth GET uri /healthz ver HTTP/1.1 hdr Host app.example.com
    http-check expect status 200
    server a 10.0.0.11:8080 check inter 2s fall 3 rise 2
    server b 10.0.0.12:8080 check port 9000 addr 10.0.1.12
```
Timing: `inter` is the delay between checks (default 2000 ms; `fastinter` applies while a server is transitioning, `downinter` while fully down), `fall` is the consecutive failures needed to mark a server down (default 3), `rise` the consecutive successes to mark it up (default 2). `inter` also acts as the check timeout when `timeout check` is not set.

`port` and `addr` send checks to another port or address; when used, the server's SSL and proxy-protocol settings are not reused, so set `check-ssl` or `check-send-proxy` explicitly (`check-sni` sets the SNI for TLS checks).

`option httpchk` sends a full HTTP request after the TCP connect; by default `OPTIONS / HTTP/1.0` is used, and 2xx and 3xx responses are healthy while everything else, including no response, is a failure. The shorthand `option httpchk <method> <uri> <version>` is also valid. `http-check send` adds the method, URI, version, headers and body; `http-check expect` replaces the default status rule. HTTP/1.1 requires a Host header, which the docs say to add with `http-check send` (for example `hdr Host www`). `option httpchk` also works in a plain TCP backend, but request formatting and response parsing are strict.

For other protocols there are `option tcp-check` with `tcp-check connect`, `tcp-check send` and `tcp-check expect string +PONG` (a Redis ping), and the built-in `option redis-check`, `option mysql-check`, `option pgsql-check user <username>`, `option ldap-check` and `option smtpchk`.

Gotcha: keep the check URI lightweight (a dedicated health endpoint rather than a full page).

Verify: `haproxy -c -f <config>` accepts the checks; take a backend down and confirm the server is marked DOWN after `fall` failed checks.

## Checked
2026-11-03. Confirmed against configuration.html: server `check`, `port`, `addr`, `inter`/`fastinter`/`downinter`, `fall`, `rise`, `check-ssl`, `check-sni`, `option httpchk`, `http-check connect/send/expect`, `option tcp-check`, `tcp-check`, and the named protocol checks. Removed: the stats-page `L7OK/200` and `L7STS/503` strings, the "Layer7 wrong status" log line, the claim that apps return 400 or redirect without a Host header, the `show servers state` remark, and an unconfirmed `tcp-check connect` pairing in a Redis example.
Method: documentation only; no commands were run.
