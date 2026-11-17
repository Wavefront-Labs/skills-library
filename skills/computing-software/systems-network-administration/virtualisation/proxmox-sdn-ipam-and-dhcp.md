---
id: computing-software.systems-network-administration.virtualisation.proxmox-sdn-ipam-and-dhcp
name: proxmox-sdn-ipam-and-dhcp
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [sdn-ipam, pve-ipam, pve-sdn, dnsmasq, netbox, phpipam, snat, dhcp-range, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Use Proxmox SDN subnets with IPAM and DHCP: built-in PVE IPAM vs NetBox/phpIPAM, DHCP ranges via dnsmasq in Simple zones, SNAT, and DNS registration."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesdn.html
  - https://github.com/proxmox/pve-docs/blob/master/pvesdn.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox SDN IPAM and DHCP

**Goal:** guests on SDN vnets get addresses automatically and those addresses are tracked
in an IPAM rather than a spreadsheet.

## IPAM plugins
| Plugin | Notes |
|---|---|
| `pve` (default) | Built-in; inspect, create, edit and delete IP mappings in Datacenter → SDN → IPAM |
| NetBox | Needs URL (`.../api`), API token and the SHA-256 fingerprint of the API certificate |
| phpIPAM | Needs URL (`.../api/<appname>/`), API token and the section ID (default installations use `sectionid=1`) |
A single IPAM instance can serve several zones. IPAM including DHCP management is documented as tech preview.

## Subnets
VNet → Subnets → Add: CIDR, gateway (deployed on the vnet in layer 3 zones: Simple and EVPN), **SNAT** (guests reach the outside by forwarding through the node's outgoing interface), DNS zone prefix. If an IPAM is associated with the zone, the subnet prefix is registered in it.

## DHCP (since PVE 8.1; Simple zones; via dnsmasq; opt-in, tech preview)
1. `apt install dnsmasq` on all nodes, then disable the default instance:
   `systemctl disable --now dnsmasq`.
2. Zone → advanced options → enable **automatic DHCP**.
3. Subnet (a gateway is required, otherwise automatic DHCP does not work) → **DHCP ranges**, in the GUI or with
   `pvesh set /cluster/sdn/vnets/<vnet>/subnets/<subnet> -dhcp-range start-address=10.0.1.100,end-address=10.0.1.200`.
4. Apply. When a NIC is added to a guest on the vnet, an IP is allocated in the IPAM within the configured ranges; when the guest starts, a MAC-to-IP mapping is created in the zone's dnsmasq. Removing the NIC or destroying the guest deletes the IPAM and DHCP entries.

The plugin runs one service per zone, `dnsmasq@<zone>`, and writes generated files in `/etc/dnsmasq.d/<zone>`; do not edit them, add your own such as `90-custom.conf`. Leases are in `/var/lib/misc/dnsmasq.<zone>.leases`.

## DNS registration
The DNS plugin (PowerDNS) registers hostname and IP for the subnet IPs of the zones it is associated with. PowerDNS needs `api=yes`, an `api-key` and `webserver=yes`; the plugin takes `url`, `key` and `ttl`.

## Gotchas
- Currently only Simple zones support automatic DHCP, and dnsmasq is the only DHCP backend.
- Adding, editing and removing IP mappings (and changing DHCP leases) is only available with the PVE IPAM plugin; after editing a DHCP-assigned IP, make the guest renew its lease.
- With the PVE IPAM the firewall generates an IP set `guest-ipam-<vmid>` per guest; removing all of a guest's IPAM entries while rules still reference that set makes the firewall fail to update.

## Verify
The IPAM panel shows the guest's MAC and IP, and the guest's DHCP lease matches it.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvesdn.adoc, last pushed 2026-10-17). Confirmed: IPAM plugin properties for PVE, NetBox and phpIPAM; DHCP prerequisites (`dnsmasq` install and disable), Simple-zone-only support, gateway requirement, `-dhcp-range` syntax, `dnsmasq@<zone>` service, config and lease paths; PowerDNS options; PVE-IPAM-only mapping edits; `guest-ipam-<vmid>` IP sets; tech-preview status. Also confirmed: DHCP integration into IPAM was added in Proxmox VE 8.1. Removed: the VLAN-zone DHCP remark, the new-vnet reallocation claim and the external-IPAM failure claim (not documented).

Method: documentation only; no commands were run.
