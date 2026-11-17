---
id: computing-software.cloud-infrastructure-engineering.linkerd.high-availability-mode
name: high-availability-mode
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, ha, high-availability, control-plane]
level: practitioner
status: docs-checked
description: "Enable HA mode with --ha for three control plane replicas, production resources, anti-affinity and a strict proxy injector."
sources:
  - https://linkerd.io/2.19/features/ha/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HA mode runs three replicas of critical control plane components, sets production-ready CPU and memory requests on the control plane and the data plane proxies, sets anti-affinity so critical components land on separate nodes and zones where possible, and requires the proxy injector to be working before pods are scheduled.

Enable it at install time or on an existing control plane:

```bash
linkerd install --ha | kubectl apply -f -
linkerd viz install --ha | kubectl apply -f -
linkerd upgrade --ha | kubectl apply -f -
```

Override parts of it with other flags, such as the number of replicas:

```bash
linkerd install --ha --controller-replicas=2 | kubectl apply -f -
```

The HA proxy injector has a stricter webhook failure policy. If injection fails with an unrecognized error or a timeout during admission, the Kubernetes API server rejects the workload, so no annotated workload can start without its proxy. That makes it essential to keep at least one healthy proxy injector replica.

If you cannot guarantee that, loosen the webhook failure policy to `Ignore` in the Linkerd Helm chart, accepting that workloads may start unmeshed when the injector is down.

Critical components also get pod anti-affinity rules to ensure redundancy.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/features/ha/.

Removed or reworded: Policy recommendation sentence (the policy page, not the HA page, gives it).

Method: documentation only; no commands were run.
