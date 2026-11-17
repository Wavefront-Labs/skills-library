---
id: computing-software.cloud-infrastructure-engineering.gateway-api.listener-distinctiveness-and-conflicts
name: listener-distinctiveness-and-conflicts
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [listener, distinctiveness, conflicted, port, protocol, hostname]
level: advanced
status: docs-checked
description: "Listener distinctiveness rules per protocol (TCP, UDP, TLS, HTTP, HTTPS) and why conflicted listeners stop a Gateway reaching Accepted."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Traffic through a Gateway must match only one Listener, so Listeners must be **distinct**. Listeners that are not distinct are **Conflicted** and may not coexist on the same Gateway; if they do, the entire Gateway is invalid and will not reach `Accepted`.

Distinctiveness by protocol:

- `TCP` and `UDP`: distinct only on `protocol` + `port`. TCP/53 and UDP/53 are distinct; two TCP listeners on port 22 are Conflicted.
- `TLS`: `protocol` + `port` + `hostname`. The hostname is the SNI; the `tls` block (terminate or not) is irrelevant to distinctiveness.
- `HTTP`: `protocol` + `port` + `hostname`. Two HTTP/80 listeners with different hostnames are distinct.
- `HTTPS`: same triple, plus a Secret reference of type `kubernetes.io/tls`. Different hostnames may use different Secrets but need not.

```yaml
listeners:
- name: specific
  hostname: specific.example.com
  protocol: HTTP
  port: 80
- name: wildcard
  hostname: "*.example.com"
  protocol: HTTP
  port: 80
```

The pair above is distinct. A Gateway holds at most 64 listeners (ListenerSet lifts this); across a Gateway and its ListenerSets the same distinctness rule applies and the Gateway's own listeners win conflicts.

Once a Listener is chosen, traffic must be routable via an attached Route or it is dropped; it cannot fall back to another Listener.

## Checked

2026-11-04. Confirmed on the Gateway API API overview (api-overview.md): single-listener requirement, per-protocol distinctiveness rules, Conflicted and Accepted behaviour, no fallback to another listener. The 64-listener limit and the parent-Gateway-wins rule are from the ListenerSet reference (listenerset.md). Nothing removed.

Method: documentation only; no commands were run.
