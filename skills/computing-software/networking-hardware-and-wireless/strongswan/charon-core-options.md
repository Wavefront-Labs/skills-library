---
id: computing-software.networking-hardware-and-wireless.strongswan.charon-core-options
name: charon-core-options
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, charon, install-routes, routing-table, keep-alive, dos-protection, interfaces-use]
level: practitioner
status: docs-checked
description: "Common strongswan.conf charon options: threads, install_routes, routing_table, install_virtual_ip, interfaces_use, keep_alive, dos_protection, rsa_pss, user and group."
sources:
  - https://docs.strongswan.org/docs/latest/config/strongswanConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# charon core options
Selected `charon.*` settings in strongswan.conf:

- `threads` (16): worker threads; several are reserved for long-running tasks, so do not set it too low.
- `install_routes` (yes): install routes into a separate routing table for established tunnels. Disabled, a more efficient source and next-hop lookup is used. `routing_table` (220) and `routing_table_prio` (220) pick the table and its priority.
- `install_virtual_ip` (yes): install virtual IPs; `install_virtual_ip_on` names the interface, otherwise the outbound interface is used.
- `interfaces_use`: comma-separated interfaces charon uses; all others are ignored. `interfaces_ignore` lists interfaces to ignore and has no effect when `interfaces_use` is set.
- `keep_alive` (20s): NAT keep alive interval.
- `dos_protection` (yes): cookies and aggressiveness checks against denial of service.
- `follow_redirects` (yes): follow IKEv2 redirects (RFC 5685).
- `rsa_pss` (no): use RSA-PSS padding by default instead of PKCS#1.
- `integrity_test` (no): check charon and libraries at startup.
- `flush_auth_cfg` (no): release authentication objects (certificates, identities) once an IKE_SA is established; may conflict with plugins needing them later.
- `user` / `group`: drop to this user after startup.
- `x509.enforce_critical` (yes): discard certificates with unsupported critical extensions.

## Checked
2026-11-04. Confirmed against the strongswan.conf page: every option and default listed above. Removed an unsupported pointer to other topics.

Method: documentation only; no commands were run.
