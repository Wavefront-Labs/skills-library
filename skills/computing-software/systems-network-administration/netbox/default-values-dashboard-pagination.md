---
id: computing-software.systems-network-administration.netbox.default-values-dashboard-pagination
name: default-values-dashboard-pagination
category: computing-software
field: systems-network-administration
product: netbox
tags: [default-dashboard, paginate-count, powerfeed-defaults]
level: practitioner
status: docs-checked
description: "Configure the default dashboard, page size and power feed or rack elevation defaults."
sources: ["https://netboxlabs.com/docs/netbox/configuration/default-values/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Default values

Goal: change defaults new objects and users receive.

Most of these are marked Dynamic Configuration Parameters, meaning they can also be changed from the UI configuration revision.

**Dashboard.** `DEFAULT_DASHBOARD` is an iterable of widget dictionaries for new users' dashboards. Attributes: `widget` (dotted class path, required), `width` (1 to 12), `height` (rows), `title`, `color` (title bar), and `config` (widget parameters). Example:
```
DEFAULT_DASHBOARD = [{
    'widget': 'extras.ObjectCountsWidget',
    'width': 4, 'height': 3, 'title': 'Organization',
    'config': {'models': ['dcim.site', 'tenancy.tenant']}
}]
```
Users can customise their own dashboard afterwards.

**Other defaults**

- `DEFAULT_USER_PREFERENCES`: preferences set on newly created accounts.
- `PAGINATE_COUNT`: 50 objects per page.
- `POWERFEED_DEFAULT_AMPERAGE` 15, `POWERFEED_DEFAULT_MAX_UTILIZATION` 80 (percent), `POWERFEED_DEFAULT_VOLTAGE` 120.
- `RACK_ELEVATION_DEFAULT_UNIT_HEIGHT` 22 and `RACK_ELEVATION_DEFAULT_UNIT_WIDTH` 220 pixels; height should be roughly one tenth of the width.

`PAGINATE_COUNT` sets the default maximum number of objects shown per page in each list of objects; the dashboard widget `width` is a value between 1 and 12 inclusive.

**Checklist**

1. Dashboard defaults only affect new dashboards.
2. Use consistent power defaults.
3. Keep elevation aspect ratio.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Default values page: DEFAULT_DASHBOARD widget attributes, PAGINATE_COUNT, POWERFEED_DEFAULT_* values, RACK_ELEVATION_DEFAULT_UNIT_* values and the dynamic-parameter note. Removed: Nothing.

Method: documentation only; no commands were run.
