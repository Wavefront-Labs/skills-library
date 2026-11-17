---
id: computing-software.systems-network-administration.coredns.coredns-plugin-chain-order
name: coredns-plugin-chain-order
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, plugin-chain, plugin-cfg, ordering, internals]
level: advanced
status: docs-checked
description: "Learn that plugin execution order comes from plugin.cfg at build time, not from Corefile line order, and what that means for rewrites and fallthrough."
sources:
  - https://coredns.io/2017/06/08/how-queries-are-processed-in-coredns/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict which plugin sees a query first.

CoreDNS chains plugins, but the chain order is dictated at build time by the plugin.cfg file, not by the order of lines in a server block. That is why `cache` can be written at the end of a block and still not be the last plugin in the chain.

Plugins fall into groups:
- Config-only plugins that modify the server or server block and never handle requests, so they are not in the chain. The docs name health, tls, startup, shutdown and root.
- Request manipulators that act and then pass the query on. rewrite changes the question, passes it on, and on return puts the original question back while keeping the response.
- Backends that are sources of zone data: etcd, file, kubernetes.

Consequences:
- A backend is normally the final word for its zone: it returns a result or NXDOMAIN.
- With `fallthrough`, a backend passes a missing record to the next plugin instead. Because kubernetes comes before file and etcd in the standard release, kubernetes gets the first chance, and file only sees what falls through.
- Changing the order means rebuilding CoreDNS with an edited plugin.cfg.

## Checked

2026-11-08. Read the cited blog post in full; all claims match it.

Method: documentation only; no commands were run.
