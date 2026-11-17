---
id: computing-software.cloud-infrastructure-engineering.graylog.index-set-templates
name: index-set-templates
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [index-set-templates, hot-tier, warm-tier, retention-profile]
level: practitioner
status: docs-checked
description: "Create index sets from built-in or custom index set templates describing hot and warm tier retention, with license and OpenSearch requirements."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/index_set_templates.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# index set templates

Templates let you create index sets with a predefined tier profile, build custom templates, and set a default template.

Requirements: a Graylog Enterprise license to use a warm tier; OpenSearch 2.12+ or Graylog Data Node.

Built-in templates:
- **7 days Hot, 90 Days Total**: lowest search backend specification, least hot storage, for rarely searched data.
- **14 days Hot, 90 Days Total**: short hot period, then cost-effective warm storage for compliance.
- **30 days Hot, 90 Days Total**: highest specification and most hot storage, for high-value, often searched data.

To use one: **System > Indices > Create index set**, then choose a template.

## Checked

2026-11-04. Confirmed against the cited page. Nothing removed.

Method: documentation only; no commands were run.
