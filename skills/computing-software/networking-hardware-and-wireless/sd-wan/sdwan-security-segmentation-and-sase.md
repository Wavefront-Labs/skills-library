---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-security-segmentation-and-sase
name: sdwan-security-segmentation-and-sase
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-segmentation, sase-sse, cloud-security-service-edge, sdwan-security]
level: advanced
status: draft
description: "Segment traffic into VPNs/VRFs, run local firewall or send internet traffic to a cloud security service (SSE/SASE)."
sources:
  - https://www.mef.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Segmentation and SASE

- Segment by service VPN/VRF (corporate, guest, IoT, PCI) and control inter-segment access explicitly through a firewall.
- Edge capabilities: stateful firewall, IPS, URL filtering, DNS security on the branch edge, or tunnel internet-bound traffic to a cloud security service (SSE/SASE: secure web gateway, CASB, ZTNA).
- Tunnel to the cloud service via IPsec/GRE; plan redundancy to two points of presence.
- Certificates and keys: rotate controller/edge certificates; protect the orchestrator with MFA and RBAC.
- Defensive: log and monitor tunnels, policy changes and failed authentications.

## Verify
- [ ] A test client in the guest VPN cannot reach corporate resources and internet traffic shows in the security service logs.
