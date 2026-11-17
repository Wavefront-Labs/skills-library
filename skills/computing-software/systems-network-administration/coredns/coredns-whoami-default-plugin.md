---
id: computing-software.systems-network-administration.coredns.coredns-whoami-default-plugin
name: coredns-whoami-default-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, whoami, testing, default, diagnostics]
level: intro
status: docs-checked
description: "Use whoami as a smoke test endpoint that returns the client IP, port and transport, and know it is the default plugin when no Corefile exists."
sources:
  - https://coredns.io/plugins/whoami/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: verify that CoreDNS answers queries.

whoami answers every A or AAAA query regardless of the query name. The answer section is empty. The client's IP address appears in the additional section as an A or AAAA record, and the port and transport (tcp or udp) appear as a SRV record of the form `_<transport>.qname. 0 IN SRV 0 0 <port> .`.

Syntax: `whoami`.

Example:

```
example.org {
    whoami
}
```

A query for `example.org A` returns an additional record such as `example.org. 0 IN A 10.240.0.1` plus `_udp.example.org. 0 IN SRV 0 0 40212`.

Notes:
- If CoreDNS cannot find a Corefile at startup, whoami is the default plugin that gets loaded, so you can still check that the binary responds.
- The docs describe it as of limited use in production; it is a fast endpoint to test clients against.

## Checked

2026-11-08. Checked in full against the whoami plugin README. Accurate; removed an unsupported remark about other plugins' examples.

Method: documentation only; no commands were run.
