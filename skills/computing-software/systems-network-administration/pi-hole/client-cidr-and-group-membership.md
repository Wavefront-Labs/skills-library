---
id: computing-software.systems-network-administration.pi-hole.client-cidr-and-group-membership
name: client-cidr-and-group-membership
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [client-subnets, group-management, default-group]
level: advanced
status: docs-checked
description: "Manage Pi-hole groups and clients, including CIDR subnet clients and the special Default group 0."
sources: ["https://docs.pi-hole.net/group_management/", "https://docs.pi-hole.net/group_management/example/", "https://docs.pi-hole.net/database/domain-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Groups and clients

Any subscribed list, allowlist, denylist or regex entry can be managed through groups. This lets you relate entries and enable or disable them together, for example to allow a service only temporarily.

**Tables.** Groups live in the `group` table. Linking tables `domainlist_by_group`, `adlist_by_group` and `client_by_group` connect IDs, so domains, subscribed lists and clients can belong to zero, one or several groups.

**Default group.** Group `Default` (`group_id` 0) is automatically assigned to every new client or domain. It cannot be deleted. Disabling it disables blocking for all unmanaged devices.

**Client identification.** Clients are identified by IP address, and you can use CIDR notation for broad clients:

- `192.168.1.0/24` matches 256 devices
- `10.8.0.0/16` matches 65,536 devices
- `2001:db8::/48` works for IPv6

Any CIDR block is allowed, not only multiples of 4.

**Surprises.** Domains enabled in some groups and disabled in others can give unexpected behaviour.

**Checklist**

1. Create groups before clients.
2. Add clients and link them to groups.
3. Remove Default membership for clients that should be exempt.
4. Run `pihole reloadlists` after database changes.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Group Management (group_management); Per-client blocking example (group_management/example); Domain Database (database/domain-database). Removed the column list of the `group` table and the claim that a group is reusable for both allow and deny entries (neither is on the pages). Added the per-client example page for the Default group rules.
Method: documentation only; no commands were run.
