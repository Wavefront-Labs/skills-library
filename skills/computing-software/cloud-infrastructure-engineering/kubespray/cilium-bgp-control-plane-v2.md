---
id: computing-software.cloud-infrastructure-engineering.kubespray.cilium-bgp-control-plane-v2
name: cilium-bgp-control-plane-v2
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [cilium, bgp, bgpv2, peering, advertisements, cluster-config]
level: sme
status: docs-checked
description: "Enable the Cilium BGP Control Plane in Kubespray and drive the bgpv2 resources from inventory variables; avoid legacy peering policies."
sources:
  - https://kubespray.io/docs/CNI/cilium.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable the control plane with `cilium_enable_bgp_control_plane: true`.

For Cilium v1.16 and later the new bgpv2 API is managed by custom resources, each fed by one inventory variable:

- `cilium_bgp_cluster_configs`: BGP instances with `localASN`, `peers` (name, `peerASN`, `peerAddress`, `peerConfigRef`) and a `nodeSelector`.
- `cilium_bgp_peer_configs`: peer settings such as `gracefulRestart`, and `families` (afi `ipv4`/`ipv6`, safi `unicast`) with `advertisements` selected by `matchLabels`.
- `cilium_bgp_advertisements`: labelled advertisements, either `PodCIDR` (with BGP communities) or `Service` (addresses `ClusterIP`, `ExternalIP`, `LoadBalancerIP`).
- `cilium_bgp_node_config_overrides`: per-node overrides such as `routerID`, `localPort` and per-peer `localAddress`.

Excerpt from the page's cluster config:

```yml
cilium_bgp_cluster_configs:
  - name: "cilium-bgp"
    spec:
      bgpInstances:
      - name: "instance-64512"
        localASN: 64512
        peers:
        - name: "peer-64512-tor1"
          peerASN: 64512
          peerAddress: '10.47.1.1'
          peerConfigRef:
            name: "cilium-peer"
```

The peer config named `cilium-peer` and the advertisement label `advertise: bgp` must match across the variables.

**Legacy.** `cilium_bgp_peering_policies` uses the deprecated `CiliumBGPPeeringPolicy` (`cilium.io/v2alpha1`) CRD, which warns in Cilium logs from v1.16. Migrate to the four variables above.

## Checked

2026-11-08. Cited pages re-read in full. Variables, YAML excerpt and the deprecation warning were confirmed on the BGP Control Plane sections of the Cilium page. The name and label matching is visible in the page example.

Method: documentation only; no commands were run.
