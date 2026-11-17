---
id: computing-software.cybersecurity-defensive.security-architecture.sdn-security
name: sdn-security
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [sdn-security, software-defined-networking, sdn-controller, nsx, cisco-aci, control-plane-security, microsegmentation]
level: advanced
status: draft
description: "Secure software-defined networks: protect the controller and northbound API, RBAC and change control on intent, southbound channel security and distributed firewall audit."
sources: ["https://docs.vmware.com/en/VMware-NSX/index.html", "https://www.cisco.com/c/en/us/solutions/data-center-virtualization/application-centric-infrastructure/index.html", "https://csrc.nist.gov/pubs/sp/800/125/b/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Software-defined networking security

In SDN the controller is the network: compromise it and you rewrite every path and firewall rule.

## Controls
| Plane | Control |
|---|---|
| Management / northbound API (NSX Manager, APIC, ONOS) | Dedicated management network, SSO with MFA, RBAC (read-only for most), API tokens scoped and rotated, IP allow-list |
| Control plane (controller cluster) | Cluster nodes in the management VRF, encrypted inter-node traffic, backups encrypted and tested |
| Southbound (controller <-> switches/hosts: OpenFlow, OpFlex, NSX control channel) | TLS with certificate pinning; reject unauthenticated switches; disable passive/listening OpenFlow modes |
| Data plane | Distributed firewall default rule set to deny/drop for in-scope segments, not allow |

## Change control
- Treat intent (NSX DFW sections, ACI contracts) as code: export via API, keep in Git, review diffs, apply via pipeline (Terraform NSX-T / ACI providers).
- Alert on rule changes outside the pipeline (audit logs: NSX `/api/v1/logical-router` and DFW audit events, APIC audit log).

## Gotchas
- ACI "vzAny"/"permit any" contracts and NSX "Any-Any-Allow" default rules are common, quietly undoing segmentation.
- Controller backups contain credentials and the full topology; protect like the controller.
- Many SDN UIs default to local admin accounts that bypass SSO; disable or vault them.

## Verify
- [ ] Northbound API not reachable from user networks.
- [ ] DFW default rule = drop for segmented zones, with logging.
- [ ] Rule changes in the last 30 days all trace to a pipeline run/ticket.
