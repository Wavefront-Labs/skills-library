---
id: computing-software.cloud-infrastructure-engineering.calico.bgpconfiguration-resource-fields-and-overrides
name: bgpconfiguration-resource-fields-and-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [bgp, bgpconfiguration, communities, prefixadvertisements, listenport, bindmode, meshpassword, node-override]
level: advanced
status: docs-checked
description: "Reference for the BGPConfiguration resource: default versus node.<name> scope, global-only fields, communities, prefixAdvertisements, listenPort, bindMode and mesh password."
sources:
  - https://docs.tigera.io/calico/latest/reference/resources/bgpconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `default` BGPConfiguration holds cluster-wide BGP settings; a resource named `node.<nodename>` overrides for one node, and **only `prefixAdvertisements`, `listenPort` and `logSeverityScreen` can be overridden that way**.

```yaml
apiVersion: projectcalico.org/v3
kind: BGPConfiguration
metadata:
  name: default
spec:
  logSeverityScreen: Info
  nodeToNodeMeshEnabled: true
  nodeMeshMaxRestartTime: 120s
  asNumber: 63400
  serviceClusterIPs:
    - cidr: 10.96.0.0/12
  serviceExternalIPs:
    - cidr: 104.244.42.129/32
    - cidr: 172.217.3.0/24
  listenPort: 178
  bindMode: NodeIP
  communities:
    - name: bgp-large-community
      value: 63400:300:100
  prefixAdvertisements:
    - cidr: 172.218.4.0/26
      communities:
        - bgp-large-community
        - 63400:120
```

Global-only on `default`: `nodeToNodeMeshEnabled`, `asNumber` (per-node AS is set on the Node resource `bgp` field), `serviceClusterIPs`, `serviceExternalIPs`, `serviceLoadBalancerIPs`. Service IPs are advertised only if they fall within the listed CIDR blocks.

Other fields: `bindMode` is `None` (listen on all addresses) or `NodeIP` (only the node's canonical IP); `communities` define named standard (`aa:nn`) or large values, and are not advertised until referenced by `prefixAdvertisements`, which can use a community name or a literal value; `nodeMeshPassword` secures all mesh peerings; `nodeMeshMaxRestartTime` sets the graceful restart time; `ignoredInterfaces` excludes interfaces when reading device routes; `programClusterRoutes` selects which pools BIRD programs cluster routes for (`Disabled`, `EnabledNoEncapOnly`, `EnabledIPIPOnly`, and more).

## Checked

2026-11-04. The sample YAML, name semantics, override limits and field descriptions were confirmed on the BGP configuration resource page.

Method: documentation only; no commands were run.
