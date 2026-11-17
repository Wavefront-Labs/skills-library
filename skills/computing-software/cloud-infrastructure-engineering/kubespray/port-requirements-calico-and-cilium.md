---
id: computing-software.cloud-infrastructure-engineering.kubespray.port-requirements-calico-and-cilium
name: port-requirements-calico-and-cilium
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ports, calico, cilium, bgp, vxlan, wireguard, hubble]
level: practitioner
status: docs-checked
description: "Firewall ports a Kubespray cluster needs when running Calico (BGP, VXLAN, Typha, WireGuard, IPIP) or Cilium (health, Hubble, VXLAN, metrics, WireGuard)."
sources:
  - https://kubespray.io/docs/operations/port-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Calico** requires:

| Protocol | Port | Used for |
|---|---|---|
| TCP | 179 | Calico networking (BGP) |
| UDP | 4789 | VXLAN enabled |
| TCP | 5473 | Typha enabled |
| UDP | 51820 | IPv4 WireGuard |
| UDP | 51821 | IPv6 WireGuard |
| IPENCAP / IPIP | - | IPIP enabled |

**Cilium** requires:

| Protocol | Port | Used for |
|---|---|---|
| TCP | 4240 | Cilium health checks (cilium-health) |
| TCP | 4244 | Hubble server |
| TCP | 4245 | Hubble Relay |
| UDP | 8472 | VXLAN overlay |
| TCP | 9962 | cilium-agent Prometheus metrics |
| TCP | 9963 | cilium-operator Prometheus metrics |
| TCP | 9964 | cilium-proxy Prometheus metrics |
| UDP | 51871 | WireGuard tunnel endpoint |
| ICMP | - | health checks |

The page links to the Calico requirements and Cilium v1.13 system requirements for the authoritative lists, so consult those if you run a different release.

## Checked

2026-11-04. Both tables were confirmed on the Port Requirements page. Removed an inference about opening only what the encapsulation mode needs.

Method: documentation only; no commands were run.
