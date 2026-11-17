---
id: computing-software.systems-network-administration.netbox.vlan-groups-and-interfaces
name: vlan-groups-and-interfaces
category: computing-software
field: systems-network-administration
product: netbox
tags: [vlan, vlan-group, 802-1q]
level: practitioner
status: docs-checked
description: "Model VLANs per IEEE 802.1Q and assign them to interface modes."
sources: ["https://netboxlabs.com/docs/netbox/features/vlan-management/", "https://netboxlabs.com/docs/netbox/reference/filtering/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# VLAN management

Goal: track layer two VLANs and where they apply.

NetBox models VLANs per IEEE 802.1Q with a 12-bit VLAN ID and a name. Each VLAN has an operational status and may take a functional role, as prefixes do.

**VLAN groups.** A group is a collection of VLANs within a scope. It can be associated with a site, location, rack or similar object to indicate its domain, and it designates a minimum and maximum VLAN ID. Within a group each VLAN must have a unique ID and name. There is no limit to the number of groups per scope.

**Interfaces.** Once defined, VLANs can be associated with device and virtual machine interfaces. Each interface has an 802.1Q mode, access or tagged, and the relevant VLANs are applied as tagged or untagged.

**Related**

- L2VPN and overlay networks such as VXLAN and EVPN can be tied to interfaces and VLANs.
- List filters accept lookups, for example `vid__gt=900`.

**Checklist**

1. Create a group per scope with a range.
2. Keep IDs and names unique in the group.
3. Set the interface mode before assigning VLANs.

## Checked

Method: docs-checked 2026-11-09 against the NetBox VLAN Management feature page and the REST API filtering reference (both read in full). Removed the unconfirmed claim that prefixes link to a VLAN.
