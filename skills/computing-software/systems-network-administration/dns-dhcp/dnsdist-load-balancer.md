---
id: computing-software.systems-network-administration.dns-dhcp.dnsdist-load-balancer
name: dnsdist-load-balancer
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns-resolver, dnsdist, dns-load-balancing, rate-limiting, packet-cache, doh, powerdns]
level: practitioner
status: docs-checked
description: "Front resolvers or authoritative servers with dnsdist: backend pools and health checks, load-balancing policies, packet cache, per-client rate limits, and DoT/DoH termination."
sources:
  - https://www.dnsdist.org/guides/serverpools.html
  - https://www.dnsdist.org/reference/config.html
  - https://www.dnsdist.org/guides/console.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnsdist load balancer

dnsdist (PowerDNS) is a DNS-aware proxy: it understands queries, so it can route by name, cache,
rate-limit and terminate encrypted DNS in front of any DNS server.

## Basic config (/etc/dnsdist/dnsdist.conf, Lua)
```lua
setLocal("192.0.2.53:53")
addLocal("[2001:db8::53]:53")
setACL({"10.0.0.0/8", "192.168.0.0/16"})           -- who may query (resolver use)

newServer({address="10.0.1.11", name="res1", checkInterval=1})      -- default pool
newServer({address="10.0.1.12", name="res2", checkInterval=1})
newServer({address="10.0.2.21", pool="ad", name="dc1"})
newServer({address="10.0.2.22", pool="ad", name="dc2"})

setServerPolicy(leastOutstanding)                   -- the default; also firstAvailable, wrandom, chashed
addAction({"corp.example.net.", "_msdcs.corp.example.net."}, PoolAction("ad"))

pc = newPacketCache(100000, {maxTTL=86400, minTTL=0})
getPool(""):setCache(pc)

addAction(MaxQPSIPRule(50, 32, 64), DropAction())   -- >50 qps per IPv4 /32 (v6 /64): drop
addAction(QTypeRule(DNSQType.ANY), TCAction())       -- force a TCP retry for ANY queries
```

## Health and operations
```
dnsdist -c                       # console (with controlSocket configured)
> showServers()                  # state up/down, latency, queries
> topClients(10)
> topQueries(10, 2)              # top names by 2 labels
> getPool(""):getCache():printStats()
> grepq("example.com")           # recent queries matching
```
Health checks send a query every `checkInterval` seconds; the default QNAME is `a.root-servers.net.` and `checkName` changes it, which matters for authoritative backends that do not answer root names. The console needs `controlSocket(...)` in the configuration (then `dnsdist -c`, or `-k`/`-C` for network connections).

## Encrypted DNS
```lua
addTLSLocal("192.0.2.53:853", "/path/to/cert.pem", "/path/to/key.pem")
addDOHLocal("192.0.2.53:443", "/path/to/cert.pem", "/path/to/key.pem", "/dns-query")
```

## Gotchas
- Backends see dnsdist's IP as the client. `useClientSubnet=true` (default false) adds the client address in an EDNS Client Subnet option, and `useProxyProtocol=true` (default off) adds a proxy protocol header, where the backend supports it.
- The packet cache options `maxTTL` (default 86400), `minTTL` (default 0) and `maxNegativeTTL` (default 3600) cap how long answers are cached.
- Run two dnsdist nodes (anycast or VRRP); dnsdist itself is now critical.

## Verify
- [ ] `showServers()` all up; queries succeed with one backend stopped; rate-limit rule increments under a test flood.

## Checked

Date: 2026-10-26. Documentation: PowerDNS dnsdist reference and guide sources in the pdns repository (pdns/dnsdistdist/docs, repository pushed 2026-10-23), read 2026-10-26. Confirmed: setLocal/addLocal/setACL, newServer keys (address, pool, name, checkName, checkInterval, useClientSubnet, useProxyProtocol), default check name, leastOutstanding default and other policies, newPacketCache option defaults, PoolAction, DropAction, TCAction, MaxQPSIPRule and QTypeRule, addAction with domain-name lists, addTLSLocal/addDOHLocal signatures, console functions showServers/topClients/topQueries/grepq, getPool():getCache()/setCache, controlSocket and dnsdist -c. Removed the unconfirmed anycast/VRRP advice wording.

Method: documentation only; no commands were run.
