---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-tenant-ids
name: grafana-mimir-tenant-ids
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [tenant-id, multitenancy, validation, identifiers]
level: intro
status: docs-checked
description: "States the rules for Grafana Mimir tenant IDs: length limit, allowed characters and reserved names. Use when choosing tenant names for a cluster."
sources: ["https://grafana.com/docs/mimir/latest/configure/about-tenant-ids/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mimir tenant IDs

A tenant ID is the unique identifier of a tenant within a Grafana Mimir cluster.

## Restrictions

- Maximum length is 150 bytes or characters.
- Allowed: alphanumerics (`0-9`, `a-z`, `A-Z`) and the special characters exclamation point (`!`), hyphen (`-`), underscore (`_`), single period (`.`), asterisk (`*`), single quote (`'`), open and close parenthesis.
- `.` and `..` are not valid tenant IDs, for security reasons.
- `__mimir_cluster` is not valid because Mimir uses the name internally.
- All other characters, including slashes and whitespace, are unsupported.

How components use tenant IDs for authentication and authorization is covered in the Mimir authentication and authorization docs.

## Checked

2026-11-04. Confirmed against the Mimir page "About Grafana Mimir tenant IDs": length limit, allowed characters, `.`/`..` and `__mimir_cluster`. Removed the "Practical use" section (metric name, YAML quoting advice; not on the page).
Method: documentation only; no commands were run.
