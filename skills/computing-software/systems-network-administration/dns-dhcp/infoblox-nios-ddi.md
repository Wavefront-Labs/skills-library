---
id: computing-software.systems-network-administration.dns-dhcp.infoblox-nios-ddi
name: infoblox-nios-ddi
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [ipam, infoblox-nios, ddi, wapi, grid, dns, dhcp]
level: practitioner
status: draft
description: "Operate Infoblox NIOS DDI: Grid members and roles, DNS views and zones, DHCP ranges and fixed addresses, the WAPI REST API and safe change practices."
sources:
  - https://docs.infoblox.com/space/nios90/
  - https://docs.infoblox.com/space/niosapi/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Infoblox

Infoblox NIOS combines DNS, DHCP and IPAM (DDI) in a Grid: a Grid Master holds the database and
pushes configuration to members that serve DNS/DHCP.

## Concepts
| Object | Meaning |
|--------|---------|
| Grid Master / Grid Master Candidate | central DB; candidate takes over on failure (manual promote) |
| Members | appliances/VMs running DNS, DHCP, NTP, etc. |
| Network view / DNS view | separate address spaces / split-horizon DNS |
| Network / range / fixed address / reservation | IPAM and DHCP objects |
| Host record | one object creating A, PTR and optionally DHCP fixed address |
| Extensible attributes (EAs) | custom metadata (site, owner, VLAN) |

Many changes require **Restart Services** on members to take effect (GUI banner); schedule restarts.

## WAPI (REST)
```
curl -k -u admin:pass "https://gm.example.com/wapi/v2.12/network?network=10.30.0.0/24&_return_fields+=extattrs"
curl -k -u admin:pass -X POST "https://gm.example.com/wapi/v2.12/record:host" -H 'Content-Type: application/json' -d '{
  "name":"srv7.corp.example.com","ipv4addrs":[{"ipv4addr":"10.30.0.57","configure_for_dhcp":false}],
  "extattrs":{"Owner":{"value":"platform"}} }'
curl -k -u admin:pass -X POST "https://gm.example.com/wapi/v2.12/grid?_function=restartservices" -d '{"restart_option":"RESTART_IF_NEEDED"}'
```
Responses return `_ref` strings used for updates (`PUT /wapi/v2.12/<_ref>`) and deletes.
Use the `infoblox-client` Python library or Ansible `infoblox.nios_modules` for automation.

## Safe practices
- Read-only API users for discovery; scoped admin groups per network view.
- Use EAs consistently; reporting and automation depend on them.
- Back up the Grid (scheduled backups off-box) before upgrades; upgrade via the Grid Master in
  distribution then upgrade phases.

## Verify
- [ ] Objects created via WAPI appear in the GUI, DNS answers after service restart, and scheduled Grid backups succeed.
