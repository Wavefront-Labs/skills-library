---
id: computing-software.systems-network-administration.netbox.object-permissions-model
name: object-permissions-model
category: computing-software
field: systems-network-administration
product: netbox
tags: [object-permissions, constraints, user-token]
level: advanced
status: docs-checked
description: "Combine object types, actions and JSON constraints."
sources: ["https://netboxlabs.com/docs/netbox/administration/permissions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Object-based permissions

Goal: grant access to specific subsets of objects.

NetBox replaces Django's built-in model with object-based permissions. A permission needs at least one **object type**, one **user or group**, and one **action**; **constraints** are optional and without them the permission covers all instances.

**Actions:** view, add, change, delete, plus custom actions such as `sync` for data sources. All are stored as strings in the `actions` array.

**Constraints** are JSON using Django query filter syntax. Backslashes must be escaped. Attributes in one object are ANDed:

```json
{"status": "active", "region__name": "Americas"}
```

A list gives OR:

```json
[{"vid__gte": 100, "vid__lt": 200}, {"status": "reserved"}]
```

Multiple permissions on one object type merge their constraints with OR.

**`$user` token.** Use it as a value, or an item in a list of values, to reference the current user:

```json
{"created_by": "$user"}
```

It cannot reference specific user attributes.

**Checklist**

1. Assign to groups.
2. Test constraints as a sample user.
3. Remember permissions combine with OR.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Object-Based Permissions page (read in full).
