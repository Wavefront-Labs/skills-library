---
id: computing-software.systems-network-administration.netbox.rest-api-related-and-generic
name: rest-api-related-and-generic
category: computing-software
field: systems-network-administration
product: netbox
tags: [generic-relations, assigned-object-type, nested-objects]
level: advanced
status: docs-checked
description: "Set foreign keys by ID or attributes and assign IPs to interfaces."
sources: ["https://netboxlabs.com/docs/netbox/integrations/rest-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Related and generic objects in writes

Goal: create objects that reference others.

**By ID or by attributes.** When creating a device, give the rack by primary key:

```json
{"name": "MyNewDevice", "rack": 123}
```

or by attributes that identify it uniquely:

```json
{"name": "MyNewDevice",
 "rack": {"site": {"name": "Equinix DC6"}, "name": "R204"}}
```

If the attributes do not match exactly one object, a validation error is raised. Attribute lookups are restricted to objects the user may view, which prevents enumeration.

**Generic relations.** Some fields can reference several types, for example an IP address assigned to a device interface or VM interface. Supply:

- `assigned_object_type`: content type as `<app>.<model>`
- `assigned_object_id`: the numeric ID

```
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://netbox/api/ipam/ip-addresses/ \
  --data '{"address": "192.0.2.1/24",
   "assigned_object_type": "dcim.interface",
   "assigned_object_id": 69023}'
```

For a VM use `virtualization.vminterface`.

**Checklist**

1. Prefer IDs for speed.
2. Use attributes for readable payloads.
3. Set both generic fields.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: REST API page: related object by ID or attributes, generic relation fields assigned_object_type/assigned_object_id, dcim.interface and virtualization.vminterface. Removed: Nothing.

Method: documentation only; no commands were run.
