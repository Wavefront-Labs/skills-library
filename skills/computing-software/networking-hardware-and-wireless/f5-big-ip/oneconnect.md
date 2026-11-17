---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.oneconnect
name: oneconnect
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, oneconnect, connection-pooling, keep-alive]
level: practitioner
status: draft
description: "Enable OneConnect on BIG-IP to reuse serverside TCP connections, with the source mask and persistence interactions."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OneConnect connection reuse

```
tmsh create ltm profile one-connect oc_app defaults-from oneconnect source-mask 0.0.0.0 max-size 10000 max-age 86400 max-reuse 1000 idle-timeout-override 0
tmsh modify ltm virtual vs_web profiles add { oc_app }
tmsh show ltm profile one-connect oc_app
```
- OneConnect multiplexes client requests over a pool of idle server connections, cutting backend handshake cost. It requires an HTTP profile on the VS.
- `source-mask` decides which client addresses may share a server connection: `0.0.0.0` shares across all clients; `255.255.255.255` pins per client. A broad mask hides different clients' requests in one backend connection, which breaks backends that authenticate the connection (NTLM/Kerberos connection-based auth).
- NTLM: add the `ntlm` profile or `oneconnect-transformations`; or disable OneConnect for the VS.
- Cookie persistence with OneConnect: each request is balanced individually; with `oneconnect-transformations enabled` the HTTP/1.0 to 1.1 header changes (Connection: keep-alive) are applied.
- Without OneConnect, only the first request of a client connection is load-balanced, and later requests go to the same member. Iterating with `HTTP::header` in a rule requires `LB::detach` for per-request switching on keepalive connections.
- Gotcha: `max-reuse` smaller than the number of requests per connection rebuilds connections frequently.

Verify: `tmsh show ltm profile one-connect oc_app` shows `Connections Reused` growing against `New`; a backend log with fewer inbound connections than client requests confirms it.
