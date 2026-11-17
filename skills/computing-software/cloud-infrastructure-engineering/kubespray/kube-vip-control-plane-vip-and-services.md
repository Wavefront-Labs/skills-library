---
id: computing-software.cloud-infrastructure-engineering.kubespray.kube-vip-control-plane-vip-and-services
name: kube-vip-control-plane-vip-and-services
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [kube-vip, vip, ha, arp, bgp, leader-election, loadbalancer]
level: advanced
status: docs-checked
description: "Enable kube-vip in Kubespray for a control plane VIP and LoadBalancer services in ARP or BGP mode, with leader election and metrics."
sources:
  - https://kubespray.io/docs/ingress/kube-vip.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
kube-vip gives clusters a virtual IP and load balancer for the control plane and for Services of type LoadBalancer. If `kube_proxy_mode` is `ipvs` and kube-vip ARP is on, set `kube_proxy_strict_arp: true`.

```yaml
kube_vip_enabled: true
# HA for control-plane, requires a VIP
kube_vip_controlplane_enabled: true
kube_vip_address: 10.42.42.42
kube_apiserver_endpoint: "https://{{ kube_vip_address }}:6443"
kube_apiserver_cluster_internal_endpoint: "https://{{ kube_vip_address }}:6443"
# kube_vip_interface: ens160

# LoadBalancer for services
kube_vip_services_enabled: false
# kube_vip_services_interface: ens320
```

Using it as a services load balancer needs extra manual steps (the kube-vip cloud provider).

Mode switches:
- Local traffic policy: `kube_vip_enableServicesElection: true`.
- ARP: `kube_vip_arp_enabled: true`.
- BGP: `kube_vip_bgp_enabled: true` with `kube_vip_local_as`, `kube_vip_bgp_routerid` and `kube_vip_bgppeers` entries written like `192.168.0.10:65000::false`; optional `kube_vip_bgp_peeraddress`, `peerpass`, `peeras`, `sourceip`, `sourceif`.
- Control plane load balancing: `kube_vip_lb_enable: true`, with `kube_vip_lb_fwdmethod: masquerade`.

Leader election parameters:

```yaml
kube_vip_leaseduration: 30
kube_vip_renewdeadline: 20
kube_vip_retryperiod: 4
```

Metrics: `kube_vip_metrics_enabled: true`; `kube_vip_metrics_port` defaults to `2112`, matching upstream.

## Checked

2026-11-08. Cited pages re-read in full. Variables, the VIP wiring and defaults were confirmed on the kube-vip page.

Method: documentation only; no commands were run.
