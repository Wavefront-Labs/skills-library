---
id: computing-software.cloud-infrastructure-engineering.calico.bgp-filters-import-export-rules
name: bgp-filters-import-export-rules
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [bgp, bgpfilter, import, export, route-filtering, bgppeer, matchoperator, cidr]
level: advanced
status: docs-checked
description: "Write a BGPFilter with ordered importV4, exportV4, importV6 and exportV6 rules, understand first-match and default Accept, and attach it to a BGPPeer by name in filters."
sources:
  - https://docs.tigera.io/calico/latest/networking/configuring/bgp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
BGP filters control which routes are imported from and exported to a peer. Rules in `importV4`, `exportV4`, `importV6` and `exportV6` are evaluated in order and the **first matching rule's `action` applies**. If nothing matches, the default is `Accept`. A filter has no effect until its `name` is listed in the `filters` field of a BGPPeer; filters are applied in the order listed there.

Rule fields seen in the page's examples: `action` (`Accept` or `Reject`), `matchOperator` (`In`, `NotIn`, `Equal`) with `cidr`, and the selectors `source: RemotePeers` and `interface: '*.calico'`.

```yaml
apiVersion: projectcalico.org/v3
kind: BGPFilter
metadata:
  name: my-filter
spec:
  exportV4:
    - action: Accept
      matchOperator: In
      cidr: 77.0.0.0/16
    - action: Reject
      source: RemotePeers
    - action: Reject
      interface: '*.calico'
  importV4:
    - action: Reject
      matchOperator: NotIn
      cidr: 44.0.0.0/16
  exportV6:
    - action: Reject
      source: RemotePeers
    - action: Reject
      interface: '*.calico'
  importV6:
    - action: Accept
      matchOperator: Equal
      cidr: 5000::0/64
    - action: Reject
```

Reading the example: export routes in 77.0.0.0/16, never re-export routes learned from remote peers or from the `*.calico` interfaces; reject imports outside 44.0.0.0/16; for IPv6 accept only 5000::0/64 and reject everything else.

The page also attaches two filters to one BGPPeer with `filters: [first-bgp-filter, second-bgp-filter]` (the peer there uses `peerSelector: has(filter-bgp)`); BGPFilters are applied in the order listed on the peer.

## Checked

2026-11-04. Rule semantics, default action, ordering note and the example filter were confirmed on the Configure BGP peering page.

Method: documentation only; no commands were run.
