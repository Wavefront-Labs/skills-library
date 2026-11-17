---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-discovery-cache-timeouts
name: proxy-discovery-cache-timeouts
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, proxy, discovery, cache, timeouts]
level: advanced
status: docs-checked
description: "Lengthen proxy discovery cache eviction timeouts for slow clients that drop connections when the control plane goes down."
sources:
  - https://linkerd.io/2.19/tasks/configuring-proxy-discovery-cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The proxy caches discovery results, connections and clients, evicting entries that go unused. Two settings control the timeouts:

- `proxy.outboundDiscoveryCacheUnusedTimeout`: eviction timeout for cached service discovery results, connections and clients. Default `5s`.
- `proxy.inboundDiscoveryCacheUnusedTimeout`: eviction timeout for cached policy discovery results. Default `90s`.

Helm:

```bash
helm upgrade linkerd-control-plane \
  --set proxy.outboundDiscoveryCacheUnusedTimeout=60s \
  --set proxy.inboundDiscoveryCacheUnusedTimeout=120s \
  linkerd/linkerd-control-plane
```

CLI, as with any Helm value:

```bash
linkerd upgrade \
  --set proxy.outboundDiscoveryCacheUnusedTimeout=60s \
  --set proxy.inboundDiscoveryCacheUnusedTimeout=120s \
  | kubectl apply -f -
```

For a single namespace or workload, annotate the pod template with `config.linkerd.io/proxy-outbound-discovery-cache-unused-timeout: "60s"` and `config.linkerd.io/proxy-inbound-discovery-cache-unused-timeout: "120s"`.

These values must be present before the workload is injected, so existing workloads need a rollout.

The defaults suit most clusters. Raise them for slow clients, meaning about 5 requests per second or less across two or more replicas, when clients see unexpected connection closures as soon as the control plane is down. A higher cache idle timeout for discovery results can help mitigate these errors.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/tasks/configuring-proxy-discovery-cache/. Both setting names and defaults (5s, 90s), Helm, CLI and annotation forms, the rollout note and the slow-client guidance.

Removed or reworded: The memory-cost remark (not stated on the page).

Method: documentation only; no commands were run.
