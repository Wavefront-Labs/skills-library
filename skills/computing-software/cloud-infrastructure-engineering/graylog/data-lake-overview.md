---
id: computing-software.cloud-infrastructure-engineering.graylog.data-lake-overview
name: data-lake-overview
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [data-lake, internal-lake, external-lake, amazon-security-lake, license-usage]
level: practitioner
status: docs-checked
description: "Graylog Data Lake: internal versus external, preview and retrieval, license-usage effect and Data Lake versus archive."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/data_lake.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# data lake overview

A data lake provides long-term, lower-cost storage that you can preview and retrieve from.

- **Internal data lake**: create backend storage in Graylog, then use data routing to send ingested logs there.
- **External data lake**: connect an existing third-party lake. Only Amazon Security Lake is supported.

Preview gives a high-level look at stored data to decide whether to retrieve it. Retrieval writes selected data into the search backend for search, alerts, dashboards and reports.

Licensing: data routed only to an internal lake does not count against license usage until retrieved. If a license expires, you can still write to an internal lake, but you cannot preview or retrieve until renewal.

Setup needs administrator rights. Compared with archives, retrieval is selective and generally faster.

## Checked

2026-11-04. Confirmed against the Data Lake pages. Nothing removed.

Method: documentation only; no commands were run.
