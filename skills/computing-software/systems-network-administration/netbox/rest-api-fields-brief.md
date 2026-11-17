---
id: computing-software.systems-network-administration.netbox.rest-api-fields-brief
name: rest-api-fields-brief
category: computing-software
field: systems-network-administration
product: netbox
tags: [api-fields, brief-format, omit]
level: practitioner
status: docs-checked
description: "Use fields, omit and brief to cut payload size and query cost."
sources: ["https://netboxlabs.com/docs/netbox/integrations/rest-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Specifying fields and brief format

Goal: speed up large API reads.

By default a response contains every field. Request a subset with `fields`:

```
GET /api/dcim/sites/?fields=id,name,status,region
```

Or leave specific ones out with `omit`:

```
GET /api/dcim/sites/?omit=circuit_count,device_count,virtualmachine_count
```

Excluding fields that reference related objects reduces the number and complexity of underlying database queries, which can drastically improve performance. The two parameters are mutually exclusive; if both are passed, `fields` takes precedence.

**Brief format.** Most endpoints support `?brief=true`, which returns a minimal representation of each object, useful when you need only a list of choices without related data:

```
GET /api/ipam/prefixes/13980/?brief=true
```

**Related objects.** Foreign keys in a complete response appear as nested brief representations with a URL and enough data to display the object.

**Checklist**

1. Prefer `fields` for known columns.
2. Use `omit` to drop expensive counts.
3. Use `brief` for pickers.

## Checked

Method: docs-checked 2026-11-09 against the NetBox REST API overview page (read in full). Removed the unconfirmed serializer comparison.
