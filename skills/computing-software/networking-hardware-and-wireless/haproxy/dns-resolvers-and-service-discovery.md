---
id: computing-software.networking-hardware-and-wireless.haproxy.dns-resolvers-and-service-discovery
name: dns-resolvers-and-service-discovery
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, resolvers-section, server-template, dns-srv, init-addr, service-discovery]
level: practitioner
status: docs-checked
description: "Resolve server names dynamically in HAProxy with a resolvers section, server-template and SRV records, plus resolve-prefer, init-addr and hold timers."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dns resolvers and service discovery
By default HAProxy resolves a server name once, at startup through libc, and caches the result for the process's life. Define a `resolvers` section and attach it per server for run-time resolution:

```
resolvers dns
    nameserver ns1 10.0.0.2:53
    resolve_retries 3
    timeout resolve 1s
    timeout retry 1s
    hold valid 10s
    hold other 30s
    accepted_payload_size 8192
backend be_svc
    balance roundrobin
    default-server check resolvers dns init-addr last,none resolve-prefer ipv4
    server-template web 1-8 _http._tcp.web.service.consul resolvers dns
    server api1 api.internal:8080 check resolvers dns
```
A server name starting with an underscore is treated as an SRV label: the SRV records are fetched, their hostnames used, and servers are added or removed as records change. `server-template <prefix> <num|range> <fqdn>[:<port>] [params]` creates the numbered servers (`web1` to `web8`). All name servers are queried at once and the first valid response is used; an address with a stream prefix such as `tcp@` makes a TCP name server. `parse-resolv-conf` adds the nameservers of resolv.conf.

`init-addr` sets how an FQDN is resolved at startup: `last` (state file), `libc`, `none` (start down with no address) or a literal IP; the first that works is used. The docs advise excluding `libc` when using `resolvers`, because mixing libc and DNS resolution is known to fail on address renewal, hence `last,none` above. `resolve-opts allow-dup-ip` permits several servers to share an IP; `resolve-prefer ipv4|ipv6` picks the address family.

`hold <status> <period>` keeps a server UP for `<period>` after an invalid answer (`nx`, `refused`, `timeout`, `other`; default 30s) if a valid one was seen in that time; `hold valid` (default 10s) applies only to `do-resolve` actions, and `hold obsolete` (default 0s) sets how long before obsolete SRV records are dropped. `accepted_payload_size` is announced to the name servers: unset it announces 512 bytes, 4096 is recommended for UDP, above 8192 is discouraged, and the maximum is 65535. `resolve_retries` defaults to 3; `timeout resolve` and `timeout retry` default to 1s.

Verify: on the runtime socket, `show resolvers dns` shows the section's counters and `show servers state be_svc` lists the servers and their addresses.

## Checked
2026-11-03. Confirmed against configuration.html sections 5.2 (`init-addr`, `resolve-prefer`, `resolve-opts`, `server-template`) and 5.3 (resolvers section keywords, defaults, SRV behaviour) and management.html (`show resolvers`, `show servers state`). Fixed: the example used `init-addr last,libc,none` although the docs say to exclude libc when using resolvers. Removed: "silently truncates big SRV answers", "unused template slots appear DOWN", "DNS changes beyond hold valid won't be seen sooner" (hold valid does not affect server resolution), and the A-record behaviour of templates.
Method: documentation only; no commands were run.
