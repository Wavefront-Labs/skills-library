---
id: computing-software.systems-network-administration.coredns.coredns-autopath
name: coredns-autopath
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, autopath, kubernetes, search-path, ndots]
level: advanced
status: docs-checked
description: "Complete client search paths on the server with autopath, including the @kubernetes search list, metric and known bugs."
sources:
  - https://coredns.io/plugins/autopath/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cut repeated search-path queries from clients.

Syntax: `autopath [ZONE...] RESOLV-CONF`. When a query matches the first element of the search path, autopath follows the chain of search elements and returns the first reply that is not NXDOMAIN. On any failure, the original reply is returned. Because the answer is for a different name, it adds a CNAME from the original name to the answer name.

RESOLV-CONF is a resolv.conf style file needing one line `search domain1 domain2 ...`, or `@kubernetes` to ask the kubernetes plugin for the search list per query. Any plugin implementing the AutoPather interface can be used.

Examples: `autopath my-resolv.conf` reads the search path from that file; `autopath @kubernetes` uses the search path retrieved dynamically from the kubernetes plugin. In Kubernetes, autopath relies on the kubernetes plugin's Pod cache to map the client IP to a Pod and its namespace.

Known bugs:
- If a Pod is deleted and its IP is immediately given to a Pod in another namespace that queries before the watch updates, autopath uses the previous Pod's namespace.
- It is not compatible with Pods on Windows nodes.
- If the server-side search ends negative (NXDOMAIN), the client still searches all paths itself, negating the benefit.

Metric: `coredns_autopath_success_total{server}`.

## Checked

2026-11-08. Checked in full against the autopath plugin README. Removed an unsupported pods verified requirement (not stated on this page) and fixed the description accordingly.

Method: documentation only; no commands were run.
