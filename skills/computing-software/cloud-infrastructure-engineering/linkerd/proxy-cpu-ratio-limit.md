---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-cpu-ratio-limit
name: proxy-cpu-ratio-limit
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, proxy, cpu, workers, helm]
level: advanced
status: docs-checked
description: "Size proxy worker threads as a ratio of node CPUs using maximumCPURatio when fixed CPU limits are impractical."
sources:
  - https://linkerd.io/2.19/tasks/configuring-proxy-concurrency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When workloads run on nodes of different sizes or declare no CPU limits, a fixed limit is hard to choose. Linkerd can instead size the proxy runtime as a ratio of the host's CPUs.

In the control-plane Helm values:

```yaml
proxy:
  runtime:
    workers:
      maximumCPURatio: 0.2
      minimum: 1
```

A `maximumCPURatio` of `1.0` allocates one worker per CPU. A value of `0.2` allocates one worker for every five available cores, rounded up or down as appropriate. `runtime.workers.minimum` sets the lower bound on workers per proxy.

Override the default for a namespace or workload with an annotation on the pod template:

```yaml
annotations:
  config.linkerd.io/proxy-cpu-ratio-limit: "0.2"
```

A CPU limit takes precedence over the ratio, so it is suitable to set a global default `maximumCPURatio` and set explicit limits on specific workloads.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Linkerd 2.19 Configuring Proxy Concurrency page (Rational Proxy CPU Limits sections: ratio meaning, Helm values, annotation, limit precedence). Removed two advisory paragraphs (scheduler request advice and re-injection timing) that the page does not state. The page is labelled as an older version at the time of reading.
