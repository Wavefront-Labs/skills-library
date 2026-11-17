---
id: computing-software.cloud-infrastructure-engineering.kubespray.metallb-bgp-mode-and-calico-advertisement
name: metallb-bgp-mode-and-calico-advertisement
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [metallb, bgp, calico, peers, communities, loadbalancer-ips]
level: advanced
status: docs-checked
description: "Run MetalLB in BGP mode via Kubespray, or disable the speaker and let Calico 3.18+ advertise LoadBalancer IPs."
sources:
  - https://kubespray.io/docs/ingress/metallb.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**BGP mode.** Define upstream peers under `metallb_config.layer3` and link pools to peers. Page structure (values abbreviated):

```yaml
metallb_config:
  layer3:
    defaults:
      peer_port: 179 # The TCP port to talk to. Defaults to 179, you shouldn't need to set this in production.
      hold_time: 120s # Requested BGP hold time, per RFC4271.
    communities:
      vpn-only: "1234:1"
      NO_ADVERTISE: "65535:65282"
    metallb_peers:
      peer1:
        peer_address: 192.0.2.1
        peer_asn: 64512
        my_asn: 4200000000
        communities:
          - vpn-only
        address_pool:
          - pool1
```

Optional per-peer keys: `router_id` (defaults to the node IP; useful when peering with a BGP router on the same machine), `password` for TCPMD5 sessions, and `source_address`, which the page marks as currently not supported.

**Calico instead of the speaker.** With Calico 3.18 or newer, disable the MetalLB speaker and have Calico advertise LoadBalancer IPs, matching your pool ranges:

```yaml
metallb_speaker_enabled: false
metallb_config:
  address_pools:
    primary:
      ip_range:
        - 10.5.0.0/16
      auto_assign: true
  layer2:
    - primary
calico_advertise_service_loadbalancer_ips: "{{ metallb_config.address_pools.primary.ip_range }}"
```

If you have extra pools, list all their ranges in `calico_advertise_service_loadbalancer_ips` (the page shows three CIDRs: 10.5.0.0/16, 10.6.0.0/16, 10.10.0.0/16).

## Checked

2026-11-08. Cited pages re-read in full. BGP structure, optional keys and both Calico variants were confirmed on the MetalLB page; the second peer and example passwords were omitted.

Method: documentation only; no commands were run.
