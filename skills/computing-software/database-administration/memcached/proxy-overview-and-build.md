---
id: computing-software.database-administration.memcached.proxy-overview-and-build
name: proxy-overview-and-build
category: computing-software
field: database-administration
product: memcached
tags: [proxy, built-in-proxy, enable-proxy, routelib, 1-6-23]
level: practitioner
status: docs-checked
description: "What the built-in proxy (1.6.23+) is, why it needs a source build with --enable-proxy, and the pool, backend, route concepts."
sources:
  - https://docs.memcached.org/features/proxy/
  - https://docs.memcached.org/features/proxy/install/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

From 1.6.23 a memcached binary can act as a frontend proxy to backend memcached servers (plain servers over TCP). Clients speak basic and meta protocols to it. Any binary can be a proxy, a cache, or both.

Concepts: backend (a normal server), pool (named group of backends; a consistent hash of the key picks one), set (group of pools), route (maps context to a handler), route library (Lua file, `routelib`, built in).

Build (not in packages):
```
./configure --enable-proxy
make && make test && sudo make install
memcached --help | grep proxy
```
Output lists `proxy_config` and `proxy_arg`. Optionally download a newer `routelib.lua` from memcached-proxylibs.

Build tools (the page's Debian example): gcc, make and libevent-dev.

Why use it: centralised pool config, thin clients, failover/replication logic. Cost: extra network hops.

## Checked

Confirmed 2026-11-09: proxy from 1.6.23 in front of backends reached over TCP/IP, basic and meta protocols, any binary can be proxy, cache or both, the proxy, backend, pool, set, route and route library definitions, consistent hash picks a backend within a pool, source build required, the `./configure --enable-proxy` build steps, the `memcached --help | grep proxy` check showing `proxy_config` and `proxy_arg`, the optional routelib.lua download from memcached-proxylibs, and the centralisation and extra-hop trade-offs (Built-in proxy, Install and Infrastructure examples pages). Removed the unconditional "needs" wording for build tools.

Method: docs-checked 2026-11-09 against docs.memcached.org Built-in proxy, Install the built-in proxy and Infrastructure examples pages
