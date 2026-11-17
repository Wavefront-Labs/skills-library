---
id: computing-software.cloud-infrastructure-engineering.cilium.endpoint-lifecycle-and-init-identity
name: endpoint-lifecycle-and-init-identity
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, endpoint, lifecycle, reserved-init, lockdown, policy-map]
level: advanced
status: docs-checked
description: "Cilium endpoint states, the reserved:init identity and policy rules for initializing endpoints, and lockdown on policy map overflow."
sources:
  - https://docs.cilium.io/en/stable/security/policy/lifecycle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Endpoint lifecycle, init identity and lockdown

## States
`restoring`, `waiting-for-identity`, `waiting-to-regenerate`, `regenerating` (eBPF being programmed), `ready`, `disconnecting`, `disconnected`. Query with `cilium-dbg endpoint list` and `cilium-dbg endpoint get`. A running endpoint cycles through waiting-for-identity, waiting-to-regenerate, regenerating and ready when identity, policy or configuration changes.

## Init identity
When labels are not yet known (Docker via libnetwork, Kubernetes API server unavailable, etcd mode with kvstore unavailable), the endpoint temporarily gets label `reserved:init`. Allow its traffic with rules selecting `reserved:init` or the special `init` entity (docs examples: allow initializing endpoints to receive from the host and do DNS queries).

If any ingress (egress) rule selects `reserved:init`, other ingress (egress) traffic to or from initializing endpoints not explicitly allowed is dropped. Otherwise, with policy enforcement mode `never` or `default` all traffic is allowed; in other modes all is dropped.

## Lockdown
Agent option `enable-lockdown-endpoint-on-policy-overflow: "true"` puts an endpoint into lockdown when its policy map overflows: all ingress and egress traffic is dropped, with a warning logged, until it no longer overflows. Monitor the `cilium_policy_*` map `bpf_map_pressure` metric (above 1.0 means pressure at the limit) for alerts.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/lifecycle/. 

Method: documentation only; no commands were run.
