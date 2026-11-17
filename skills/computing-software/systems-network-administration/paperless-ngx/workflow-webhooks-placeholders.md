---
id: computing-software.systems-network-administration.paperless-ngx.workflow-webhooks-placeholders
name: workflow-webhooks-placeholders
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, webhooks, workflow-placeholders, jinja, paperless-webhooks-allowed-ports, localize-date]
level: advanced
status: docs-checked
description: "Send workflow webhooks safely and build titles and payloads from Jinja placeholders, restricting ports, schemes and internal targets."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/advanced_usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow webhooks and placeholders

## Webhook action
It sends a POST request to a URL. You set the URL, the body as text or key-value pairs (placeholders allowed), the encoding (JSON or form data) and the request headers as key-value pairs.

## Restricting webhooks
- `PAPERLESS_WEBHOOKS_ALLOWED_SCHEMES`: comma-separated; default `http,https`.
- `PAPERLESS_WEBHOOKS_ALLOWED_PORTS`: comma-separated; default is an empty list, which allows all ports. Setting `80,443` limits webhooks to URLs using those ports.
- `PAPERLESS_WEBHOOKS_ALLOW_INTERNAL_REQUESTS`: default true; set to `false` to block internal URLs such as localhost.
If you allow non-admins to create workflows, consider adjusting these settings to prevent abuse.

## Placeholders
Titles and webhook payloads can use Jinja templates. Available with any trigger type: `{{correspondent}}`, `{{document_type}}`, `{{owner_username}}`, `{{added}}` with `added_year`, `added_year_short`, `added_month`, `added_month_name`, `added_month_name_short`, `added_day` and `added_time` (HH:MM), `{{original_filename}}`, `{{filename}}` (for "added" workflows it may not be final yet), `{{custom_fields}}` and `{{doc_title}}` (not usable in title assignment).

Only for "added" or "updated" triggers: `{{created}}` with the same set of parts (`created_year` and so on), `{{doc_url}}` (requires `PAPERLESS_URL`) and `{{doc_id}}`.

The inputs differ by trigger because, at consumption time, no automatic tags and the like have been applied yet.

## Examples
```jinja2
{{ created | localize_date('MMMM', 'en_US') }}
{{ custom_fields | get_cf_value("Invoice", "") }}
```
`localize_date` formats a date into a localised string using Babel (arguments: format and locale; it needs a date or datetime object such as `created`, or an ISO string). `get_cf_value("Invoice", "")` gives a fallback when the field is missing; `{{ custom_fields.Invoice.value }}` also works.

## Checked
Date: 2026-11-07
Pages read in full: usage (docs/usage.md), configuration (docs/configuration.md), advanced_usage (docs/advanced_usage.md; the post-consumption example file included by snippet was not opened).
Corrections: removed the unsupported statement that correspondent and similar placeholders are "empty" at consumption start (the page says only that no automatic tags etc. have been applied); added the exact defaults and the full placeholder list; described localize_date from the advanced_usage page.
Method: documentation only; no commands were run.
