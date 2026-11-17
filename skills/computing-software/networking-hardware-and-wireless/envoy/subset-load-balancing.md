---
id: computing-software.networking-hardware-and-wireless.envoy.subset-load-balancing
name: subset-load-balancing
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, subset-lb, lb-subset-config, metadata-match, fallback-policy, default-subset, subset-selectors]
level: practitioner
status: docs-checked
description: "Route to host subsets chosen by endpoint metadata using Envoy lb_subset_config, selectors and fallback policies."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/load_balancing/subsets.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# subset load balancing
Subsets divide an upstream cluster's hosts by metadata attached to endpoints; routes then request hosts whose metadata matches, optionally falling back to a defined set. Subsets use the cluster's load balancing policy. The original destination policy cannot be used. Zone aware routing is compatible but can violate its minimum hosts condition.

```yaml
lb_subset_config:
  fallback_policy: DEFAULT_SUBSET
  default_subset: { stage: prod }
  subset_selectors:
  - keys: [version]
  - keys: [stage, version]
```
and on the route:
```yaml
route:
  cluster: backend
  metadata_match:
    filter_metadata:
      envoy.lb: { version: "1.2" }
```
Fallback policies: `NO_FALLBACK` (default; the request fails as if there were no hosts), `ANY_ENDPOINT` (all hosts, ignoring metadata), `DEFAULT_SUBSET` (hosts matching `default_subset`). A selector can override the fallback policy.

Gotchas: subsets must be predefined via selectors; a definition yields subsets only for hosts that carry all of its keys, and one host may appear in several subsets. When the route has no metadata or no subset exists, the fallback policy fires, so the default is a hard failure. The route's metadata match must have a selector with the same keys, or the fallback policy is used.

## Checked
2026-11-03. Confirmed against subsets.rst, including the fallback policies and selector rules. Removed or corrected: the lb_subsets_* stats verify step.
Method: documentation only; no commands were run.
