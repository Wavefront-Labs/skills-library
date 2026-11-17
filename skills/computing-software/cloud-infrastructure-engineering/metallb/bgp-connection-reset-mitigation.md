---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-connection-reset-mitigation
name: bgp-connection-reset-mitigation
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, bgp, resilient-ecmp, connection-reset, stateless-hashing, node-failure, ingress]
level: advanced
status: docs-checked
description: "Why a node change resets most active connections to a MetalLB BGP service and the documented mitigations, from resilient ECMP to ingress controllers and client retries."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/bgp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP connection resets and mitigations

Cause: routers load balance statelessly by hashing packet fields into the array of backends. These hashes are usually not stable, so when the backend set changes (for example a node's BGP session drops), most existing connections are rehashed to a backend that knows nothing about them. Users see "Connection reset by peer".

Impact: a one-time break whenever the IP-to-node mapping changes; no ongoing loss or blackholing.

Mitigations the docs list:
- Use a stable ECMP hash on the router ("resilient ECMP" or "resilient LAG"), which hugely reduces affected connections.
- Pin service deployments to specific nodes to shrink the set of nodes you must be careful with.
- Schedule changes during traffic troughs.
- Split a logical service into two Services with different IPs and migrate users by DNS before disrupting the drained one.
- Add transparent client retry logic (works well for mobile apps and single-page web apps).
- Put services behind an ingress controller that uses MetalLB; only changes to the ingress deployment itself (for example scaling NGINX pods) are risky.
- Accept occasional resets for low-availability internal services.

## Checked
2026-11-04. Confirmed against the MetalLB "MetalLB in BGP mode" page, Limitations section: cause, one-time impact and all seven mitigations. Removed an added pre-drain check line.
Method: documentation only; no commands were run.
