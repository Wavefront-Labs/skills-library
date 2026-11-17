---
id: computing-software.systems-network-administration.netbox.rest-api-filter-lookups
name: rest-api-filter-lookups
category: computing-software
field: systems-network-administration
product: netbox
tags: [filtering, lookup-expressions, choice-fields]
level: practitioner
status: docs-checked
description: "Use query parameters, custom field filters and OPTIONS to find choice values."
sources: ["https://netboxlabs.com/docs/netbox/reference/filtering/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# API filtering

Goal: query list endpoints precisely.

Attach parameters to a list URL: `GET /api/dcim/sites/?status=active`. Joined parameters narrow results: `?status=active&region=europe`. Repeating one parameter generally ORs the values: `?region=north-america&region=south-america`.

**Choice fields.** To list valid values for a field such as Prefix `status`, make an authenticated OPTIONS request:

```
curl -s -X OPTIONS -H "Authorization: Bearer $TOKEN" \
  http://netbox/api/ipam/prefixes/ | jq ".actions.POST.status.choices"
```

This works only if the token may POST to that endpoint. The prefix result lists container, active, reserved and deprecated.

**Custom fields.** Prepend `cf_`:

```
GET /api/dcim/sites/?cf_foo=123
GET /api/dcim/sites/?cf_managed__empty=true
```

Boolean custom fields support `empty`; a value of false is not empty. String custom fields use loose or exact matching depending on their filter setting.

**Lookup expressions.** Suffix a field name with `__n` for negation, for example `mac_address__n`. Numeric fields accept suffixes such as `lt`, `gt` and `empty` (for example `vid__gt=900`).

**Checklist**

1. Use OPTIONS for choice values.
2. Use `cf_` for custom fields.
3. Repeat a parameter for OR (but repeating `tag` is AND; use `tag__any` for OR).

## Checked

Method: docs-checked 2026-11-09 against the NetBox REST API filtering reference (read in full).
