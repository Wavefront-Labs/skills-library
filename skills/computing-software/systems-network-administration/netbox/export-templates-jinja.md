---
id: computing-software.systems-network-administration.netbox.export-templates-jinja
name: export-templates-jinja
category: computing-software
field: systems-network-administration
product: netbox
tags: [export-templates, queryset, as-attachment]
level: practitioner
status: docs-checked
description: "Render objects with Jinja2 from the UI export button or REST API."
sources: ["https://netboxlabs.com/docs/netbox/customization/export-templates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Export templates

Goal: produce custom text output for a list of objects.

Create them under Customization > Export Templates. Each is tied to one object type and appears under that list's Export button. They must be written in Jinja2. The name `table` is reserved.

**Template variable.** Results are in `queryset`:

```
{% for rack in queryset %}
Rack: {{ rack.name }}
Site: {{ rack.site.name }}
Height: {{ rack.u_height }}U
{% endfor %}
```

- Custom fields: `{{ obj.cf.color }}`.
- Config context: `{% set data = server.get_config_context() %}`.

**Options.** `as_attachment` true returns a downloadable file; false displays in the browser. An optional MIME type and file extension can be set; the default MIME type is `text/plain`.

**REST API.** When authentication is required (for example `LOGIN_REQUIRED`), render via the API so a token can be sent:

```
GET /api/dcim/sites/?export=MyTemplateName
```

The body contains only the rendered content, not JSON.

**Security.** Templates run user-submitted code; grant create and modify rights only to trusted users.

**Checklist**

1. Iterate over `queryset`.
2. Use the API for authenticated export.
3. Restrict editing.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Export Templates page (read in full).
