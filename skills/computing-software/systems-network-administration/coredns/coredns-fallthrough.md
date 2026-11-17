---
id: computing-software.systems-network-administration.coredns.coredns-fallthrough
name: coredns-fallthrough
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, fallthrough, nxdomain, plugin-chain, backend]
level: practitioner
status: docs-checked
description: "Use the fallthrough option so a backend plugin passes unanswered names to the next plugin in the chain instead of returning NXDOMAIN."
sources:
  - https://coredns.io/2017/06/08/how-queries-are-processed-in-coredns/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a second plugin answer names the first backend does not have.

Backend plugins (etcd, file, kubernetes) supply zone and record data. A backend is usually the final word for its zone: it returns a result or NXDOMAIN. Some plugins support a `fallthrough` option; when enabled, a missing record is passed down the chain instead of returning NXDOMAIN, so a backend further down can answer.

The chain order is fixed at build time by `plugin.cfg`, not by the order of lines in the Corefile. In the standard release kubernetes comes before file and etcd, so it gets the first chance at a query. Plugins that only change configuration (health, tls, startup, shutdown, root) are not part of the request chain. Plugins like rewrite change the request, pass it on, then restore the original question section on the way back.

Worked example from the docs: add arbitrary records inside the cluster.local zone.

```
.:53 {
    errors
    log
    health
    kubernetes cluster.local 10.0.0.0/24 {
        fallthrough
    }
    file /etc/coredns/cluster.db cluster.local
    forward . /etc/resolv.conf
    cache 30
}
```

Because kubernetes precedes file in plugin.cfg, file handles only the queries kubernetes does not. The zone file (`cluster.db`) must be mounted into the pod through the ConfigMap volume, and CoreDNS told to reload (the post sends SIGUSR1 to PID 1 in each pod). In the post's test, a record in the zone file resolved while a misspelt name still returned NXDOMAIN.

Failure mode: without fallthrough on the earlier backend, the later plugin is never consulted for that zone. The post covers `fallthrough` on the kubernetes plugin; check each plugin's own README for whether it supports the option and for its optional zone arguments.

## Checked

2026-11-08. Read the How Queries Are Processed in CoreDNS post in full. Removed the invented fallthrough ZONES syntax and the plugin support list, neither of which the post gives; rewrote around the post's chain, plugin.cfg ordering and kubernetes plus file example.

Method: documentation only; no commands were run.
