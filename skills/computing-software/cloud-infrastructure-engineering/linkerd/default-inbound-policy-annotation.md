---
id: computing-software.cloud-infrastructure-engineering.linkerd.default-inbound-policy-annotation
name: default-inbound-policy-annotation
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, authorization-policy, default-policy, annotations]
level: practitioner
status: docs-checked
description: "Choose a default inbound policy for the cluster, namespaces and workloads with proxy.defaultInboundPolicy and config.linkerd.io/default-inbound-policy."
sources:
  - https://linkerd.io/2.19/features/server-policy/
  - https://linkerd.io/2.19/reference/authorization-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Linkerd allows all traffic. Default policies set the baseline before fine-grained CRDs refine it.

The cluster-wide default is the install value `proxy.defaultInboundPolicy`. Override it on a namespace, workload or pod with the annotation `config.linkerd.io/default-inbound-policy`. Valid values:

- `all-unauthenticated`: allow all traffic (the default)
- `all-authenticated`: allow meshed clients from the same or another cluster
- `cluster-authenticated`: allow meshed clients in the same cluster
- `cluster-unauthenticated`: allow meshed and unmeshed clients in the same cluster
- `deny`: deny everything
- `audit`: like `all-unauthenticated`, but requests are flagged in logs and metrics

```yaml
metadata:
  annotations:
    config.linkerd.io/default-inbound-policy: cluster-authenticated
```

The default is fixed when the proxy initializes. Changing the annotation on a running pod has no effect; the pod must be recreated.

Policy is enforced only on meshed pods. If policy is a strict requirement, combine it with HA mode, which requires that the proxy be present when pods start.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/features/server-policy/, https://linkerd.io/2.19/reference/authorization-policy/.

Removed or reworded: Rollout recommendation not on the pages.

Method: documentation only; no commands were run.
