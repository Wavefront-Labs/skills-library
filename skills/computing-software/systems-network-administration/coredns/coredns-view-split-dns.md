---
id: computing-software.systems-network-administration.coredns.coredns-view-split-dns
name: coredns-view-split-dns
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, view, split-dns, expr, server-block]
level: advanced
status: docs-checked
description: "Route queries to a server block by boolean expression for split DNS, and order blocks so a catch-all does not shadow filtered ones."
sources:
  - https://coredns.io/plugins/view/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give different clients different answers for one zone.

Syntax:

```
view NAME {
    expr EXPRESSION
}
```

NAME appears in metrics and as metadata. The block receives a query only when EXPRESSION is true. If several view directives exist, all expressions must be true. Expressions use the expr-lang/expr package, must evaluate to a boolean, and can call functions such as `client_ip()`, `type()`, `name()`, `class()`, `bufsize()`, `do()` and `id()`, plus helpers like `incidr()`.

Example from the docs: `incidr(client_ip(), '127.0.0.0/24')` selects a block with `hosts { 1.1.1.1 test }`, another block selects 192.168.0.0/16, a third an IPv6 range, and a final block without a view answers everyone else with 3.3.3.3.

Ordering: blocks sharing a zone and port are evaluated top to bottom. The first block whose view matches, or that has no view, handles the query. An unfiltered catch-all declared first shadows later view blocks. Declare all view blocks first and the catch-all last.

Gotchas: `client_ip()` returns IPv6 addresses enclosed in brackets (`[::1]`), while `server_ip()` returns them without brackets. In a regex such as `name() matches '^abc\\..*\\.example\\.com\\.$'` the pattern is single-quoted and backslashes are doubled. If the metadata plugin is enabled, `view/name` is published for the request.

Another example: `expr type() in ['A', 'AAAA']` to send address queries to one upstream and everything else to another.

## Checked

2026-11-08. Checked in full against the view plugin README. Accurate; added the IPv6 bracket difference between client_ip() and server_ip(), regex quoting, and the view/name metadata.

Method: documentation only; no commands were run.
