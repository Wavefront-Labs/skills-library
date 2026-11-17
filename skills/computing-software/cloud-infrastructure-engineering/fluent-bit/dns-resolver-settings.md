---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.dns-resolver-settings
name: dns-resolver-settings
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, dns, net-dns-mode, net-dns-resolver, ipv4, ipv6, async-resolver]
level: advanced
status: docs-checked
description: "Choose DNS transport, resolver implementation and IPv4 or IPv6 preference for Fluent Bit connections."
sources: ["https://docs.fluentbit.io/manual/administration/networking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS settings

**Transport.** Global `dns.mode` issues DNS requests over `TCP` or `UDP`. A plugin that sets `net.dns.mode` overrides the global value. It applies only to the asynchronous resolver.

**Resolver.** `net.dns.resolver` selects the implementation:
- `ASYNC`: the bundled asynchronous resolver, running on the event loop without blocking the worker during a lookup.
- `LEGACY`: the operating system resolver via `getaddrinfo()`, which blocks the worker until the lookup completes. The OS then decides the transport and `net.dns.mode` has no effect.

The global `dns.resolver` sets it for every plugin, and a plugin's own `net.dns.resolver` overrides it. If neither is set, asynchronous plugins use the asynchronous resolver and synchronous plugins use the operating system resolver. Setting `ASYNC` does not make a synchronous plugin asynchronous.

**Address family.** `net.dns.prefer_ipv4` and `net.dns.prefer_ipv6` (both default `false`) prioritise results of that family when connecting.

**Source address.** `net.source_address` binds data traffic to a given local address on multi-interface hosts.

```yaml
pipeline:
  outputs:
    - name: http
      match: '*'
      host: logs.example.com
      port: 443
      net.dns.mode: TCP
      net.dns.resolver: ASYNC
      net.dns.prefer_ipv4: true
      net.source_address: 10.0.0.5
```

Set `LEGACY` when name resolution must follow the behaviour of the host platform, and expect the worker to block for each lookup.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs networking page (raw markdown, read in full).
