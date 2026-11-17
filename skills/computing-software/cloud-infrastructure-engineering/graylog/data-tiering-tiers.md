---
id: computing-software.cloud-infrastructure-engineering.graylog.data-tiering-tiers
name: data-tiering-tiers
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [data-tiering, hot-tier, warm-tier, searchable-snapshots, archive-tier]
level: practitioner
status: docs-checked
description: "Understand Graylog data tiering: hot tier, Enterprise warm tier on searchable snapshots, and the archive, with cost trade-offs."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/data_tiering.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# data tiering tiers

Tiers group data by storage and management needs, classed by performance requirements, frequency of use and cost efficiency. Data Tiering is recommended for self-managed installations (Cloud customers have it handled).

- **Hot tier**: the search backend cluster. Default for incoming data; easy to search, highest operating cost.
- **Warm tier** (Enterprise): data still searchable but slower, stored in searchable snapshots on lower-cost storage.
- **Archive**: inactive storage for long retention.

Requirements: Enterprise license for a warm tier; administrator rights to manage index sets and warm tiers.

Storing compliance-only data in a cheaper tier lowers cost while reserving fast storage for recent, often-searched data.

## Checked

2026-11-04. Confirmed against the Data Tiering page. Nothing removed.

Method: documentation only; no commands were run.
