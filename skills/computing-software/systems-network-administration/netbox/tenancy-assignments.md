---
id: computing-software.systems-network-administration.netbox.tenancy-assignments
name: tenancy-assignments
category: computing-software
field: systems-network-administration
product: netbox
tags: [tenancy, tenant-groups, resource-allocation]
level: practitioner
status: docs-checked
description: "Assign racks, prefixes, VMs and more to tenants and nest tenant groups."
sources: ["https://netboxlabs.com/docs/netbox/features/tenancy/", "https://netboxlabs.com/docs/netbox/features/context-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tenancy

Goal: tie objects to a customer or business unit.

Tenancy is the association of an object with a tenant to convey assignment or dependency. A tenant typically represents a customer or internal organization, though it can serve any purpose.

**Tenant groups** may be nested recursively. For example, a parent "Customers" group might contain "Current" and "Past" children.

**Assignable objects** include circuits, circuit groups, virtual circuits, cables, devices, virtual device contexts, power feeds, racks, rack reservations, sites, locations, ASNs, ASN ranges, aggregates, prefixes, IP ranges, IP addresses, VLANs, VLAN groups, VRFs, route targets, clusters, virtual machines, L2VPNs, tunnels, wireless LANs and wireless links.

**One tenant only.** Tenancy represents dedication of an object to one tenant, so each object takes a single tenant. A firewall dedicated to a customer goes to that tenant.

**Use.** Because so many object types accept a tenant, you can filter by tenant to correlate each customer's racks, address space and devices in one view. Tenant is also a match criterion for config contexts.

**Checklist**

1. Design tenant groups first.
2. Assign one tenant per object.
3. Filter by tenant for reporting.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Tenancy and Context Data feature pages (read in full).
