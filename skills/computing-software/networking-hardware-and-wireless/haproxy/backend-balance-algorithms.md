---
id: computing-software.networking-hardware-and-wireless.haproxy.backend-balance-algorithms
name: backend-balance-algorithms
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, balance, roundrobin, leastconn, balance-source, balance-uri, consistent-hashing]
level: practitioner
status: docs-checked
description: "Choose a HAProxy balance algorithm (roundrobin, leastconn, source, uri, hdr, random) and the hash-type and weight settings that go with it."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# backend balance algorithms
`balance` selects how a backend picks a server. The backend uses `roundrobin` when no other algorithm, mode or option is set, and the algorithm may be set only once per backend.

```
backend be_app
    balance leastconn
    server a 10.0.0.11:8080 check weight 100
    server b 10.0.0.12:8080 check weight 50
```
- `roundrobin`: weighted, dynamic (weights can change on the fly), limited to 4095 active servers per backend.
- `static-rr`: like roundrobin but static: weight changes at runtime have no effect; no server-count limit.
- `leastconn`: lowest number of connections (queued ones counted too); recommended for very long sessions such as LDAP, SQL, TSE and not well suited to short HTTP sessions.
- `first`: first server with a free `maxconn` slot, by server id; pointless without `maxconn`; ignores weight; lets idle servers be powered off.
- `source`: hashes the client IP; best-effort stickiness, mostly used in TCP mode.
- `uri` (optional `len`, `depth`, `whole`, `path-only`), `url_param`, `hdr(<name>)`, `hash <expr>`: hash a request element; static by default; `uri`/`url_param`/`hdr` are for HTTP backends where a missing value falls back to round robin. Do not use URI-based algorithms with NTLM.
- `random` / `random(<draws>)`: random key into consistent hashing; weights and server additions take effect immediately; the default is 2 draws (the "Power of Two Random Choices"), picking the least loaded; good for large farms or servers that come and go.

`hash-type consistent` (instead of `map-based`) makes hash-based algorithms remap only part of the keys when a server changes; with `map-based` the table is a static array of alive servers, so a server change reshuffles clients. `hash-balance-factor <factor>` (needs `hash-type consistent`; default 0 = off; otherwise a percentage above 100, reasonable values 125 to 200) caps a server's load at that percent of the average, and is also used by `balance random`.

Verify: `show stat` on the runtime socket (see runtime-api-stats-socket) has `stot` (cumulative sessions) per server; compare after a load test.

## Checked
2026-11-03. Confirmed against configuration.html: `balance` algorithm list and notes, `hash-balance-factor`, `hash-type` methods. Removed or corrected: "roundrobin default for most HTTP" (default applies when nothing else is set), "leastconn best for databases, websockets" (docs say LDAP, SQL, TSE and not for short HTTP), the description of `random(2)` as hashing request parts, "works well with many load balancers", the `hash-balance-factor` "confirm" marker, and the `show servers state` command with `Stot` (`stot` is a `show stat` column).
Method: documentation only; no commands were run.
