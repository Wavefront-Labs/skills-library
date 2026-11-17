---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-cpu-requests-limits
name: proxy-cpu-requests-limits
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, proxy, cpu, resources, helm]
level: advanced
status: docs-checked
description: "Set proxy CPU requests and limits through Helm values or annotations, which also determine how many worker threads the proxy allocates."
sources:
  - https://linkerd.io/2.19/tasks/configuring-proxy-concurrency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each proxy allocates a fixed number of worker threads at startup, and that count caps its CPU use. The default Helm configuration runs one runtime worker (`proxy.runtime.workers.minimum: 1`) with no CPU request or limit.

Set a global default in the control-plane chart. When only a request is given, its value (rounded up to the next whole number) configures the proxy runtime; the same applies to a limit given alone. If both are present, the request goes to the scheduler and the limit configures the runtime:

```yaml
proxy:
  resources:
    cpu:
      request: 100m
      limit: 2000m
```

Override per namespace or workload with annotations on the pod template:

```yaml
annotations:
  config.linkerd.io/proxy-cpu-request: 100m
  config.linkerd.io/proxy-cpu-limit: 2000m
```

Non-integer values are rounded up to the next whole number for the runtime.

How the kubelet enforces limits matters. With the default `none` CPU manager policy, Linux CFS quotas cap CPU time. With the `static` policy, whole cores are pinned through cpusets, which requires the pod to be in the Guaranteed QoS class (every container with matching CPU and memory requests and limits) and the proxy request and limit to be integers of at least 1.

Choosing too many threads can oversubscribe the CPU, so balance the proxy's fixed thread count with the pod's CPU limits and resource quotas.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Linkerd 2.19 Configuring Proxy Concurrency page (default Helm values, request and limit behaviour, annotations, rounding, CPU manager policies and the static policy conditions). The page is labelled as an older version at the time of reading.
