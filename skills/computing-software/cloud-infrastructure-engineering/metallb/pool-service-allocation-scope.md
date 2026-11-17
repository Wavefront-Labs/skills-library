---
id: computing-software.cloud-infrastructure-engineering.metallb.pool-service-allocation-scope
name: pool-service-allocation-scope
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, serviceallocation, pool-priority, namespaceselectors, serviceselectors, multitenant]
level: advanced
status: docs-checked
description: "Pin a MetalLB IPAddressPool to namespaces, namespace labels and service labels with serviceAllocation, and order pools by priority (lowest number wins)."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_ipaddresspool_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pool scope and priority

`serviceAllocation` narrows who can take addresses from a pool; useful in multitenant clusters.

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: ippool-ns-service-alloc-sample
  namespace: metallb-system
spec:
  addresses:
    - 192.168.20.0/24
  avoidBuggyIPs: true
  serviceAllocation:
    priority: 50
    namespaces:
      - namespace-a
      - namespace-b
    namespaceSelectors:
      - matchLabels:
          foo: bar
    serviceSelectors:
      - matchExpressions:
          - {key: app, operator: In, values: [bar]}
```
This pool serves Services labelled `app In [bar]` in `namespace-a`, `namespace-b`, or any namespace labelled `foo: bar`.

Priority when several pools match a Service:
- Pools are sorted by `priority`; the lowest number is chosen first (`priority=1` is the highest priority).
- Unset or `0` means lowest priority: used last.
- Equal priorities: the choice is random.

Gotcha: if a Service explicitly picks a pool (`metallb.io/address-pool`) or an IP (`spec.loadBalancerIP`, `metallb.io/loadBalancerIPs`) that its selectors do not allow, it stays pending.

See `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-ip-assignment` for assignment problems.

## Checked

2026-11-04. Confirmed against the MetalLB "Advanced AddressPool configuration" page (serviceAllocation example, namespaces/namespaceSelectors/serviceSelectors, priority ordering, pending note for explicit requests that do not match). Removed the unsupported debug command line.

Method: documentation only; no commands were run.
