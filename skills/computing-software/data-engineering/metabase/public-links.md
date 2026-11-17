---
id: computing-software.data-engineering.metabase.public-links
name: public-links
category: computing-software
field: data-engineering
product: metabase
tags: [public-links, public-sharing, iframe, hash-parameters, hide-parameters, url-filters]
level: practitioner
status: docs-checked
description: "Create and control Metabase public links and iframes: admin toggle, URL formats, export extensions, appearance hash parameters, URL filters and their security limits."
sources:
  - https://www.metabase.com/docs/latest/embedding/public-links
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Access: only admins create public links. Public sharing is enabled by default; disable it at Admin, Settings, Public sharing. Earlier links work again after re-enabling unless deactivated.

Create: Share icon, Create a public link (questions, dashboards, documents).
- `/public/question/<uuid>` with `.csv`, `.xlsx` or `.json` appended for downloads (questions only).
- `/public/dashboard/<uuid>`.
- Append `?format_rows=false` for unformatted export rows.

Iframe: Share, Embed, Get embedding code. Appearance goes after `#`: `theme=night`, `bordered`, `titled`, `refresh` and `background` (dashboards only). `locale`, `font` and `downloads` need Pro or Enterprise; `downloads` takes `true`, `false`, `results` or `pdf`.

Filters: query parameters with lowercase underscore names, `/dashboard/42?id=7`. Hide widgets with `#hide_parameters=id,customer_name`. Repeat a parameter for multi-select (`?category=Gadget&category=Gizmo`). Values are case-sensitive and must be URL-encoded.

Gotchas:
- URL parameters are not secure: anyone can drop them and see the unfiltered original. Use guest embedding for locked filters.
- Drill-through does not work on public dashboards.
- Custom visualizations fall back to the default.
- Events saved with a question are visible to anyone with the link.
- `MB_JETTY_REQUEST_HEADER_SIZE` (default 8192 bytes) caps URL length; longer URLs fail with HTTP 414 and nothing is logged.

Audit and revoke: Admin, Public Sharing lists every shared item; click the X to deactivate.

## Checked
2026-11-03. Confirmed against the Metabase docs page Embedding, Public sharing: admin-only creation, default-on toggle and re-enable behaviour, export extensions and format_rows=false, iframe steps, appearance hash parameters with plan limits, downloads values, filter URL rules, hide_parameters, security caveat, drill-through and custom visualization limits, MB_JETTY_REQUEST_HEADER_SIZE (8192 bytes, HTTP 414), audit and deactivate path. Nothing removed.
Method: documentation only; no commands were run.
