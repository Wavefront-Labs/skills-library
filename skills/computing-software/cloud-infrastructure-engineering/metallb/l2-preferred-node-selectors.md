---
id: computing-software.cloud-infrastructure-engineering.metallb.l2-preferred-node-selectors
name: l2-preferred-node-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, preferrednodeselectors, weight, l2advertisement, layer2, soft-preference, failover]
level: sme
status: docs-checked
description: "Express a soft node preference for L2 announcements with preferredNodeSelectors weights (1-100), how scores sum across selectors and advertisements, and flapping risks."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_l2_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# L2 preferred node selectors

`nodeSelectors` is a hard filter. `preferredNodeSelectors` is a soft preference: prefer edge nodes, fall back to others. Weights range 1-100.

```yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: prefer-edge
  namespace: metallb-system
spec:
  ipAddressPools:
  - production-pool
  preferredNodeSelectors:
  - weight: 100
    preference:
      matchLabels:
        node-role: edge
```
Nodes matching score 100 and win; others score 0 and serve as failover. Ties are decided by the usual `sha256(node + "#" + ip)` hash, so ordering is deterministic.

Scoring:
- A node matching several selectors sums the weights.
- Several `L2Advertisement` objects for the same pool sum per-ad scores. Example: `tiered-zones` (zone primary 100, secondary 50) plus `zone-boost` (primary 60): a node that is edge and primary scores 160, beating edge-only (100) and primary-only (60).
- Preferences are scoped to the advertisement's own `nodeSelectors`: an ad without `nodeSelectors` scores every node; an ad with them never raises scores of nodes outside its eligible set.

Gotcha: soft preferences make the announcing node track label changes. Flapping labels move services, which is more churn than the pure hash election. Use stable labels (role, zone), not dynamic state.

`kubectl get servicel2statuses -n metallb-system` lists the allocated node per Service.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced L2 configuration" page, "Prefer specific nodes for L2 announcements": weights 1-100, YAML, scoring examples (160, 100, 60), sha256 tie-break, scope rule, label-flap note. ServiceL2Status columns come from the FAQ.
Method: documentation only; no commands were run.
