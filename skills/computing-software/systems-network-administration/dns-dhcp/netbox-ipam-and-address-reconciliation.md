---
id: computing-software.systems-network-administration.dns-dhcp.netbox-ipam-and-address-reconciliation
name: netbox-ipam-and-address-reconciliation
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [ipam, ddi, netbox, netbox-ipam, ip-reconciliation, prefixes, ip-ranges, vrf, pynetbox, source-of-truth, arp-scan, dhcp-leases, dns-records, stale-addresses]
level: practitioner
status: draft
description: "Model addressing in NetBox (RIRs, aggregates, prefixes, ranges, IPs, VRFs, roles) and reconcile it with reality from ARP tables, DHCP leases, DNS and scans using pynetbox."
sources:
  - https://netboxlabs.com/docs/netbox/en/stable/features/ipam/
  - https://github.com/netbox-community/pynetbox
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NetBox IPAM and address reconciliation

## Model
| Object | Use |
|---|---|
| RIR / Aggregate | top-level blocks you own (RFC 1918 "RIR", your PI space) |
| VRF | separate address spaces (overlapping allowed between VRFs; enforce unique within) |
| Prefix (with role, site, VLAN, status container/active/reserved) | every subnet; containers for site/region summaries |
| IP Range | DHCP pools (mark as DHCP) so they are not handed out manually |
| IP Address (status active/reserved/deprecated/dhcp, dns_name, assigned interface) | statics, gateways, VIPs (role anycast/vip/vrrp) |
Use **Available prefixes / IPs** in the UI or API (`/api/ipam/prefixes/<id>/available-ips/`) to
allocate without collisions; tags and custom fields for owner/ticket.

## Reconciliation (documented vs real)
Sources of truth on the network:
- ARP/ND tables from gateways (SNMP ipNetToPhysicalTable or `show ip arp` via Netmiko).
- DHCP leases (Kea API `lease4-get-all`, Windows `Get-DhcpServerv4Lease`).
- DNS zones (AXFR or provider API) for names.
- Scans (`nmap -sn`) for hosts that are silent at layer 3 from your vantage.

```python
import pynetbox, ipaddress
nb = pynetbox.api("https://netbox.example.org", token=TOKEN)
documented = {str(ipaddress.ip_interface(i.address).ip): i for i in nb.ipam.ip_addresses.filter(parent="10.20.10.0/24")}
seen = set(arp_ips)            # from the gateway ARP table
for ip in seen - documented.keys():
    print("UNDOCUMENTED", ip)  # create as status=active with tag 'discovered', or ticket it
for ip, obj in documented.items():
    if ip not in seen and obj.status.value == "active":
        print("NOT SEEN", ip, obj.dns_name)   # candidate stale; check last-seen history before reclaiming
```
Run nightly; keep "last seen" in a custom field. Never auto-delete: flag and review (devices may be
off, on another VLAN, or silent).

## Drive configs from IPAM
Generate DHCP reservations/DNS records from NetBox (webhooks or scripts) so IPAM leads and drift
goes to zero; NetBox plugins (netbox-dns) or external DDI integrations exist.

## Verify
- [ ] Every active subnet is a prefix with site/VLAN/role; DHCP pools modelled as ranges.
- [ ] Reconciliation report trending toward zero undocumented and zero stale addresses.
