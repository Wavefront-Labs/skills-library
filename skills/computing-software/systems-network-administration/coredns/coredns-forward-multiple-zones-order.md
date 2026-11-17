---
id: computing-software.systems-network-administration.coredns.coredns-forward-multiple-zones-order
name: coredns-forward-multiple-zones-order
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, forward, ordering, subdomains, except]
level: practitioner
status: docs-checked
description: "Order several forward lines in one server block so subdomain zones come before parent zones, and exclude names with except."
sources:
  - https://coredns.io/plugins/forward/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: route different domains to different upstreams in one block.

When a server block has several forward plugins, CoreDNS evaluates them in the order listed. Subdomains must therefore come before parent domains, or subdomain queries are sent to the parent's upstream.

```
. {
    cache
    forward lab.example.local 10.20.0.1
    forward example.local 10.0.0.1
    forward . /path/to/resolv.conf
}
```

This is almost equivalent to three server blocks, except that three blocks define three separate plugin chains and therefore three cache instances.

Exclusion: `except IGNORED_NAMES...` is a space-separated list of domains not to forward. Requests matching none of the names are passed through.

```
. {
    forward . 10.0.0.10:1234 {
        except example.org
    }
}
```

Other options:
- `force_tcp`: use TCP even if the request arrived over UDP.
- `prefer_udp`: try UDP first even for TCP requests, retrying over TCP if the response is truncated. If both are set, force_tcp wins.
- `source_address IP`: source address for all outgoing queries and health checks. Responses may fail if upstreams are on other networks without correct return routing.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/forward/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
