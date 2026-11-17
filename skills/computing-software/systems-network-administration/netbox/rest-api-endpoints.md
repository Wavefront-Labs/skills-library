---
id: computing-software.systems-network-administration.netbox.rest-api-endpoints
name: rest-api-endpoints
category: computing-software
field: systems-network-administration
product: netbox
tags: [rest-api, swagger-ui, api-ordering]
level: practitioner
status: docs-checked
description: "Use the endpoint hierarchy, list and detail views, filters and ordering."
sources: ["https://netboxlabs.com/docs/netbox/integrations/rest-api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REST API endpoints

Goal: find and call the right endpoint.

All endpoints sit under `https://<hostname>/api/`. The root is divided by application: circuits, DCIM, extras, IPAM, plugins, tenancy, users and virtualization. Examples: `/api/circuits/providers/`, `/api/dcim/sites/`, `/api/dcim/devices/`.

**Interactive docs.** A running instance serves a sandbox at `/api/schema/swagger-ui/`. Browsing to `/api/` shows the full endpoint hierarchy.

**Views.** Each model has a list view and a detail view.

- `/api/dcim/devices/`: list, or create a device.
- `/api/dcim/devices/123/`: retrieve, update or delete device 123.

**Filtering and ordering** use query parameters:

```
GET /api/dcim/interfaces/?device_id=123
GET /api/dcim/interfaces/?device_id=123&ordering=-created
```

The second sorts newest first.

**Auth example**

```
curl -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json; indent=4" \
  http://netbox/api/dcim/sites/
```

**Related objects.** Foreign keys in responses appear as nested brief representations carrying a URL, and every object has a primary key named `id` used in detail URLs.

**Checklist**

1. Start from Swagger UI.
2. Use list for create, detail for change.
3. Order with a leading minus for descending.

## Checked

Method: docs-checked 2026-11-09 against the NetBox REST API overview page (read in full). Removed the unconfirmed note on the Accept header.
