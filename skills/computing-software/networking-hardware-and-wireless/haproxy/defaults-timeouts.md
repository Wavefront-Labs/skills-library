---
id: computing-software.networking-hardware-and-wireless.haproxy.defaults-timeouts
name: defaults-timeouts
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, timeout-client, timeout-server, timeout-connect, timeout-http-request, timeout-tunnel, timeout-queue]
level: practitioner
status: docs-checked
description: "Set the HAProxy timeouts that matter (client, server, connect, http-request, http-keep-alive, queue, tunnel, check) and what each does on expiry."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defaults timeouts
Set `timeout connect`, `timeout client` and `timeout server`. An unspecified timeout is infinite; HAProxy accepts that but reports a warning at startup.

```
defaults
    timeout connect 5s
    timeout client  30s
    timeout server  30s
    timeout http-request 10s
    timeout http-keep-alive 5s
    timeout queue 10s
    timeout tunnel 1h
    timeout check 3s
```
Meaning:
- `connect`: maximum wait for a server connection attempt. If `queue` and `tarpit` are unset they default to this value. Values slightly above multiples of 3 s (4 or 5 s) cover TCP packet loss.
- `client` and `server`: inactivity limits on each side. In TCP mode the docs strongly recommend keeping them equal.
- `http-request`: time to receive the complete request headers (not the body unless `option http-buffer-request`). On expiry HAProxy sends a 408 and the log termination code is `cR`. It is the better Slowloris defence than `client`, which is only an inactivity timeout. Set it in the frontend.
- `http-keep-alive`: how long to wait for a new request on an idle keep-alive connection; if unset, `http-request` applies, and if both are unset `client` applies. Expiry here closes the connection with no error. The docs suggest about 4 seconds as a starting value for HTTP/2, and warn that very small values can truncate HTTP/2 responses.
- `queue`: maximum time in the backend or server queue; on expiry the request is dropped with a 503 (termination flag `sQ`). Default is the `connect` value.
- `tunnel`: replaces `client` and `server` once a connection becomes a tunnel (WebSocket upgrade, CONNECT, or after the first response when no keep-alive or close option is set). Pair it with `timeout client-fin` for half-closed connections.
- `check`: extra read timeout for health checks after the connection is up; without it `inter` bounds the whole check.

Log termination codes: `sH` means `timeout server` struck before the server returned its headers; `cD` means the client sent or acknowledged nothing for `timeout client`. A 504 is returned when the response timeout strikes before the server responds.

Gotcha: some browsers open speculative connections that send nothing; the resulting 408s can be hidden with `option http-ignore-probes` or `errorfile 408 /dev/null`.

Verify: `haproxy -c -f <config>` shows no missing-timeout warnings; with `option httplog`, a request that stalls past `timeout http-request` gets a 408 and logs `cR`.

## Checked
2026-11-03. Confirmed against configuration.html: `timeout connect`, `client`, `client-fin`, `server`, `check`, `http-request`, `http-keep-alive`, `queue`, `tunnel`, `tarpit`, `http-ignore-probes`, the 504 description and termination codes `sH`, `cD`, `cR`, `sQ`. Corrected: `http-keep-alive` falls back to `http-request` then `client`; `queue` and `tarpit` default to `connect`; `tunnel` applies after the first response when no keep-alive or close option is set. Removed: "keep client and server timeouts equal for all modes" (the docs say TCP mode, and to a lesser extent HTTP), and the `curl --limit-rate` verify command.
Method: documentation only; no commands were run.
