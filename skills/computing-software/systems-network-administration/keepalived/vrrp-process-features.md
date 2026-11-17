---
id: computing-software.systems-network-administration.keepalived.vrrp-process-features
name: vrrp-process-features
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, vrrp, rfc-2338, sync-groups, ipsec-ah, use-vmac, notify-scripts, multicast]
level: practitioner
status: docs-checked
description: "VRRP child process features: RFC 2338 failover, sync groups, IPSEC-AH MD5-96 authentication, transition scripts, virtual MAC, multicast 224.0.0.18."
sources:
  - https://keepalived.readthedocs.io/en/latest/software_design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VRRP process features

The VRRP child implements RFC 2338 failover with extensions for LVS and firewall use.

- **Sync groups** (`vrrp_sync_group`) keep related instances in the same state.
- **Authentication:** IPSEC-AH with MD5-96 protects advertisements.
- **Scripts:** external scripts can run on state transitions. They run in a forked process so the main timer is not disturbed.
- **Virtual MAC:** `use_vmac` creates a macvlan interface such as `vrrp.250`; the `vmac_xmit_base` option sends VRRP traffic over the physical interface.
- VRRP code can run without LVS support.

Supporting components:
- Netlink reflector sets the VIPs and keeps interface state in sync with the kernel.
- VRRP advertisements use multicast address 224.0.0.18.
- SMTP and syslog carry notifications and daemon messages.

Verify: ip address output on the MASTER shows the VIPs, and advertisements to 224.0.0.18 are visible on the interface.

## Checked

2026-11-04. Confirmed RFC 2338, sync groups, IPSEC-AH MD5-96, forked transition scripts, use_vmac with macvlan and vmac_xmit_base, LVS independence, the Netlink reflector, multicast 224.0.0.18 and SMTP and syslog notification on the Software Design page. Nothing removed.

Method: documentation only; no commands were run.
