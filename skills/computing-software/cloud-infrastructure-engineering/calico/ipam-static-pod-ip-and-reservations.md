---
id: computing-software.cloud-infrastructure-engineering.calico.ipam-static-pod-ip-and-reservations
name: ipam-static-pod-ip-and-reservations
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ipam, static-ip, annotation, ipreservation, ippool, allowed-uses, nodeselector, reserve]
level: practitioner
status: docs-checked
description: "Give a pod a fixed address with the ipAddrs annotation and keep Calico from reusing it: !all() pool, IPReservation or allowedUses."
sources:
  - https://docs.tigera.io/calico/latest/networking/ipam/use-specific-ip
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Needs Calico IPAM. The static address must lie inside a configured Calico IP pool and not be in use.

Annotate the pod with a bracketed list; note the escaped inner quotes:

```
  "cni.projectcalico.org/ipAddrs": "[\"192.168.0.1\", \"2001:db8::1\"]"
```

Rules from the page:

- The annotation must be present **at pod creation**; adding it later has no effect.
- Only one address per IP family per pod is supported.

**Stopping automatic reuse.** Because the address must be inside a pool, Calico may hand it to another workload or use it for an internal tunnel address. Options:

| Goal | Approach |
|---|---|
| Reserve a whole pool for manual use | Set the IPPool `nodeSelector` to `"!all()"`, which matches no nodes, so it is never used automatically |
| Reserve part of a pool | Create an `IPReservation` resource; Calico IPAM then avoids those IPs, but annotation-based manual assignment can still use them |
| Keep tunnel addresses out of a pool | Set the IPPool `allowedUses` to `["Workload"]` |

Static addresses suit applications needing stable IPs, or external DNS entries pointing directly at pods.

The Kubernetes pod CIDR (the range Kubernetes components use to decide whether an IP belongs to a pod) is separate from Calico pools; keep static addresses inside both.

## Checked

Read in full on 2026-11-08: the Use a specific IP address with a pod page. The annotation syntax, the creation-time and single-address rules and the three reservation options match it.

Method: documentation only; no commands were run.
